
import csv
import json
from pathlib import Path

from generator import generator
from critic import critic


PROJECT_DIR = Path(__file__).resolve().parent
DATASET_DIR = PROJECT_DIR / "critic_eval_dataset"
CODE_FILE = PROJECT_DIR / "generated_code.py"
RESULTS_FILE = PROJECT_DIR / "evaluation_results.csv"

MAX_ATTEMPTS = 3
TASK_LIMIT = 20


def test_candidate(code, test_file, task_id, attempt):
    
    CODE_FILE.write_text(code, encoding="utf-8")

    print(f"\n[{task_id}] Attempt {attempt}")
    print(code)

    approval = input(
        "Review the code. Type 'run' to test it (anything else stops): "
    )

    if approval.strip().lower() != "run":
        raise KeyboardInterrupt("Execution stopped.")

    try:
        compile(code, "generated_code.py", "exec")

    except SyntaxError as error:
        return {
            "test_status": "failed",
            "feedback": f"SyntaxError on line {error.lineno}: {error.msg}\n{error.text or ''}",
            "return_code": None
        }

    return critic(str(test_file))


def evaluate_task(task):
    spec = task["spec"]
    test_file = DATASET_DIR / task["test_file"]

   
    candidate = generator(spec)
    feedback = ""

    baseline_status = None
    final_status = None
    attempts = 0

    for attempt in range(1, MAX_ATTEMPTS + 1):

        if attempt > 1:
            candidate = generator(
                spec,
                previous_code=candidate,
                feedback=feedback
            )

        result = test_candidate(
            candidate, test_file, task["id"], attempt
        )

        attempts = attempt
        final_status = result["test_status"]

       
        if attempt == 1:
            baseline_status = final_status

        print("Test status:", final_status)

        if final_status == "passed":
            break

        elif final_status == "execution error":
            print("Testing error:", result["feedback"])
            break

       
        feedback = result["feedback"]
        print("Tests failed. Feedback will be sent on the next attempt if available.")

    return {
        "id": task["id"],
        "title": task["title"],
        "difficulty": task["difficulty"],
        "baseline_status": baseline_status,
        "reflection_status": final_status,
        "baseline_passed": baseline_status == "passed",
        "reflection_passed": final_status == "passed",
        "attempts": attempts
    }


def save_results(results):
    if not results:
        return

    with RESULTS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=list(results[0].keys())
        )
        writer.writeheader()
        writer.writerows(results)


def main():
    if Path.cwd().resolve() != PROJECT_DIR:
        raise RuntimeError("Run this script from your 03-critic directory.")

   
    with (DATASET_DIR / "specs.json").open(encoding="utf-8") as file:
        tasks = json.load(file)

    if not 1 <= TASK_LIMIT <= len(tasks):
        raise ValueError("Invalid TASK_LIMIT.")

    results = []

 
    original_code = (
        CODE_FILE.read_text(encoding="utf-8")
        if CODE_FILE.exists()
        else None
    )

    try:
        for task in tasks[:TASK_LIMIT]:
            print(f"\n========== {task['id']}: {task['title']} ==========")

            row = evaluate_task(task)
            results.append(row)

         
            save_results(results)

            print("Baseline:", row["baseline_status"])
            print("Reflection:", row["reflection_status"])
            print("Attempts tested:", row["attempts"])

    except KeyboardInterrupt:
        print("\nEvaluation stopped. Completed results were saved.")

    finally:
        if original_code is None:
            CODE_FILE.unlink(missing_ok=True)
        else:
            CODE_FILE.write_text(original_code, encoding="utf-8")

    if results:
        n = len(results)
        baseline_passes = sum(r["baseline_passed"] for r in results)
        reflection_passes = sum(r["reflection_passed"] for r in results)

        baseline_rate = 100 * baseline_passes / n
        reflection_rate = 100 * reflection_passes / n

        print("\n========== EVALUATION SUMMARY ==========")
        print(f"Evaluated tasks: {n}/{len(tasks)}")
        print(f"Baseline pass rate: {baseline_rate:.1f}%")
        print(f"Reflection pass rate: {reflection_rate:.1f}%")
        print(f"Improvement: {reflection_rate - baseline_rate:+.1f} percentage points")
        print(f"Results saved to: {RESULTS_FILE.name}")

        if n < len(tasks):
            print("Partial evaluation: run all 20 tasks for the full experiment.")

        if any(
            r["baseline_status"] == "execution error"
            or r["reflection_status"] == "execution error"
            for r in results
        ):
            print("WARNING: Investigate tasks with execution errors.")


if __name__ == "__main__":
    main()
