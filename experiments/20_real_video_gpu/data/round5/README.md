# Round 5 public data

Issue #48 Round 5 uses the official Tanks and Temples image sets for Truck
and Train.

- Authors: Arno Knapitsch, Jaesik Park, Qian-Yi Zhou, Vladlen Koltun
- Dataset page: https://www.tanksandtemples.org/download/
- License page: https://www.tanksandtemples.org/license/
- Copyright section: CC BY 4.0
- Additional terms on the same official page: the License Grant section limits
  use to non-commercial scientific research and prohibits reproducing,
  modifying, or making the Data available to third parties without prior
  written permission
- Citation: *Tanks and Temples: Benchmarking Large-Scale Scene
  Reconstruction*, ACM Transactions on Graphics 36(4), 2017.

The Copyright and License Grant sections on the official terms page conflict.
This provenance record preserves both statements, refers users to the official
terms, and does not attempt to resolve the inconsistency. This experiment is
non-commercial scientific research, and image payloads remain untracked.

## Reproduction

Download and verify each pinned archive:

    python experiments/20_real_video_gpu/download_round5_data.py \
      --scene Truck --destination C:/path/to/tnt
    python experiments/20_real_video_gpu/download_round5_data.py \
      --scene Train --destination C:/path/to/tnt

Prepare the hard-locked 24-frame splits:

    python experiments/20_real_video_gpu/prepare_round5_data.py \
      --scene Truck --archive C:/path/to/tnt/Truck.zip
    python experiments/20_real_video_gpu/prepare_round5_data.py \
      --scene Train --archive C:/path/to/tnt/Train.zip

The script preserves the native 1920x1080 JPEG bytes. For a source sequence of
N frames, selected source index is position * floor(N / 24) for positions
0 through 23. Positions 4, 10, 16, and 22 go to heldout-sealed; only the other
20 may be enumerated by COLMAP or training before the fit hard stop. Because the
source is public, sealing means pipeline non-access, not secrecy.

The committed per-scene manifest.json files are the source of truth for archive
identity, selection, frame hashes, and split membership. Image payloads remain
untracked.
