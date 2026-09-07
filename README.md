# Heesch Mage contribution

A publication handoff for a tested multilevel-encoder performance patch and
independent follow-up of the public Heesch unresolved-shape queue.

Start with **RESEARCH_UPDATE.md** for the latest results, then
**PUBLISHING_HANDOFF.md** for the authorized publishing steps.
**DISCUSSION_POST.md** contains the encoder proposal and full patch;
**FOLLOWUP_75.md** contains the original result reply with a runnable certificate
check. Integrate RESEARCH_UPDATE.md before posting the older first-batch drafts.

No post, PR, leaderboard improvement or new finite Heesch number is claimed.
The user authorized substantive research posts, with an authenticated publishing
agent handling them. No credentials or local dependency installations are included.
Publication receipts should record verified public URLs and dates.

## Validation and reproduction

The patch targets upstream commit
`ce3b8d6974d3f318c3c6081b421ed51c7d041d6e` in
https://github.com/Layr-Labs/heesch. Apply it in a disposable checkout:

```sh
git apply --check /path/to/touch-graph-bitsets.patch
git apply /path/to/touch-graph-bitsets.patch
python -m unittest discover -s tests/encoder -p test_touch_bitsets.py -v
```

Seven existing universe/CNF golden fixtures and 240 geometric-oracle cases passed
across four fresh hash-seed processes. Three emission lint checks also passed.
Six paired local formula measurements preserve ordered-clause digests and metadata.
`validation.json` and `evidence/` preserve results. The full upstream CI, official
proof pipeline and deeper Linux peak-memory measurements remain pending.

MANIFEST.json verifies the selected exported source artifacts. README.md and the
Git metadata are packaging additions. Review newer upstream changes before a PR.

## Attribution and scope

The `research/` directory includes the pure-Python screening code, exact public
input bank, latest results and recovered witnesses. Install the unchanged upstream
package into a disposable Python environment first (`python -m pip install -e
/path/to/heesch`); the verifier must be importable. Then, from `research/`, run
`python discussion_periodic.py --offset 48 --limit 12 --seconds 3`, followed by
`python discussion_geometry.py --offset 48 --seconds 3`. No native SAT package is
needed for this fallback. Preserve existing results when rerunning earlier offsets.

Credit upstream encoder/verifier authors, Craig S. Kaplan for parent shapes and
native solver, Frodan for the overlay recipe and earlier pipeline work, and
nasqret for the public unresolved queue and calibration audit. Prepared with Codex.
No blanket new license is asserted for upstream-derived material; preserve its
provenance and consult upstream terms before redistributing broader source trees.

The active search lab remains separate. This repository contains only the selected
contribution files for syncing with the publishing agent. No remote is configured.
