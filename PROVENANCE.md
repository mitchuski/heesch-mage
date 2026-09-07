# Provenance and attribution

Upstream verifier and encoder interface target:
https://github.com/Layr-Labs/heesch/tree/ce3b8d6974d3f318c3c6081b421ed51c7d041d6e

Public source queue and calibration audit by nasqret:
https://github.com/Layr-Labs/heesch/discussions/75

Exact public inputs:
https://gist.github.com/nasqret/598c8f7e05310294e5fc81b7af9b2e59

Parent shapes and native solver: Craig S. Kaplan,
https://arxiv.org/abs/2105.09438 and https://cs.uwaterloo.ca/~csk/heesch/ .
Overlay recipe: Frodan, as credited in discussion #75.

Local additions include the encoder patch and tests, search drivers, recovered
geometry and tiling certificates, exact incidence identities, repair bounds,
and these notes. Prepared by Mitch with Codex. Existing algorithms and parent
shapes are not claimed as new discoveries. No blanket new license is asserted
over upstream-derived fixtures, inputs or witnesses. Preserve attribution and
the applicable upstream terms when integrating them.

The upstream source tree, local Python dependencies, credentials, private paths,
and the active lab's operational state are excluded. Research results and
selected source files are copied byte-for-byte. MANIFEST.json records SHA-256
for release files other than the manifest, Git metadata, .gitattributes and
.gitignore. Aggregate historical results are retained as evidence; the current
claims are in CONTRIBUTION.md and RESEARCH_UPDATE.md.
