# Round 5 public data

Issue #48 Round 5 uses the official Tanks and Temples image sets for Truck
and Train.

- Authors: Arno Knapitsch, Jaesik Park, Qian-Yi Zhou, Vladlen Koltun
- Dataset page: https://www.tanksandtemples.org/download/
- License page: https://www.tanksandtemples.org/license/
- Citation: *Tanks and Temples: Benchmarking Large-Scale Scene
  Reconstruction*, ACM Transactions on Graphics 36(4), 2017.

License status (the official license page is internally inconsistent, and this
record does not resolve it):

- The Copyright section of the official license page states CC BY 4.0, which is
  the attribution the Round 5 hard lock recorded. This notice is preserved here
  and in the committed manifests.
- The License Grant section of the same official license page additionally
  limits use to non-commercial scientific research and says the Data may not
  be reproduced, modified, or made available in any form to any third party
  without prior written permission.

The authoritative terms are whatever the official license page states; consult
it directly before any reuse. This experiment is non-commercial scientific
research, and image payloads are not committed to this repository.

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
