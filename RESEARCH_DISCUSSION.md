# When preserving a corona forces periodicity: a checked inverse-design experiment

We tried inverse tile design: keep a verified arrangement and edit the tile
instead of generating shapes first and searching for surrounds. In one periodic
20-cell seed, this recovered 29 distinct legal variants with three verified
rings, but every one admitted an explicit periodic tiling.

There is an exact explanation for this particular search family. Let A encode
occupancy of 205 protected cells under the fixed 37 placements, with 44 possible
tile cells as columns. Let B encode occupancy of the 80 residues in the seed's
four-copy periodic template. We exported rational coefficients C and separately
rebuilt both matrices from geometry, checking all 80 identities in B = C A
directly (3,520 entries). Both A and [A;B] have rank 27.

For the original occupancy x0, A x0 = 1 and B x0 = 1. Thus any binary tile x in
this specified domain satisfying A x = A x0 also satisfies B x = 1. Preserving
the protected occupancy therefore forces that periodic partition, even for
larger edits within this domain. This is a conditional result about fixed poses
and fixed constraints, not a general impossibility theorem for Heesch numbers.

We then relaxed protection to the center or center plus halo. Rank(A) dropped
to 20 while rank([A;B]) stayed 27, breaking that implication. Complete one/two-cell
exchanges produced 214 legal variants per relaxation: 29 already-known accepted
tilers, 184 overlapping the inherited arrangement, and one ring-label failure.

For all 184 overlapping variants, explicit disjoint-edge matchings and matching
vertex covers independently prove the minimum inherited placements that must
change: nine for 60 shapes and ten for 124. These are fixed-pose bounds only.
Across the 60 nine-change shapes, enumerating minimum removal choices recovered
two verified three-ring repairs preserving the source inner-two-ring region and
halo. The other 58 had an uncoverable target cell for every minimum cover.
Releasing the outer scaffold and regrowing from a repaired first corona produced
eleven three-ring and one two-ring witness in a twelve-shape sample.

However, all 184 shapes subsequently yielded explicit checked periodic
partitions. Destroying one tiling template had merely exposed other tilings.
This closes that repair queue as finite-Heesch candidates. It does not classify
the separate ring-label failure or establish a shape's finite Heesch number.

The reusable result is a diagnostic and a set of counterexamples: check whether
patch-incidence constraints imply a known periodic template before enumerating
mutations, then filter surviving shapes against additional explicit templates
before expensive corona regrowth. Failure of the implication never proves
non-tilerhood. This release tests that workflow; it does not establish global
novelty for linear algebra, matching, exact cover, or inverse design.

The repository includes `research/results/inverse-periodic-obstruction.json`,
the independent `check_inverse_identity.py`, matching certificates and checker,
all 184 tiling certificates in `research/results/repair-periodic.json`, and
repaired witnesses. REPRODUCE.md gives the checks. No official proof gate or
leaderboard improvement is claimed.

Background and attribution: [Kaplan's polyform work](https://arxiv.org/abs/2105.09438),
the [upstream verifier](https://github.com/Layr-Labs/heesch), and
[nasqret's shared queue](https://github.com/Layr-Labs/heesch/discussions/75),
following Frodan's overlay recipe. Prepared by Mitch with Codex.
