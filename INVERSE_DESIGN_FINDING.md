# Inverse tile design and a checked periodicity implication

Instead of generating a shape and searching for rings, this experiment fixes a
verified ring arrangement and searches for a new tile compatible with it.
Exact integer incidence signatures match one- and two-cell removals to additions
in the tile's first edge-neighbor shell. Matched edits preserve occupancy of a
protected region, then pass the unchanged full geometry verifier.

Seven arrangements were examined: five known-record depth-three controls, the
20-cell periodic depth-three control from discussion #75, and the inherited
four-ring incumbent. The six known-record arrangements admitted no matching
one/two-cell exchanges under these specific constraints. This says nothing about
other placements, larger edits, or edits that move the protected region.

The periodic 20-cell arrangement admitted 45 signature matches, yielding 30 legal
new canonical shapes in this experiment. Twenty-nine retained verified three-ring
witnesses; one failed the ring-level check. All 29 accepted variants have explicit
periodic partition certificates. These are not new finite-Heesch candidates.

An exact algebraic check explains the failure to escape periodicity in this family.
Let x be the binary occupancy vector on the 44 possible tile cells: the original
20 cells plus 24 boundary cells. Let A record the occupancy induced by the fixed
37 placements on the 205 protected cells. Let B record the occupancy induced by
the original four-copy periodic template on its 80 lattice residues.

Both A and the stacked matrix [A;B] have rational rank 27. More concretely, the
exported certificate expresses every row of B as a rational combination of rows
of A: B = C A. A separate checker rebuilt both incidence matrices directly from
the transforms, then checked all 80 row identities by multiplication, covering
3,520 matrix entries. It does not rely on the elimination routine's rank verdict.

The original tile x0 satisfies A x0 = 1 and B x0 = 1. Therefore any binary tile
x in this domain with A x = A x0 also satisfies

```text
B x = C A x = C A x0 = B x0 = 1.
```

Thus the four-copy template still partitions every lattice residue exactly once,
and its lattice translates tile the plane. This applies to arbitrary binary
edits inside this 44-cell domain satisfying these protected occupancy constraints,
not merely the one/two-cell exchanges enumerated. It is a checked conditional
obstruction to this inverse-design family, not a general impossibility theorem
about Heesch numbers, fixed-corona methods, or shape deformation.

The useful next experiment must change the assumptions: permit selected placement
changes, let the protected region change, or choose a different arrangement whose
patch-incidence constraints do not imply a known periodic template. Row-space
testing offers a cheap diagnostic before spending time enumerating such a family.
That diagnostic does not prove non-tilerhood when implication fails.

Reproduce with `inverse_patch_design.py`, `inverse_periodic_obstruction.py`, and
`check_inverse_identity.py`. The result and explicit row certificate are in
`results/inverse-periodic-obstruction.json`; the independent check is in
`results/inverse-identity-check.json`. `check_artifacts.py` rechecks the geometric
witnesses and periodic partitions. No official non-tiler proof gate was run.

Background: Kaplan's [Heesch polyform work](https://arxiv.org/abs/2105.09438)
establishes the SAT-based surround framework; the public seed here comes from
[discussion #75](https://github.com/Layr-Labs/heesch/discussions/75), with attribution
to nasqret for the queue, Frodan for the overlay recipe, and Kaplan for parent shapes.
The inverse-design and exact implication checks above are this lab's experiment;
no claim of global methodological novelty is made.
