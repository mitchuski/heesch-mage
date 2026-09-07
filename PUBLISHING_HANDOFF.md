# Publishing handoff

The user will perform the pushes. This preparation has not posted, opened a PR,
configured a remote, or submitted a leaderboard entry. The refreshed files are
uncommitted changes in this separate publishing repository, ready for review.

1. Read CONTRIBUTION.md and RESEARCH_UPDATE.md. Run the checks in REPRODUCE.md.
2. Inspect `git status --short` and `git diff --stat`, then commit the reviewed
   changes. Push this repository to your chosen research remote. Use your normal
   Git authentication; the bundle contains no credentials.
3. Reply to discussion #75 using FOLLOWUP_75.md. Attach
   public-queue-certificates.json and link the pushed repository at its commit.
   Check current replies first; these local results may overlap others' work.
4. Publish RESEARCH_DISCUSSION.md as a separate research Discussion with links
   to the committed certificates and checkers. Keep its local 184-shape family
   separate from the public 153-case queue.
5. For the encoder, use DISCUSSION_POST.md for review, or apply the supplied
   patch in a disposable upstream checkout and run current CI before opening a
   focused PR using PR_DESCRIPTION.md. Recheck the upstream base; the patch was
   tested against ce3b8d6974d3f318c3c6081b421ed51c7d041d6e, not an assumed latest HEAD.
6. After posting, verify the pages and record repository commit, Discussion/PR
   URLs and dates in PUBLICATION_RECEIPTS.md. Leave acceptance status pending
   until maintainers actually respond or merge.

No leaderboard submission is prepared: there is no new eligible witness with a
checked non-tiler proof. Research Discussions do not themselves earn score.
Prefer measured claims from CONTRIBUTION.md over the volume of generated files.
