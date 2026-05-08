---
name: nextjs-setup
description: Create a new Next.js app or harden an existing one using the user's preferred Bun, strict TypeScript, ESLint, Prettier, Tailwind, shadcn, and AGENTS.md baseline. Use when the user wants to create, initialize, scaffold, set up, or update a Next.js project with bunx create-next-app@latest and strict project defaults.
---

# Next.js Setup

Create a new Next.js app or update an existing one with the user's preferred baseline.

## Start

1. Ask for the target path before running setup or edits.
2. Resolve the target path to an absolute path.
3. Inspect whether it already contains a Next.js app:
   - existing app: `package.json` with `next` in dependencies/devDependencies, or Next files such as `next.config.*`, `app/`, or `pages/`
   - new app: target path does not exist or has no Next.js project
4. Read `references/baseline.md` before changing files.

## New App Flow

1. Ensure the parent directory exists, creating it if needed.
2. Run setup from the parent directory:

```bash
bunx create-next-app@latest <app-directory-name>
```

3. Use the default `create-next-app` setup flow unless the user explicitly gives different preferences.
4. Apply the baseline from `references/baseline.md`.

## Existing App Flow

1. Inspect the existing `package.json`, lockfile, TypeScript, ESLint, Prettier, Tailwind, shadcn, and `AGENTS.md` setup.
2. Preserve app-specific dependencies, scripts, ports, product rules, environment handling, and generated files.
3. Apply only missing or weaker baseline pieces that fit the repo:
   - Bun-only package manager expectations
   - strict TypeScript flags
   - type-aware ESLint with React, Tailwind, and Prettier integration
   - Prettier config in `package.json`
   - explicit non-default Next.js dev/start port, preferably `6474` unless it conflicts
   - `bun run check` as the main combined validation script
   - Tailwind 4, typography, animation, and shadcn defaults when Tailwind/shadcn are used
   - App Router metadata conventions using Next.js `metadata`, `generateMetadata`, and file-based metadata
   - baseline `AGENTS.md` rules when absent or clearly weaker

## Path Handling

- If the user provides a path to the app directory, use its parent as the working directory and its basename as `<app-directory-name>`.
- If the provided path is relative, resolve it from the current workspace unless the user specifies a different base.
- Do not infer or invent a project path when the user has not provided one. Ask once for the path.

## Baseline Suggestions

When the user asks what should be used everywhere, suggest these defaults from the baseline repo:

- Bun only: `bun`, `bunx`, `bun run`, `bun add`, `bun remove`; never npm/pnpm/yarn.
- TypeScript: keep `strict` and add flags such as `exactOptionalPropertyTypes`, `noUncheckedIndexedAccess`, `noImplicitReturns`, `noImplicitOverride`, `noFallthroughCasesInSwitch`, and `noPropertyAccessFromIndexSignature`.
- ESLint: use Next core web vitals/typescript, `typescript-eslint` strict type-checked rules, React Compiler/hooks rules, Tailwind rules, Playwright rules for e2e folders, and `eslint-config-prettier`.
- Prettier: store strict formatting preferences in `package.json`, including `prettier-plugin-tailwindcss`.
- Scripts: prefer an explicit non-default Next.js port, usually `6474`, and include `bun run check` as the canonical combined validation command.
- Metadata: use the App Router Metadata API; put root defaults and title templates in layout metadata, page-specific dynamic titles in `generateMetadata`, and icons/OG/robots/sitemap in file-based metadata where possible.
- Tailwind/shadcn: prefer Tailwind 4 with `@tailwindcss/postcss`, `@tailwindcss/typography`, `tw-animate-css`, shadcn `new-york`, CSS variables, zinc base color, and lucide icons.
- Project guidance: include an `AGENTS.md` that leads with concise response style, Bun rules, scoped changes, validation expectations, and Next.js docs-as-source-of-truth.
- Frontend architecture: thin `app/` routes; reusable UI under `components/ui`, `components/shared`, `components/shells`, and `components/features/<feature>`; avoid runtime barrels and keep client boundaries narrow.

Do not copy baseline repo details that are product-specific, such as Convex, auth, app domain names, live test scripts, or feature import restrictions, unless the target project already uses those concepts or the user asks.

## Validation

- Confirm the generated directory exists.
- Inspect the generated `package.json`.
- For new or updated apps, run `bun run check` when available; otherwise run the smallest relevant checks, usually `bun run typecheck` and `bun run lint`.
- If the user asks to run it, start the dev server with `bun dev` and provide the local URL.
