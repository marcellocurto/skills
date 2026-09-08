import { expect, test } from "bun:test";
import { join } from "node:path";

test("GitHub helpers preserve identity and retrieve complete review context", () => {
  const result = Bun.spawnSync(["python3", "-B", join(import.meta.dir, "github_helpers_test.py")]);
  if (result.exitCode !== 0) {
    throw new Error(result.stdout.toString() + result.stderr.toString());
  }
  expect(result.exitCode).toBe(0);
});
