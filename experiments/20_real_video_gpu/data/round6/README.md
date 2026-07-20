# Round 6 public data

Issue #48 Round 6 (hard lock: issue comment 5017827938) reuses the official
Tanks and Temples Truck and Train archives pinned in Round 5 — same bytes,
same SHA-256, same download instructions. See
`experiments/20_real_video_gpu/data/round5/README.md` for the dataset
attribution, citation, and the recorded license status (the official license
page is internally inconsistent; both readings are recorded there without
being resolved). Image payloads are not committed to this repository.

The only change from Round 5 is the frame selection. Round 5's global stride
left the 24 selected frames too far apart for complete SfM registration and
ended in a DNF. Round 6 selects a centrally fixed contiguous block so that
adjacent-frame overlap is structurally guaranteed:

    start = floor((total_source_frames - 24) / 2)
    source_index = start + position   for positions 0 through 23

- Truck (251 frames): start 113, source indices 113-136
- Train (301 frames): start 138, source indices 138-161

The start index is fixed by the formula above; the window is never moved or
tuned, even if SfM fails (that outcome is a DNF, not a search). Positions
4, 10, 16, and 22 go to heldout-sealed; only the other 20 may be enumerated
by COLMAP or training before the fit hard stop. Sealing means pipeline
non-access, not secrecy.

## Reproduction

    python experiments/20_real_video_gpu/download_round5_data.py \
      --scene Truck --destination C:/path/to/tnt
    python experiments/20_real_video_gpu/download_round5_data.py \
      --scene Train --destination C:/path/to/tnt
    python experiments/20_real_video_gpu/prepare_round6_data.py \
      --scene Truck --archive C:/path/to/tnt/Truck.zip
    python experiments/20_real_video_gpu/prepare_round6_data.py \
      --scene Train --archive C:/path/to/tnt/Train.zip

The per-scene manifest.json files written here are the source of truth for
archive identity, selection, frame hashes, and split membership. Image
payloads remain untracked.
