import { mkdtemp, readFile, rm } from "node:fs/promises";
import { homedir, tmpdir } from "node:os";
import { join } from "node:path";

const source = "marcellocurto/skills";
const repository = `https://github.com/${source}`;
const cli = ["bunx", "skills@1.7.0"];
const agents = ["--global", "--agent", "codex", "--agent", "claude-code", "--yes"];

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

export function publishedSkillNames(manifest: unknown): string[] {
  if (!isRecord(manifest) || !Array.isArray(manifest.skills) || !manifest.skills.length) {
    throw new Error("Published plugin must contain a nonempty skills list; refusing cleanup.");
  }
  return manifest.skills.map((path: unknown) => {
    if (typeof path !== "string" || !/^\.\/skills\/[a-z0-9]+(?:-[a-z0-9]+)*$/.test(path)) {
      throw new Error("Invalid published skill path; refusing cleanup.");
    }
    return path.slice("./skills/".length);
  });
}

function skillEntries(lock: unknown): Record<string, unknown> {
  if (!isRecord(lock) || !isRecord(lock.skills)) {
    throw new Error("Invalid skills lock file; refusing to guess installation ownership.");
  }
  return lock.skills;
}

function isManaged(entry: unknown): entry is Record<string, unknown> {
  return isRecord(entry) && entry.source === source && entry.sourceType === "github";
}

export function removedSkillNames(lock: unknown, published: readonly string[]): string[] {
  if (!published.length) throw new Error("Cannot reconcile an empty published skill list.");
  return Object.entries(skillEntries(lock))
    .filter(([name, entry]) => isManaged(entry) && !published.includes(name))
    .map(([name]) => {
      if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name)) {
        throw new Error("Invalid managed skill name; refusing cleanup.");
      }
      return name;
    });
}

async function run(command: string[], capture = false): Promise<string> {
  const child = Bun.spawn(command, {
    stdout: capture ? "pipe" : "inherit",
    stderr: "inherit",
    env: { ...process.env, GIT_TERMINAL_PROMPT: "0", GH_HOST: "github.com" },
  });
  const output = capture ? await new Response(child.stdout).text() : "";
  if ((await child.exited) !== 0) throw new Error(`Command failed: ${command.join(" ")}`);
  return output.trim();
}

async function install() {
  const lockPath = process.env.XDG_STATE_HOME
    ? join(process.env.XDG_STATE_HOME, "skills", ".skill-lock.json")
    : join(homedir(), ".agents", ".skill-lock.json");
  async function readLock(): Promise<unknown> {
    try {
      return JSON.parse(await readFile(lockPath, "utf8"));
    } catch (error) {
      if (isRecord(error) && error.code === "ENOENT") return { skills: {} };
      throw error;
    }
  }

  const directory = await mkdtemp(join(tmpdir(), "install-marcello-skills-"));
  try {
    await run(["git", "clone", "--quiet", "--depth", "1", `${repository}.git`, directory]);
    const revision = await run(["git", "-C", directory, "rev-parse", "HEAD"], true);
    const published = publishedSkillNames(
      JSON.parse(await readFile(join(directory, ".claude-plugin", "plugin.json"), "utf8")),
    );
    const before = skillEntries(await readLock());
    for (const name of published) {
      if (before[name] !== undefined && !isManaged(before[name])) {
        throw new Error(`${name} belongs to another installation; refusing to overwrite it.`);
      }
    }

    // Install and reconcile against the same published revision, never the local checkout.
    await run([
      ...cli,
      "add",
      `${repository}/tree/${revision}`,
      "--skill",
      ...published,
      ...agents,
    ]);
    const after = await readLock();
    const entries = skillEntries(after);
    for (const name of published) {
      const entry = entries[name];
      if (!isManaged(entry) || entry.ref !== revision) {
        throw new Error(
          `Installation of ${name} was not recorded; leaving obsolete skills intact.`,
        );
      }
    }
    const removed = removedSkillNames(after, published);
    if (removed.length) {
      // Other detected agents also share the canonical directory. Limiting removal
      // to Codex and Claude leaves that directory and its tracking entry installed.
      await run([...cli, "remove", ...removed, "--global", "--yes"]);
      const remaining = removedSkillNames(await readLock(), published);
      if (remaining.length) throw new Error(`Cleanup incomplete: ${remaining.join(", ")}`);
    }
    console.log(`Installed ${published.length} skills; removed ${removed.length} obsolete skills.`);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

if (import.meta.main) await install();
