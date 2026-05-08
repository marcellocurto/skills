# Baseline Next.js Setup

Use this as the reusable baseline. Adapt to the target repo instead of blindly copying app-specific details.

## Source Baseline

Inspired by `/Users/marcellocurto/Code/app.tenderintelligenceplatform.com/`.

Reusable:

- Bun-only workflow.
- Strict TypeScript.
- Type-aware ESLint.
- Prettier config in `package.json`.
- Tailwind 4 plus useful plugins.
- shadcn defaults.
- Explicit non-default Next.js dev/start port.
- `bun run check` as the combined validation command.
- App Router metadata conventions.
- `AGENTS.md` working rules.
- Frontend component ownership rules.

Avoid by default:

- Convex-specific scripts, rules, generated paths, and docs.
- Product-specific dependencies and import restrictions.
- Auth, email, storage, live-test, and domain-specific scripts.

## Package Manager

Use Bun only:

- `bun`
- `bunx`
- `bun run <script>`
- `bun add`
- `bun remove`

Do not use `npm`, `npx`, `pnpm`, `yarn`, `npm install`, or `npm run`. Keep `bun.lock` as the lockfile and do not create `package-lock.json`.

## Recommended Scripts

Keep scripts small and standard unless the repo needs more:

```json
{
  "scripts": {
    "dev": "next dev --port 6474",
    "build": "next build",
    "start": "next start --port 6474",
    "lint": "eslint . --cache --cache-strategy content --cache-location .eslintcache",
    "lint:full": "eslint .",
    "typecheck": "tsc --noEmit",
    "check": "bun run lint && bun run typecheck",
    "format": "prettier --write '**/*.{ts,tsx,js,jsx,css,md}'"
  }
}
```

Prefer a non-default Next.js port so parallel local projects do not fight over `3000`. Use `6474` unless it conflicts or the target repo already has a clear port convention. If a project has multiple dev processes, keep `dev` as the main command and split Next into `dev:next`.

`bun run check` should be the standard handoff validation. Add project-specific guardrails to `check` only when they are deterministic and worth running before handoff.

## Dependencies To Consider

Dev dependencies for the strict baseline:

```bash
bun add -d eslint eslint-config-next eslint-config-prettier typescript typescript-eslint prettier prettier-plugin-tailwindcss eslint-plugin-react-compiler eslint-plugin-tailwindcss @tailwindcss/postcss @tailwindcss/typography tailwindcss tw-animate-css
```

Add `eslint-plugin-playwright` only when the repo has e2e tests or Playwright folders.

Common app dependencies when using shadcn/UI primitives:

```bash
bun add class-variance-authority clsx tailwind-merge lucide-react
```

Add Radix packages only for components actually installed.

## Prettier

Prefer package-level Prettier config:

```json
{
  "prettier": {
    "trailingComma": "es5",
    "tabWidth": 2,
    "useTabs": true,
    "semi": true,
    "singleQuote": false,
    "proseWrap": "preserve",
    "quoteProps": "as-needed",
    "arrowParens": "always",
    "bracketSpacing": true,
    "endOfLine": "lf",
    "htmlWhitespaceSensitivity": "css",
    "insertPragma": false,
    "singleAttributePerLine": false,
    "bracketSameLine": false,
    "jsxSingleQuote": false,
    "printWidth": 80,
    "plugins": ["prettier-plugin-tailwindcss"]
  }
}
```

## TypeScript

Keep Next defaults and add stricter correctness flags:

```json
{
  "compilerOptions": {
    "strict": true,
    "exactOptionalPropertyTypes": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "noImplicitReturns": true,
    "noPropertyAccessFromIndexSignature": true,
    "noUncheckedIndexedAccess": true,
    "useUnknownInCatchVariables": true,
    "types": ["bun", "node"]
  }
}
```

Preserve the target repo's `target`, `module`, `moduleResolution`, `jsx`, `paths`, `include`, and `exclude` unless they are clearly weaker or broken.

## ESLint

Use flat config when possible. Baseline ingredients:

- `eslint-config-next/core-web-vitals`
- `eslint-config-next/typescript`
- `typescript-eslint` with `strictTypeChecked`
- `parserOptions.projectService: true`
- `eslint-plugin-react-compiler`
- strict React hooks rules
- `eslint-plugin-tailwindcss`
- optional `eslint-plugin-playwright` for e2e folders
- `eslint-config-prettier` last
- global ignores for `.next/**`, `out/**`, `build/**`, and `next-env.d.ts`

Rules worth carrying everywhere:

