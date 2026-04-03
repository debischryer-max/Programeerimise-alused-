import json
import os

from chemicals_db import list_chemicals_files, load_chemicals

_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(_ROOT_DIR, "tests")


def _results_files(test_dir):
    return sorted([
        f for f in os.listdir(test_dir)
        if f.startswith("results_") and f.endswith(".json")
    ])


def show_results():
    all_results = []
    for test in sorted(os.listdir(TESTS_DIR)):
        test_dir = os.path.join(TESTS_DIR, test)
        if not os.path.isdir(test_dir):
            continue
        for rf in _results_files(test_dir):
            all_results.append((test, rf, os.path.join(test_dir, rf)))

    if not all_results:
        print("No completed tests found in tests/")
        return

    print("Available results:")
    for i, (test, rf, _) in enumerate(all_results, 1):
        print(f"  {i}. {test} / {rf}")

    while True:
        choice = input("\nSelect a result: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(all_results):
            break
        print(f"Please enter a number between 1 and {len(all_results)}.")

    _, _, results_path = all_results[int(choice) - 1]

    with open(results_path) as f:
        results = json.load(f)

    chemicals = load_chemicals(list_chemicals_files())
    print_results_table(results, chemicals)


def print_results_table(results, chemicals):
    rows = []
    correct_count = 0
    for filename, entry in results.items():
        cid = filename.replace(".png", "")
        name = chemicals.get(cid, {}).get("name", f"CID {cid}")
        correct = entry["correct"]
        given = entry["given"]
        is_correct = correct == given
        correct_count += is_correct
        rows.append((name, correct, given, "✓" if is_correct else "✗"))

    col_name = max(len(r[0]) for r in rows)
    header = f"  {'Chemical':<{col_name}}  {'Answer':>6}  {'Given':>5}  Result"
    divider = "  " + "-" * (len(header) - 2)
    print()
    print(header)
    print(divider)
    for name, correct, given, status in rows:
        print(f"  {name:<{col_name}}  {correct:>6}  {given:>5}  {status}")
    print(divider)
    print(f"  Score: {correct_count}/{len(results)} ({correct_count / len(results) * 100:.0f}%)")


