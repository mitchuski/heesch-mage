# Heesch contribution: handoff to a signed-in agent

The user has authorized useful public Heesch research contributions and prefers
trying for a candidate result before publishing. A bounded follow-up is recorded
in RESEARCH_UPDATE.md. No post, PR or leaderboard submission has been made.

Use an already authenticated GitHub session or Yukon CLI. If authentication is
missing, ask the user to sign in through the normal interface; do not request,
print or include credentials in a post. No additional approval to publish these
reviewed research notes is needed.

1. Read RESEARCH_UPDATE.md, DISCUSSION_POST.md and FOLLOWUP_75.md. Check current
   discussions for overlapping posts and replies before publishing.
2. Publish the result reply on https://github.com/Layr-Labs/heesch/discussions/75.
   Integrate the newer certificate in RESEARCH_UPDATE.md with FOLLOWUP_75.md so
   the reply is current. Include the executable checks and preserve attribution.
3. Create a distinct discussion titled "Bitset contact graph: identical CNF
   output with 4.2–9.8x local encoding speedups" using DISCUSSION_POST.md.
   Its embedded patch and measurement records make it self-contained. Link the
   result reply and ask for maintainer CI and deeper Linux/RSS measurements.
4. Verify both published pages contain the intended content, then return their
   URLs. Record URLs and publication time in a receipt. Do not claim publication
   succeeded merely because a submit button was clicked or a request sent.

Do not submit to the leaderboard, modify the benchmark contract, open a PR
without a suitable checkout and validation, or claim that maintainers accepted
the patch. No new finite Heesch number has been established. Local timeouts are
UNKNOWN, solver UNSAT without a checked proof is provisional, and explicit
periodic partitions exclude shapes as finite-Heesch candidates.

The patch applies to upstream commit ce3b8d6974d3f318c3c6081b421ed51c7d041d6e,
which matched remote master when checked on 7 September 2026. Recheck before a
later PR. Tests completed and limitations are recorded in validation.json and
the post. No complete upstream CI or official dual-checker proof replay is claimed.

The measurements are single paired samples on Windows CPython 3.14. They measure
formula generation, not SAT solving, end-to-end proof throughput or score gain.
The algorithmic technique is standard; the contribution is its tested application.

Credits: upstream encoder and verifier authors; Craig S. Kaplan for parent shapes
and native solver; Frodan for the overlay recipe and earlier pipeline research;
nasqret for the public unresolved queue and calibration audit. Prepared with Codex.
