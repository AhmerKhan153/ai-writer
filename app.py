import argparse
import sys
from pathlib import Path

from src.integrations.openclaw import check_gateway_status

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from graphs.workflow import graph
from shared.save import save_json


def main():
    check_gateway_status()
    # parser = argparse.ArgumentParser(description="Run the AI Writer workflow.")
    # parser.add_argument("--save", action="store_true", help="Save workflow output to output/workflow_result.json")
    # args = parser.parse_args()

    # result = graph.invoke({"provider": "hackernews"})

    # print(result.get("selected_story"))
    # print("\nGenerated LinkedIn post on topic:\n")
    # print(result.get("published") or result.get("post"))
    # print("\nProcess completed.")

    # if args.save:
    #     path = save_json(result, "workflow_result.json")
    #     print(f"Saved workflow output to {path}")


if __name__ == "__main__":
    main()
    