- `@typescript-eslint/consistent-type-imports`
- `@typescript-eslint/consistent-type-exports`
- `@typescript-eslint/no-floating-promises`
- `@typescript-eslint/no-misused-promises`
- `@typescript-eslint/no-non-null-assertion`
- `@typescript-eslint/no-unnecessary-condition`
- `@typescript-eslint/no-unnecessary-type-assertion`
- `@typescript-eslint/prefer-nullish-coalescing`
- `@typescript-eslint/prefer-optional-chain`
- `@typescript-eslint/restrict-template-expressions`
- `@typescript-eslint/strict-boolean-expressions`
- `@typescript-eslint/switch-exhaustiveness-check`
- `react-hooks/exhaustive-deps`
- `react-hooks/purity`
- `react-hooks/refs`
- `react-hooks/static-components`
- `react-compiler/react-compiler`
- `react/jsx-no-leaked-render`
- `react/no-unstable-nested-components`
- `tailwindcss/classnames-order`
- `tailwindcss/enforces-shorthand`
- `tailwindcss/no-contradicting-classname`
- `tailwindcss/no-unnecessary-arbitrary-value`

For tests, relax only rules that create false positives, such as `@typescript-eslint/unbound-method`.

## Tailwind And shadcn

For Tailwind 4, use `postcss.config.mjs`:

```js
const config = {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};

export default config;
```

Global CSS should start with:

```css
@import "tailwindcss";
@import "tw-animate-css";
@plugin "@tailwindcss/typography";

@custom-variant dark (&:is(.dark *));
```

Prefer this `components.json` baseline:

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "styles/globals.css",
    "baseColor": "zinc",
    "cssVariables": true,
    "prefix": ""
  },
  "iconLibrary": "lucide",
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "registries": {}
}
```

## Next.js Metadata

Use the App Router Metadata API instead of manually managing `<head>` tags.

Baseline root layout metadata:

```tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  metadataBase: new URL("https://example.com"),
  title: {
    default: "App Name",
    template: "%s - App Name",
  },
  description: "Short product description.",
};
```

Rules:

- Use static `export const metadata: Metadata` for metadata that does not depend on route params, request data, or fetched content.
- Use `export async function generateMetadata(...): Promise<Metadata>` only when metadata is dynamic.
- Keep `metadata` and `generateMetadata` in Server Components only. If a page needs client interactivity, keep the page/server layout as the metadata owner and move interactive UI into child `"use client"` components.
- Do not export both `metadata` and `generateMetadata` from the same route segment.
- In Next.js 15+ style code, type `params` and `searchParams` as promises and await them inside `generateMetadata`.
- Prefer `metadataBase` at the root so URL-based metadata fields resolve predictably.
- Remember metadata merges shallowly from root to leaf. Nested fields such as `openGraph` and `robots` are replaced by later segments, so intentionally extend parent metadata when needed.
- Use `React.cache` or cached data helpers when the same non-`fetch` data is needed by both metadata and the page. `fetch` calls are automatically memoized by Next.js across metadata, layouts, pages, and static params.
- Use file-based metadata for assets and special routes when possible: `favicon.ico`, `icon.*`, `apple-icon.*`, `opengraph-image.*`, `twitter-image.*`, `robots.ts`, `sitemap.ts`, and `manifest.ts`.
- Use `next/og` for generated Open Graph images, not `@vercel/og`.
- Keep viewport concerns separate with `viewport` or `generateViewport` when customizing viewport/theme color.
- For localized apps, set the `html lang` attribute in layout and generate localized titles/descriptions from the server-side i18n layer.

Dynamic metadata pattern:

```tsx
import type { Metadata } from "next";

type Props = {
  params: Promise<{ slug: string }>;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPost(slug);

  return {
    title: post.title,
    description: post.description,
  };
}
```

## AGENTS.md

Create or update `AGENTS.md` with these reusable rules:

- Lead with the answer; be concise without losing exact constraints.
- Ship production-quality work only.
- Stay in scope and avoid opportunistic refactors.
- Ask before ambiguous destructive changes.
- Do not edit generated artifacts unless asked.
- Do not touch `.env*`, secrets, production deploy config, or credentials unless asked.
- Use Bun only.
- Local dev runs with `bun dev` on an explicit non-default Next.js port, preferably `6474`.
- Commit only when explicitly asked in the current turn.
- After edits, run `bun run check` when available; otherwise run the smallest relevant validation: targeted test, typecheck, lint, or script.
- Final responses should include changed files, validation, and risks or follow-ups.
- Before Next.js work, read relevant docs in `node_modules/next/dist/docs/` when available.
- Use Next.js App Router metadata APIs for page metadata; do not hand-roll `<head>` management.

## Frontend Architecture

Use these defaults for app structure:

- Keep `app/` route files thin; reserve it for Next.js route conventions.
- Put primitive design-system UI in `components/ui`.
- Put reusable product UI in `components/shared`.
- Put app chrome and route shells in `components/shells`.
- Put feature-owned UI in `components/features/<feature>`.
- Prefer Server Components by default.
- Add `"use client"` only at the smallest interactive leaf.
- Name paired client boundary files `*.client.tsx`.
- Avoid runtime barrel imports and `index.ts` re-export files for features.
- Pass plain serializable data from server components to client components.
