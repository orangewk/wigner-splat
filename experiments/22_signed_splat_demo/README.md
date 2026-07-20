# Experiment 22 — signed-splat expression demos

Issue #89 の表現デモ。公開済みの学習済み3D Gaussian sceneに時間変化する
負の寄与を加え、次の3効果を高精細GPU描画する。

1. `eraser`: カメラ側を移動する3D球内でsource splatと同位置の負コピーを相殺し、
   取得済みの背面splatsを露出させる。
2. `dark-flashlight`: 52個の低振幅negative Gaussianからなるビームを走査し、
   投影先のradianceを減算する。
3. `annihilation`: サボテン領域の負コピーを右から接近させ、接触時に正側を相殺する。

これはsigned representationの表現可能性を見せるデモである。物理的な負の光、
既存編集法に対する優越、学習済みモデルの品質改善は主張しない。

## Committed demos

3本とも960×960、12 fps、96 frames、8秒、H.264 yuv420p。

- [Eraser](media/cc0-cactus-eraser.mp4)
- [Dark flashlight](media/cc0-cactus-dark-flashlight.mp4)
- [Annihilation](media/cc0-cactus-annihilation.mp4)

## Public input and provenance

正式デモはsteam studio / 3D SCAN STUDIO iris公開の
[Free Download!! 3D Gaussian Splatting Data (PLY)](https://note.com/steam_studio/n/ne9736d94f162)
を使用する。配布ページは全ファイルをCC0と明記している。

- capture: Nikon Z7II、8256×5504、427 photos
- training/export: Postshot v0.5.250、25k steps
- full PLY: 456,689,798 bytes、1,935,120 splats、SH degree 3
- SHA-256: `0d747af95e3e9d55837a1e3aa6a4ed7dc6222866e0ba8cda928e211f7e8888c1`
- source PLYは456MBのためリポジトリへ含めない
- CC0派生動画3本は小容量なのでPRへ含める

旧ローカル検証で使用した`cakewalk/splat-data/garden.splat`は個別ファイルの
出典・license対応が不明確だったため正式成果物には使わない。自作MOVからの再学習も
行わない。

## High-fidelity GPU run

CUDA版PyTorch、`gsplat`、NumPy、Pillow、PATH上のffmpegが必要。
`gpu_renderer.py`はPostshot/INRIA binary PLYから位置、opacity、異方性scale、
WXYZ quaternion、SH degree-3係数を読み、`gsplat`のantialiased rasterizerへ渡す。
学習処理は含まない。

```powershell
$python = "C:\path\to\cuda-env\Scripts\python.exe"
$scene = "C:\path\to\cactus_splat3_25kSteps_2M_splats.ply"

& $python experiments\22_signed_splat_demo\render_gpu_demo.py `
  --scene $scene --effect eraser `
  --output experiments\22_signed_splat_demo\out\eraser.mp4

& $python experiments\22_signed_splat_demo\render_gpu_demo.py `
  --scene $scene --effect dark-flashlight `
  --output experiments\22_signed_splat_demo\out\dark-flashlight.mp4

& $python experiments\22_signed_splat_demo\render_gpu_demo.py `
  --scene $scene --effect annihilation `
  --output experiments\22_signed_splat_demo\out\annihilation.mp4
```

既定は960×960、12 fps、8秒。単一フレーム確認には拡張子を`.png`にし、
`--preview-progress 0.5`を指定する。出力済みファイルは上書きしない。

## Dependency-light CPU fallback

`render_demo.py`と`signed_renderer.py`は32-byte `.splat`およびgsplat test
`.npz`用のCPU prototypeとして残す。固定screen-space footprintによる近似であり、
Gaussianの異方性scale・quaternion・SHを使わないため、正式な美麗成果物には用いない。

## Prior-work boundary

- NegGS (Kasymov et al., 2024/2025): negative Gaussian自体と再構成用途の先行。
- GaussianEditor (CVPR 2024): text instructionとGaussian RoIによる局所編集。
- Point'n Move (2023): object manipulationと露出領域inpainting。

本デモの差分は学習改善ではなく、時間変化する符号付き表現操作である。

References:

- https://arxiv.org/abs/2405.18163
- https://gaussianeditor.github.io/
- https://arxiv.org/abs/2311.16737
- https://note.com/steam_studio/n/ne9736d94f162
- https://docs.gsplat.studio/
