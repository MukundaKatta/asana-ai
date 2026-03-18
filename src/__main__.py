"""CLI for asana-ai."""
import sys, json, argparse
from .core import AsanaAi

def main():
    parser = argparse.ArgumentParser(description="Asana — AI Yoga Pose Corrector. Real-time yoga pose correction using computer vision.")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "run", "info"])
    parser.add_argument("--input", "-i", default="")
    args = parser.parse_args()
    instance = AsanaAi()
    if args.command == "status":
        print(json.dumps(instance.get_stats(), indent=2))
    elif args.command == "run":
        print(json.dumps(instance.process(input=args.input or "test"), indent=2, default=str))
    elif args.command == "info":
        print(f"asana-ai v0.1.0 — Asana — AI Yoga Pose Corrector. Real-time yoga pose correction using computer vision.")

if __name__ == "__main__":
    main()
