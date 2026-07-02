import argparse

from graphs.workflow import graph
from output.save import save_json


def main():
    parser = argparse.ArgumentParser(description="Run the AI Writer workflow.")
    parser.add_argument("--save", action="store_true", help="Save workflow output to output/workflow_result.json")
    args = parser.parse_args()

    result = graph.invoke({})

    print(result["selected_topic"])
    print("\nGenerated LinkedIn post on topic:\n")
    print(result["post"])
    print("\nProcess completed.")

    if args.save:
        path = save_json(result, "workflow_result.json")
        print(f"Saved workflow output to {path}")


if __name__ == "__main__":
    main()
    