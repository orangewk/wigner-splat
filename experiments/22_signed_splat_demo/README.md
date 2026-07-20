# Experiment 22 — signed-splat expression demos

Issue #89 のデモ／表現線。学習済み 3D Gaussian scene に、時間変化する負の寄与を
後処理で加え、次の3効果を CPU だけで動画化する。

1. `eraser`: 3D 球内の source splat に同位置・同強度の負コピーを重ね、背後の
   計測済み splat を露出させる。
2. `dark-flashlight`: ビーム体積を低振幅の負 Gaussian 群で満たし、投影先から
   radiance を減算する。
3. `annihilation`: 選択領域の負コピーを接近させ、接触時に正負を打ち消す。

これは確認的検証ではなく、signed representation の表現可能性を見せるデモである。
物理的な負の光、既存編集法に対する優越、学習済みモデルの品質改善は主張しない。

## Inputs and redistribution boundary

CLI は gsplat の `test_garden.npz` 形式（`means3d`, `colors`）と、一般的な
32-byte `.splat` 形式を読む。入力 scene はリポジトリに含めない。

`cakewalk/splat-data` は model card で「様々な出典・様々なライセンス」と記す一方、
個別 `.splat` の出典・ライセンス対応表を公開していない。このため、同リポジトリの
ファイルはローカル検証専用とし、再配布可能と扱わない。公開動画にも個別素材の権利を
自動的に推定しない。自作 Scaniverse 素材へ差し替えるのが公開上もっとも明確である。

## Run

追加 Python package は不要。リポジトリの既存 `.venv`（NumPy / Pillow）と
PATH 上の ffmpeg を使う。出力は `out/`（gitignore 対象）へ置き、既存ファイルを
上書きしない。

```powershell
$python = "C:\dev\wigner-splat\.venv\Scripts\python.exe"
$scene = "C:\path\to\scene.splat"

& $python experiments\22_signed_splat_demo\render_demo.py `
  --scene $scene --effect eraser `
  --output experiments\22_signed_splat_demo\out\eraser.mp4

& $python experiments\22_signed_splat_demo\render_demo.py `
  --scene $scene --effect dark-flashlight `
  --output experiments\22_signed_splat_demo\out\dark-flashlight.mp4

& $python experiments\22_signed_splat_demo\render_demo.py `
  --scene $scene --effect annihilation `
  --output experiments\22_signed_splat_demo\out\annihilation.mp4
```

既定は 1296×840、15 fps、8秒。構図は `--yaw` / `--pitch`、大規模 scene の
決定論的間引きは `--max-splats` で調整できる。単一フレーム確認には拡張子を `.png`
にして `--preview-progress 0.5` を指定する。

`cakewalk/splat-data` の `garden.splat` には、同作者の WebGL viewer に収録された
camera 0 を `--camera-preset garden` で使用する。camera の位置・回転・焦点距離は
viewer `main.js` の値を転記しており、scene から推測していない。大きく間引くと
sub-pixel splat が疎になる。今回のローカル代表動画は 2M 点に固定し、実点数を sidecar JSON に記録する。

## Prior work boundary

- NegGS (Kasymov et al., 2024/2025) は負 Gaussian を再構成へ導入し、高周波構造や
  影の表現を改善した先行研究。本デモの「負 Gaussian」自体の先行として引用する。
- GaussianEditor (CVPR 2024) は text instruction と Gaussian RoI による局所編集。
- Point'n Move (2023) は object manipulation と露出領域 inpainting。本デモの
  `eraser` は inpainting せず、取得済み splat だけを露出させる点を区別する。

References:

- https://arxiv.org/abs/2405.18163
- https://gaussianeditor.github.io/
- https://arxiv.org/abs/2311.16737
- https://huggingface.co/cakewalk/splat-data
