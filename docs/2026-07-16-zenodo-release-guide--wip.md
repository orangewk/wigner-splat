# Zenodo release guide: wigner-splat v0.1.0

Status: wip. Owner action after the Zenodo-preparation PR is merged.

## Goal

Archive the exact `v0.1.0` GitHub release on Zenodo and obtain a citable DOI.
The DOI identifies a fixed software release; it is not peer review or a
scientific endorsement.

## Before starting

Confirm that the Zenodo-preparation PR is merged into `main`, and that
`README.md`, `CITATION.cff`, `LICENSE`, experiment logs, and
[`2026-07-16-v0.1.0-release-notes--proposed.md`](2026-07-16-v0.1.0-release-notes--proposed.md)
are present. Do not publish if the release notes conflict with the README or
research log.

## 1. Connect Zenodo and enable this repository

1. In a signed-in browser, open <https://zenodo.org/account/settings/github>.
   The page should show a GitHub connection panel and accessible repositories.
2. If it shows **Connect**, select it and complete GitHub authorization. Return
   to the same URL; the repository list should now be visible.
3. Find `orangewk/wigner-splat` and enable its toggle. Its row should indicate
   that new GitHub releases will be archived by Zenodo.

If the repository is absent, check that it is public and the connected GitHub
account is `orangewk`, then reload. Do not create a manual duplicate archive.

## 2. Publish the GitHub release

1. Open <https://github.com/orangewk/wigner-splat/releases/new>. The page
   should show **Choose a tag**, a title field, and a Markdown notes editor.
2. Create the tag `v0.1.0` from `main`, and title the release
   `wigner-splat v0.1.0`.
3. Copy the release notes from the `## Scope` heading onward into the notes
   editor. The preview should show the scope, evidence, and limits.
4. Keep **Set as the latest release** enabled and do not mark it as a
   prerelease. Select **Publish release**. GitHub should show a published
   release page with source archives.

## 3. Confirm the Zenodo archive and DOI

1. Open <https://zenodo.org/uploads>. The list should show an archive generated
   from `orangewk/wigner-splat`; it can take several minutes after publication.
2. Open the record and confirm title, authorship, version `v0.1.0`, license, and
   repository link.
3. Copy the **version DOI** (the exact v0.1.0 citation) and **concept DOI**
   (the latest-version landing page) into Issue #20.

Published Zenodo files are immutable. If a file needs correction, create a new
version instead of editing the published record.

## 4. Follow-up after DOI issuance

Open a small follow-up PR that adds the version DOI and release date to
`CITATION.cff`, a Zenodo DOI badge to `README.md`, and labels the concept DOI as
a moving latest-version link. Cite the version DOI for v0.1.0.

## References

- [Zenodo: GitHub and software](https://help.zenodo.org/docs/github/)
- [Zenodo: archive a GitHub release](https://help.zenodo.org/docs/github/archive-software/github-upload/)
- [Zenodo: DOI](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/)
