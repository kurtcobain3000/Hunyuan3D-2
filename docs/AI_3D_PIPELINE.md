# AI 3D Character Pipeline

This repository can act as the code center for a local/cloud 3D generation workflow:

`Reference image -> Hunyuan3D -> mesh/texture -> Maya -> RizomUV -> Substance Painter -> UEFN`

## Hub roles

- **Hugging Face**: model discovery, model files, and public model metadata.
- **Kaggle**: datasets, notebook outputs, and optional cloud execution.
- **GitHub**: versioned code, configuration, scripts, and project history.
- **Local workstation**: final 3D cleanup and game-asset preparation.

## Local setup

Create a Python virtual environment, then install the project requirements plus:

```powershell
python -m pip install --upgrade pip
python -m pip install --upgrade huggingface_hub kagglehub
```

Hugging Face authentication is optional for public resources. If needed, use the
`hf auth login` command rather than putting a token in source code.

Kaggle authentication is only needed for resources that require an account or
private access. `kagglehub` can authenticate using `KAGGLE_API_TOKEN` or its
standard local token configuration.

## Bridge commands

```powershell
python tools/hub_bridge.py hf-info tencent/Hunyuan3D-2
python tools/hub_bridge.py hf-download tencent/Hunyuan3D-2 README.md --out models/hunyuan
python tools/hub_bridge.py kaggle-dataset OWNER/DATASET --out data
```

Do **not** commit `HF_TOKEN`, `KAGGLE_API_TOKEN`, API keys, or downloaded model
weights/datasets unless their licenses and repository policy explicitly permit it.

## Target game workflow

1. Prepare a clean front/three-quarter character reference.
2. Generate the base 3D shape with a suitable image-to-3D model.
3. Generate or refine textures only after the geometry is acceptable.
4. Inspect the mesh in a lightweight viewer before opening Maya.
5. Retopologize in Maya for game use.
6. UV unwrap in RizomUV.
7. Bake and texture in Substance Painter.
8. Export game-ready meshes/textures to UEFN.
9. Keep source references, scripts, settings, and metadata in GitHub; keep large
   generated assets outside Git unless they are intentionally versioned.

## Important

AI-generated meshes are not automatically game-ready. Expect cleanup for topology,
UVs, material organization, scale, pivots, normals, deformation, and performance.
Also check the license of every model and dataset before using generated assets in
a commercial project.
