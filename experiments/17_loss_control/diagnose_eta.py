"""Exp17 follow-up: why did the jointly-fitted-eta arm collapse?

The main run's FITTED arm landed at eta = 0.5635 with F = 0.5085 -- worse
than ignoring the noise entirely. Two candidate explanations: (a) start
sensitivity / under-optimization (eta0 = 0.6 was deliberately wrong), or
(b) a genuine identifiability failure at this shot budget. Discriminator,
declared before running: refit the FITTED arm from a near-true start
(eta0 = 0.79) and compare the TRAIN NLLs of every fit against the
known-eta reference. If the near-true starts recover eta ~ 0.8 and the
wrong starts show materially higher NLL, it is (a); if all runs sit on one
NLL plateau while eta and fidelity scatter, it is (b) -- the likelihood is
flat along a (state, eta) direction and cannot identify eta here.
"""
import itertools
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat import bbdagM  # noqa: E402
from wigner_splat.data3 import apply_detection_noise  # noqa: E402
from wigner_splat.states3 import ThreeModeCat  # noqa: E402

ALPHA, PARITY, ETA, EXTRA, SHOTS, DATA_SEED = 1.5, +1, 0.8, 0.02, 1000, 42
GRID = [t for t in itertools.product(
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
)]


def main():
    print("=== exp17 diagnostic: fitted-eta collapse -- start sensitivity "
          "or identifiability? ===")
    target = ThreeModeCat(ALPHA, PARITY)
    ideal = target.sample_homodyne(GRID, SHOTS, rng=DATA_SEED)
    data = apply_detection_noise(ideal, ETA, EXTRA, rng=DATA_SEED + 1000)
    for eta0 in (0.6, 0.79):
        for s in (0, 1, 2):
            st, ef = bbdagM.fit_bbdagM_lossy(
                data, K=2, M=3, eta0=eta0, fit_eta=True,
                extra_noise_var=EXTRA, iters=300, seed=s)
            nll = bbdagM.nll_lossy(st, data, ef, EXTRA)
            F = bbdagM.fidelity_vs_cat3(st, ALPHA, PARITY)
            print(f"  eta0={eta0} seed={s}: eta_fit={ef:.4f} "
                  f"NLL={nll:.5f} F={F:.4f}", flush=True)
    st, _ = bbdagM.fit_bbdagM_lossy(data, K=2, M=3, eta0=ETA, fit_eta=False,
                                    extra_noise_var=EXTRA, iters=300, seed=0)
    print(f"  known eta={ETA} seed=0: "
          f"NLL={bbdagM.nll_lossy(st, data, ETA, EXTRA):.5f} "
          f"F={bbdagM.fidelity_vs_cat3(st, ALPHA, PARITY):.4f}")


if __name__ == "__main__":
    main()
