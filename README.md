# iPhone build checks

Check the pinned Super Mario Odyssey iOS source on GitHub's Apple Silicon Xcode 27 runner. The default run performs game-free checks. Game data and keys are never committed. Game-bearing IPA artifacts are disabled for public repositories; private-repository artifacts expire after one day.

For a full private build, the owner supplies three Actions secrets: `TRANSFER_URL`, `TRANSFER_TOKEN`, and `PROD_KEYS`. A temporary HTTPS endpoint requires the transfer token on every request and serves only the two selected input files. The workflow returns the IPA to the workstation in chunks and verifies its size and SHA-256 before accepting it. Stop the temporary endpoint and remove its Actions secrets when the run finishes.
