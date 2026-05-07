---
name: nextjs-setup
description: Set up a default Next.js app using the user's preferred CLI flow. Use when the user wants to create, initialize, scaffold, or set up a new Next.js project with bunx create-next-app@latest.
---

# Next.js Setup

Set up a new default Next.js app with the user's preferred CLI command.

## Workflow

1. Ask for the target path before running setup.
2. Resolve the target path to an absolute path.
3. Ensure the parent directory exists, creating it if needed.
4. Run the setup from the parent directory:

```bash
bunx create-next-app@latest <app-directory-name>
```

5. Use the default `create-next-app` setup flow unless the user explicitly gives different preferences.
6. After setup, report the project path and any commands needed to start the app.

## Path Handling

- If the user provides a path to the app directory, use its parent as the working directory and its basename as `<app-directory-name>`.
- If the provided path is relative, resolve it from the current workspace unless the user specifies a different base.
- Do not infer or invent a project path when the user has not provided one. Ask once for the path.

## Defaults

- Package manager command: `bunx create-next-app@latest`
- Setup style: default Next.js setup
- Additional preferences: none yet

## Validation

- Confirm the generated directory exists.
- Inspect the generated `package.json`.
- If the user asks to run it, start the dev server with the package manager selected by `create-next-app` and provide the local URL.
