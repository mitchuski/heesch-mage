# Three independently checked periodic partitions from the shared queue

Thanks for publishing the exact input bank and calibration audit. We followed
up your [153-case queue](https://github.com/Layr-Labs/heesch/discussions/75), using
the unchanged public JSONL with SHA-256
`c131631a5fb1806f722031175e51d8576ddd74b46cc745eaeb7a76ab991621de`.
All 153 canonical identities and native-input hashes were checked locally.
Credit for the bank is nasqret's, the overlay recipe Frodan's, and the parent
shapes and native solver Kaplan's.

We recovered explicit residue partitions for three entries (zero-based indices):

| Index | Canonical digest | Lattice basis | Copies |
| --- | --- | --- | --- |
| 1 | f8df9dc177363142ba2df27d279a12b78b974c40f2f66d9418841fc5036bd0f6 | (8,0), (3,10) | 4 |
| 22 | 378a95b263f7cc868db91bce1d22bbfcb1047073086fb2ca63be402939f3228a | (8,0), (3,10) | 4 |
| 43 | b47720b325d371f956b7e58eb28dc0c63053f8b3e15b803a9f2dfa3bef51136e | (40,0), (4,4) | 8 |

Each tile has 20 cells. The certificates cover all 80, 80 and 160 residues
exactly once respectively, with no within-tile aliasing or between-tile overlap.
Their lattice translates therefore tile the plane. This is positive certificate
evidence, not reliance on the native periodic marker. We do not claim these are
minimal periods or that nobody else has classified the same inputs.

The attached `public-queue-certificates.json` contains exact cells, transforms,
identities and provenance. With the pinned upstream verifier importable, run
`python verify_release.py` from the contribution repository to check all three
partitions as well as the local mutation certificates.

In total, 72 entries received mixed bounded follow-up here; 81 remain untouched.
Indices 24 and 34 have verified two-ring witnesses but unresolved tiling status.
Search timeouts remain UNKNOWN, and experimental UNSAT/exhaustion reports are
not official checked non-tiler proofs. No record or leaderboard gain is claimed.

Our separate 184-shape inverse-design repair queue also proved periodic; those
are derived local mutations, not 184 exclusions from this 153-case bank. We
report that experiment separately to keep classifications unambiguous.

Prepared by Mitch with Codex. We welcome independent certificate reproduction
and correction of any overlap with existing classifications.
