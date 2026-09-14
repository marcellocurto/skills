import { readdir } from "node:fs/promises";
import { join, posix } from "node:path";

const guides = [
  {
    name: "vercel-react-best-practices",
    title: "React Best Practices",
    priorityLabel: "Investigation priority",
    introduction:
      "Use [SKILL.md](SKILL.md) and only the rules relevant to the task. This compiled reference is for deliberate full-guide reading. Apply optimizations only for a supported performance mechanism; ratings and example gains are not measurements of the current application.",
  },
  {
    name: "vercel-composition-patterns",
    title: "React Composition Patterns",
    priorityLabel: "Impact",
    introduction:
      "Use [SKILL.md](SKILL.md) to select the rules relevant to the task. This document combines all source rules for full-guide reading.",
  },
];
const checkOnly = Bun.argv.slice(2).includes("--check");

function record(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function requiredString(value: unknown, field: string, source: string): string {
  if (!record(value) || typeof value[field] !== "string" || !value[field].trim()) {
    throw new Error(`${source}: expected a nonempty ${field}`);
  }
  return value[field];
}

async function readRule(rulesRoot: string, name: string) {
  const source = (await Bun.file(join(rulesRoot, name)).text()).replaceAll("\r\n", "\n");
  const match = /^---\n([\s\S]*?)\n---\n([\s\S]*)$/.exec(source);
  if (!match?.[1] || !match[2]) throw new Error(`${name}: missing frontmatter or body`);
  const metadata: unknown = Bun.YAML.parse(match[1]);
  const title = requiredString(metadata, "title", name);
  const impact = requiredString(metadata, "impact", name);
  const description =
    record(metadata) && typeof metadata.impactDescription === "string"
      ? metadata.impactDescription
      : "";
  const body = match[2].trim();
  const heading = `## ${title}`;
  if (body.split("\n")[0] !== heading) throw new Error(`${name}: title and heading differ`);
  return {
    name,
    prefix: name.slice(0, name.indexOf("-")),
    title,
    impact,
    description,
    body: body
      .slice(heading.length)
      .trim()
      .replace(/^\*\*Impact: [^\n]+\*\*\n*/, ""),
  };
}

// Shift prose headings and relative links while preserving fenced code verbatim.
function compiledBody(body: string): string {
  let fence: string | undefined;
  return body
    .split("\n")
    .map((line) => {
      const marker = /^\s*(`{3,}|~{3,})/.exec(line)?.[1];
      if (fence) {
        if (
          marker &&
          marker[0] === fence[0] &&
          marker.length >= fence.length &&
          line.trim() === marker
        ) {
          fence = undefined;
        }
        return line;
      }
      if (marker) {
        fence = marker;
        return line;
      }
      return line
        .replace(/^(#{1,5}) /, "$1# ")
        .replace(
          /\]\((\.{1,2}\/[^\s)]+)\)/g,
          (_match: string, target: string) => `](${posix.normalize(posix.join("rules", target))})`,
        );
    })
    .join("\n");
}

async function compileGuide(guide: (typeof guides)[number]) {
  const skillRoot = join(import.meta.dir, "../skills", guide.name);
  const rulesRoot = join(skillRoot, "rules");
  const outputFile = Bun.file(join(skillRoot, "AGENTS.md"));
  const metadata: unknown = await Bun.file(join(skillRoot, "metadata.json")).json();
  const sectionSource = await Bun.file(join(rulesRoot, "_sections.md")).text();
  const sections = sectionSource
    .split(/^## /m)
    .slice(1)
    .map((source) => {
      const match =
        /^(\d+)\. (.+) \(([^)]+)\)\s*\n+\*\*Impact:\*\* (\S+)\s*\n\*\*Description:\*\* ([\s\S]+)$/.exec(
          source.trim(),
        );
      if (!match) throw new Error(`${guide.name}: invalid section metadata`);
      const [, number, title, prefix, impact, description] = match;
      if (!number || !title || !prefix || !impact || !description) {
        throw new Error("Invalid section metadata");
      }
      return { number, title, prefix, impact, description: description.trim() };
    });
  if (!sections.length) throw new Error("No rule sections found");

  const names = (await readdir(rulesRoot)).filter(
    (name) => name.endsWith(".md") && !name.startsWith("_"),
  );
  const rules = await Promise.all(names.map((name) => readRule(rulesRoot, name)));
  for (const rule of rules) {
    if (!sections.some((section) => section.prefix === rule.prefix)) {
      throw new Error(`${rule.name}: unknown section prefix ${rule.prefix}`);
    }
  }

  const contents: string[] = [];
  const chapters: string[] = [];
  for (const section of sections) {
    const members = rules
      .filter((rule) => rule.prefix === section.prefix)
      .toSorted((a, b) => (a.title < b.title ? -1 : a.title > b.title ? 1 : 0));
    contents.push(`${section.number}. **${section.title}**`);
    chapters.push(
      `## ${section.number}. ${section.title}\n\n**${guide.priorityLabel}: ${section.impact}**\n\n${section.description}`,
    );
    for (const [index, rule] of members.entries()) {
      const number = `${section.number}.${index + 1}`;
      const anchor = rule.name.slice(0, -3);
      contents.push(`   - ${number} [${rule.title}](#${anchor})`);
      const impact = `${rule.impact}${rule.description ? ` (${rule.description})` : ""}`;
      chapters.push(
        `<a id="${anchor}"></a>\n\n### ${number} ${rule.title}\n\n[Source rule](rules/${rule.name})\n\n**${guide.priorityLabel}: ${impact}**\n\n${compiledBody(rule.body)}`,
      );
    }
  }

  const generated =
    [
      `# ${guide.title}`,
      "<!-- Generated by scripts/compile-react-guidance.ts. Edit rules/ or metadata.json instead. -->",
      `**Version ${requiredString(metadata, "version", "metadata.json")}**  \n${requiredString(metadata, "organization", "metadata.json")}  \n${requiredString(metadata, "date", "metadata.json")}`,
      guide.introduction,
      requiredString(metadata, "abstract", "metadata.json"),
      "## Contents\n\n" + contents.join("\n"),
      chapters.join("\n\n---\n\n"),
    ].join("\n\n") + "\n";

  if (checkOnly) {
    if (!(await outputFile.exists()) || (await outputFile.text()) !== generated) {
      throw new Error(
        `${guide.name}: compiled guidance is stale. Run bun run react-guidance:build.`,
      );
    }
    console.log(`${guide.name}: compiled guidance matches ${rules.length} source rules.`);
  } else {
    await Bun.write(outputFile, generated);
    console.log(`${guide.name}: compiled ${rules.length} source rules.`);
  }
}

for (const guide of guides) await compileGuide(guide);
