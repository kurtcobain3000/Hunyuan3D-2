"""Small bridge for the Hunyuan3D workflow.

Uses public Hugging Face resources without credentials and KaggleHub for
Kaggle datasets/models/notebook outputs. Secrets are read from the environment
and are never written to the repository.

Examples:
  python tools/hub_bridge.py hf-info tencent/Hunyuan3D-2
  python tools/hub_bridge.py hf-download tencent/Hunyuan3D-2 README.md --out models/hunyuan
  python tools/hub_bridge.py kaggle-dataset <owner/dataset> --out data
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path


def hf_api():
    from huggingface_hub import HfApi
    return HfApi(token=os.getenv("HF_TOKEN") or None)


def hf_info(repo_id: str) -> None:
    info = hf_api().model_info(repo_id)
    print(f"repo: {info.id}")
    print(f"pipeline: {getattr(info, 'pipeline_tag', None)}")
    print(f"license: {(info.card_data or {}).get('license') if info.card_data else None}")
    print(f"downloads: {getattr(info, 'downloads', None)}")


def hf_download(repo_id: str, filename: str, output_dir: str) -> None:
    from huggingface_hub import hf_hub_download

    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir=str(target),
    )
    print(path)


def kaggle_dataset(handle: str, output_dir: str) -> None:
    import kagglehub

    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    path = kagglehub.dataset_download(handle, output_dir=str(target))
    print(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Hugging Face + Kaggle bridge")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("hf-info")
    p.add_argument("repo_id")

    p = sub.add_parser("hf-download")
    p.add_argument("repo_id")
    p.add_argument("filename")
    p.add_argument("--out", default="models")

    p = sub.add_parser("kaggle-dataset")
    p.add_argument("handle")
    p.add_argument("--out", default="data")

    args = parser.parse_args()
    if args.command == "hf-info":
        hf_info(args.repo_id)
    elif args.command == "hf-download":
        hf_download(args.repo_id, args.filename, args.out)
    elif args.command == "kaggle-dataset":
        kaggle_dataset(args.handle, args.out)


if __name__ == "__main__":
    main()
