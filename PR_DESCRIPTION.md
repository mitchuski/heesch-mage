# Build multilevel contact pairs with cell-incidence bitsets

Large placement universes spend time materializing contact pairs that are then
discarded because the tiles overlap. Build occupied-cell incidence bitsets,
subtract overlap sets from contact sets, and extract surviving indices in
ascending order. The resulting disjoint contact pairs preserve emission order
without adding a runtime dependency.

Local validation: seven existing universe/CNF golden fixtures, 240 randomized
geometric comparisons across three grids and both contact modes, repeated under
four hash seeds, plus three emission lint checks. Six paired formula-generation
measurements retained identical ordered clause digests and metadata and showed
4.18–9.79x elapsed-time improvements on Windows CPython 3.14. These are single
paired samples, not Linux medians or end-to-end SAT performance measurements.

The supplied three-file patch targets commit
ce3b8d6974d3f318c3c6081b421ed51c7d041d6e. Full current upstream CI and deeper
Linux/RSS measurements remain pending. No benchmark-rule, verifier-contract,
non-tiler-proof, or leaderboard result is changed. See DISCUSSION_POST.md and
validation.json for raw evidence and limitations.
