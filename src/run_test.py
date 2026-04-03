import json
import os
import platform
import subprocess
from datetime import datetime

from show_results import print_results_table
from chemicals_db import list_chemicals_files, load_chemicals

_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(_ROOT_DIR, "tests")


def run_test():
    tests = sorted([
        d for d in os.listdir(TESTS_DIR)
        if os.path.isdir(os.path.join(TESTS_DIR, d))
        and os.path.exists(os.path.join(TESTS_DIR, d, "test.json"))
    ])

    if not tests:
        print("No tests found in tests/")
        return

    print("Available tests:")
    for i, name in enumerate(tests, 1):
        print(f"  {i}. {name}")

    while True:
        choice = input("\nSelect a test number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(tests):
            break
        print(f"Please enter a number between 1 and {len(tests)}.")

    test_dir = os.path.join(TESTS_DIR, tests[int(choice) - 1])

    with open(os.path.join(test_dir, "test.json")) as f:
        test_answers = json.load(f)

    images = list(test_answers.keys())
    results = {}

    for i, filename in enumerate(images, 1):
        filepath = os.path.abspath(os.path.join(test_dir, filename))
        if platform.system() == "Windows":
            os.startfile(filepath)
        elif platform.system() == "Darwin":
            subprocess.run(["open", filepath])
        else:
            subprocess.run(["xdg-open", filepath])

        print(f"\nImage {i}/{len(images)}: {filename}")
        while True:
            answer = input("Enter the number of the correct chemical (1-10): ").strip()
            if answer.isdigit() and 1 <= int(answer) <= 10:
                break
            print("Please enter a number between 1 and 10.")

        given = int(answer)
        correct = test_answers[filename]
        results[filename] = {"correct": correct, "given": given}
        print("Correct!" if given == correct else f"Wrong. The answer was {correct}.")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M")
    results_file = os.path.join(test_dir, f"results_{timestamp}.json")
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)

    chemicals = load_chemicals(list_chemicals_files())
    print_results_table(results, chemicals)
    print(f"\n  Results saved to {results_file}")


