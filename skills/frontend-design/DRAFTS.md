# Drafts

Drafts are exploratory. They show the user ideas they haven't considered yet, so the request and the current app are a starting point, not a boundary. A draft can restructure a page, invent features, workflows, and data that don't exist yet, or propose a page that has no current version at all. Unless the user asks to stay close to what exists, drafts don't need to follow the current pages' structure, features, or look. Make each draft a different idea, not the same layout restyled, and fill it with realistic content you make up when no real content is available. Drafts never change production code.

## Build

Put the drafts in `.tmp/drafts/<topic>/`, one plain HTML file per draft, named after its idea, such as `b-route.html`. If `git check-ignore -q .tmp/drafts` fails, add `.tmp/` to the file `git rev-parse --git-path info/exclude` prints, so the drafts stay out of commits without changing the project's `.gitignore`.

Each draft is a page the browser opens directly. Don't add a build step, and don't build a gallery, viewer, or wrapper page around the drafts.

## Screenshot

Use the screenshot command built into Playwright, and don't write a screenshot script. Take a desktop and a mobile screenshot of every draft:

```sh
D=.tmp/drafts/login
./node_modules/.bin/playwright-core screenshot --viewport-size=1440,900 --wait-for-timeout=1500 \
  "file://$PWD/$D/b-route.html" $D/b-route-desktop.png
./node_modules/.bin/playwright-core screenshot --viewport-size=390,844 --wait-for-timeout=1500 \
  "file://$PWD/$D/b-route.html" $D/b-route-mobile.png
```

- Set `--wait-for-timeout` past the end of the page-load animation. Don't record videos of animations; the user opens the link to see them.
- Add `--full-page` when the part of the page that matters is below the fold, and `--color-scheme=dark` when the draft has a dark variant worth showing.
- When `node_modules/.bin/playwright-core` is missing, run `bunx playwright-core@<version> screenshot ...` with the version from the lockfile, or the latest version if the project has none. When Chromium is missing, install it with `bunx playwright-core@<version> install --only-shell chromium`.

Look at both screenshots of each draft and fix visible defects, such as overflow, awkward wrapping, overlapping elements, low contrast, or a broken mobile layout. Then recheck only what changed. Don't iterate on polish.

## Present

For each draft, in the reply:

1. Its name and its idea in a sentence or two, including anything it invents that doesn't exist yet.
2. A link to the file by its absolute path, such as `[b-route.html](/abs/path/.tmp/drafts/login/b-route.html)`, so the user can open it live in one click.
3. The desktop and mobile screenshots, embedded by absolute path.

Don't also render the drafts inline with `html_render` or a similar tool; the screenshots and links are how the user wants to see them. End with a recommendation if one draft is clearly stronger.
