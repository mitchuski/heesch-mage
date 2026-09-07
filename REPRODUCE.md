# Reproduce the evidence

Use a disposable checkout/environment of the upstream Heesch package at
`ce3b8d6974d3f318c3c6081b421ed51c7d041d6e`. Make its `heesch_verify` package
importable, for example by installing that checkout into your Python environment.
The release contains no vendored upstream package or native SAT dependencies.

From this repository's root, using that Python environment:

```sh
python verify_release.py
cd research
python -B check_inverse_identity.py
python -B check_overlap_profile.py
python -B check_repair_examples.py
python -B check_artifacts.py
```

Expected: release manifest valid; three public-queue and 184 repair partitions
checked; 80 exact row identities; 184 matching-bound checks; 60 center-halo
examples; 162 saved geometry artifacts and 265 shape/certificate pairs.
Some checkers rewrite their recorded check JSON with the same result. If files
are deliberately regenerated, review the changes and regenerate the manifest;
do not treat old hashes as covering new content.

Optional bounded search reproduction from research/:

```sh
python -B coordinated_repair.py --limit 60 --seconds 2 --target center
python -B coordinated_repair.py --limit 60 --seconds 2 --target inner-two
python -B repair_regrow.py
python -B repair_periodic.py
```

Search commands overwrite their corresponding result files. Machine-dependent
deadlines can change results; missing solutions remain UNKNOWN. Periodic search
reuses already certified results if present. Run in a copy to retain the release.

For the encoder patch, in a separate disposable upstream checkout:

```sh
git apply --check /path/to/touch-graph-bitsets.patch
git apply /path/to/touch-graph-bitsets.patch
python -m unittest discover -s tests/encoder -p test_touch_bitsets.py -v
```

Run upstream's current full CI before requesting merge. Historical local
validation and timing records are shipped; no new Linux run or official
non-tiler proof replay is implied by this release's certificate checks.
