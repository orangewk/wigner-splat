# Project Agent Notes

- Before retrying a hung pytest run, do not start a second pytest process; first inspect/stop the original process and record the hang diagnosis.
- When stating what an external licence, standard, or paper says, fetch the primary source and quote only what you verified there; a search snippet or a plausible paraphrase is not a source. (2026-07: a zero-counting lemma was cited from a snippet and had to be withdrawn; the Tanks and Temples licence terms were recorded inaccurately for weeks.)
- Before deleting a branch or worktree, or promoting one into main, check its dirty state and the head of each changed file; publication status is sometimes recorded in uncommitted working-tree edits rather than in commits. (2026-07: a doc marked "Private, local only" in an uncommitted edit was merged into the public repo and had to be reverted.)
- Code that prints a verdict must compute it from the data. Never hard-code the conclusion in the output string. (2026-07: routeB.py printed "cutoff-stable" unconditionally; the claim propagated into the README and the archived preprint while the measured series was increasing.)
