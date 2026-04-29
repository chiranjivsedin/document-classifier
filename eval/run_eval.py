"""
Benchmark harness for the document classifier.

Usage (server must be running):
    cd backend
    uv run python ../eval/run_eval.py [--api http://localhost:8000] [--dataset ../eval/datasets/samples.jsonl]

Results are saved to eval/results/YYYY-MM-DD-HH-MM.json and printed to stdout.
"""

import argparse
import json
import mimetypes
import sys
from datetime import datetime
from pathlib import Path

import httpx


def _content_type(path: Path) -> str:
    ct, _ = mimetypes.guess_type(str(path))
    return ct or "application/octet-stream"


def _classify(client: httpx.Client, api: str, file_path: Path) -> dict:
    with file_path.open("rb") as f:
        response = client.post(
            f"{api}/classify",
            files={"file": (file_path.name, f, _content_type(file_path))},
            timeout=60,
        )
    response.raise_for_status()
    return response.json()


def run(api: str, dataset_path: Path, results_dir: Path) -> None:
    samples = [json.loads(l) for l in dataset_path.read_text().splitlines() if l.strip()]
    base_dir = dataset_path.parent

    results = []
    correct = 0

    print(f"\nRunning eval against {api}  ({len(samples)} samples)\n")
    print(f"{'FILE':<35} {'EXPECTED':<12} {'PREDICTED':<12} {'CONF':>6}  {'OK'}")
    print("-" * 80)

    with httpx.Client() as client:
        for sample in samples:
            file_path = base_dir / sample["file"]
            expected = sample["expected_class"]

            try:
                result = _classify(client, api, file_path)
            except Exception as exc:
                print(f"  ERROR {file_path.name}: {exc}")
                results.append({**sample, "error": str(exc), "correct": False})
                continue

            predicted = result["predicted_class"]
            confidence = result["confidence"]
            ok = predicted == expected
            if ok:
                correct += 1

            marker = "✓" if ok else "✗"
            print(
                f"{file_path.name:<35} {expected:<12} {predicted:<12} {confidence:>6.2f}  {marker}"
            )
            results.append({
                **sample,
                "predicted_class": predicted,
                "confidence": confidence,
                "reason": result.get("reason", ""),
                "route": result.get("route", ""),
                "ocr_used": result.get("ocr_used", False),
                "correct": ok,
            })

    accuracy = correct / len(samples) if samples else 0.0
    print("-" * 80)
    print(f"\nAccuracy: {correct}/{len(samples)} = {accuracy:.0%}\n")

    # per-class breakdown
    categories = sorted({s["expected_class"] for s in samples})
    print(f"{'CATEGORY':<15} {'CORRECT':<10} {'TOTAL':<10} {'ACC'}")
    print("-" * 45)
    for cat in categories:
        cat_samples = [r for r in results if r.get("expected_class") == cat]
        cat_correct = sum(1 for r in cat_samples if r.get("correct"))
        cat_acc = cat_correct / len(cat_samples) if cat_samples else 0.0
        print(f"{cat:<15} {cat_correct:<10} {len(cat_samples):<10} {cat_acc:.0%}")

    # save
    results_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    out_path = results_dir / f"{timestamp}.json"
    out_path.write_text(json.dumps({
        "timestamp": timestamp,
        "api": api,
        "dataset": str(dataset_path),
        "accuracy": accuracy,
        "correct": correct,
        "total": len(samples),
        "samples": results,
    }, indent=2))
    print(f"\nResults saved to {out_path}")


def main() -> None:
    here = Path(__file__).parent
    parser = argparse.ArgumentParser(description="Evaluate document classifier accuracy.")
    parser.add_argument("--api", default="http://localhost:8000", help="API base URL")
    parser.add_argument(
        "--dataset",
        default=str(here / "datasets" / "samples.jsonl"),
        help="Path to samples.jsonl",
    )
    parser.add_argument(
        "--results-dir",
        default=str(here / "results"),
        help="Directory to write result JSON files",
    )
    args = parser.parse_args()

    run(
        api=args.api,
        dataset_path=Path(args.dataset),
        results_dir=Path(args.results_dir),
    )


if __name__ == "__main__":
    main()
