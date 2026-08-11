"""Free-cloud-only TRELLIS.2 bridge.

This script runs on a GitHub-hosted runner and calls the Hugging Face
TRELLIS.2 Space API. It never loads a 3D model or uses the local machine GPU.

The Hugging Face token is read only from HF_TOKEN. No token is written to
files or logs.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

SPACE = "microsoft/TRELLIS.2"


def require_token() -> str:
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN GitHub secret is missing.")
    return token


def generate(args: argparse.Namespace) -> None:
    token = require_token()
    image_path = Path(args.image).resolve()
    if not image_path.is_file():
        raise SystemExit(f"Input image not found: {image_path}")

    from gradio_client import Client, handle_file

    print(f"Connecting to Hugging Face Space: {SPACE}")
    print("CLOUD-ONLY MODE: no local AI/GPU inference is performed.")
    client = Client(SPACE, token=token)

    # TRELLIS.2's current public Space exposes these inputs for /image_to_3d.
    # We deliberately use the lower 512 preset for the first automated test.
    image_to_3d = client.submit(
        handle_file(str(image_path)),
        int(args.seed),
        args.resolution,
        7.5, 0.7, 12, 5.0,
        7.5, 0.5, 12, 3.0,
        1.0, 0.0, 12, 3.0,
        api_name="/image_to_3d",
    )

    print("Waiting for cloud generation...")
    state, _preview = image_to_3d.result()

    # GLB extraction is a second cloud-GPU operation in the Space.
    print("Requesting cloud GLB extraction...")
    glb_job = client.submit(
        state,
        int(args.decimation),
        int(args.texture_size),
        api_name="/extract_glb",
    )
    glb_path, _download_path = glb_job.result()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(Path(glb_path).read_bytes())
    print(f"Cloud-generated GLB saved to: {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Free-cloud TRELLIS.2 generator")
    parser.add_argument("--image", required=True)
    parser.add_argument("--output", default="artifacts/character.glb")
    parser.add_argument("--resolution", choices=["512", "1024", "1536"], default="512")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--decimation", type=int, default=200000)
    parser.add_argument("--texture-size", type=int, default=2048)
    args = parser.parse_args()
    generate(args)


if __name__ == "__main__":
    main()
