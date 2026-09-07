# Publication receipts

Published 7 September 2026. Maintainer acceptance is not recorded; these are
posting receipts only.

- Research repository: https://github.com/mitchuski/heesch-mage
  - Published commit: `1d7298f096e6c3f3709e24798a26ca5a598502c7` (public, 7 September 2026).
- Public queue reply: https://github.com/Layr-Labs/heesch/discussions/75#discussioncomment-18338170
  (posted 7 September 2026 as `mitchuski`; body is FOLLOWUP_75.md with the
  certificate file linked at the pinned commit instead of attached).
- Inverse-design Discussion: https://github.com/Layr-Labs/heesch/discussions/83
  (posted 7 September 2026 via `yukon discussion create`; body is
  RESEARCH_DISCUSSION.md plus pinned repository links).
- Encoder Discussion: https://github.com/Layr-Labs/heesch/discussions/84
  (posted 7 September 2026 via `yukon discussion create`; body is
  DISCUSSION_POST.md plus an update recording the run below).
  - Discussions created through the Yukon CLI are brokered by Yukon's GitHub
    App and are authored by `yukon-autoresearch`; attribution is in the body.
- Encoder PR: not opened. Offered in Discussion #84 if maintainers prefer that route.
- Leaderboard submission: none prepared. No new eligible witness exists.

## Pre-publication verification, 7 September 2026

Against upstream `ce3b8d6974d3f318c3c6081b421ed51c7d041d6e`, confirmed via the
GitHub API to still be `Layr-Labs/heesch` master HEAD on that date.

| Check | Result |
| --- | --- |
| `verify_release.py` | 277 manifest hashes; 3 public-queue and 184 repair partitions |
| `check_inverse_identity.py` | 3,520 matrix entries; B = C A holds |
| `check_overlap_profile.py` | 184 matching bounds |
| `check_repair_examples.py` | 60 center-halo examples |
| `check_artifacts.py` | 162 geometry artifacts; 265 shape/certificate pairs |
| `git apply --check touch-graph-bitsets.patch` | clean at that commit |
| `python -m pytest tests/ -q` with the patch applied | 528 passed, 47 skipped, 7 subtests passed (499.08s) |

The pytest run was Windows, CPython 3.14, pytest 9.0.3 and python-sat 1.9.dev7,
which corresponds to upstream CI's Windows job only. The 47 skips are the
Linux-only paths; the `cake_lpr` proof-gate, census and harness e2e steps and
the repeated-timing and peak-RSS measurements were not run.

- Independent reproduction: pending external review.
- Maintainer decision or merge: pending.
