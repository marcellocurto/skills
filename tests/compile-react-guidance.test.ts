import { expect, test } from "bun:test";
import { copyFile, mkdir, mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

const skillNames = ["vercel-react-best-practices", "vercel-composition-patterns"];

test("builds both guides without losing wrapped descriptions or code", async () => {
  await withRepository(async (root, run) => {
    expect((await run()).exitCode).toBe(0);
    for (const name of skillNames) {
      const compiled = await Bun.file(join(root, "skills", name, "AGENTS.md")).text();
      expect(compiled).toContain("A description that wraps\nonto another line.");
      expect(compiled).toContain("```md\n## Keep this code heading\n[link](./example.md)\n```");
      expect(compiled).toContain("[Related](rules/example.md)");
    }
    expect((await run("--check")).exitCode).toBe(0);
  });
});

for (const name of skillNames) {
  test(`detects stale ${name} output and repairs it on build`, async () => {
    await withRepository(async (root, run) => {
      expect((await run()).exitCode).toBe(0);
      const rule = Bun.file(join(root, "skills", name, "rules", "architecture-example.md"));
      await Bun.write(rule, (await rule.text()) + "\nAn updated example.\n");

      const stale = await run("--check");
      expect(stale.exitCode).not.toBe(0);
      expect(stale.output).toContain(name);
      const compiled = Bun.file(join(root, "skills", name, "AGENTS.md"));
      expect(await compiled.text()).not.toContain("An updated example.");

      expect((await run()).exitCode).toBe(0);
      expect(await compiled.text()).toContain("An updated example.");
      expect((await run("--check")).exitCode).toBe(0);

      await Bun.write(compiled, (await compiled.text()) + "\nAn accidental generated-file edit.\n");
      expect((await run("--check")).exitCode).not.toBe(0);
    });
  });
}

async function withRepository(
  verify: (
    root: string,
    run: (...args: string[]) => Promise<{ exitCode: number; output: string }>,
  ) => Promise<void>,
) {
  const root = await mkdtemp(join(tmpdir(), "react-guidance-test-"));
  try {
    await mkdir(join(root, "scripts"));
    const script = join(root, "scripts", "compile-react-guidance.ts");
    await copyFile(join(import.meta.dir, "../scripts/compile-react-guidance.ts"), script);
    for (const name of skillNames) {
      const directory = join(root, "skills", name);
      await mkdir(join(directory, "rules"), { recursive: true });
      await Bun.write(
        join(directory, "metadata.json"),
        JSON.stringify({
          version: "1",
          organization: "Example",
          date: "Today",
          abstract: "Example",
        }),
      );
      await Bun.write(
        join(directory, "rules", "_sections.md"),
        "## 1. Architecture (architecture)\n\n**Impact:** HIGH  \n**Description:** A description that wraps\nonto another line.\n",
      );
      await Bun.write(
        join(directory, "rules", "architecture-example.md"),
        "---\ntitle: Example\nimpact: HIGH\n---\n\n## Example\n\n[Related](./example.md)\n\n```md\n## Keep this code heading\n[link](./example.md)\n```\n",
      );
    }
    await verify(root, async (...args) => {
      const process = Bun.spawn([Bun.which("bun") ?? "bun", script, ...args], {
        cwd: root,
        stdout: "pipe",
        stderr: "pipe",
      });
      const [exitCode, stdout, stderr] = await Promise.all([
        process.exited,
        new Response(process.stdout).text(),
        new Response(process.stderr).text(),
      ]);
      return { exitCode, output: stdout + stderr };
    });
  } finally {
    await rm(root, { recursive: true, force: true });
  }
}
