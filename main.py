import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from create_test import create_test
from fetch_chemicals import fetch_chemicals
from run_test import run_test
from show_results import show_results

while True:
    print("\n1. Fetch chemicals")
    print("2. Create test")
    print("3. Run test")
    print("4. Show results")
    print("5. Exit")

    choice = input("\nSelect an option: ").strip()

    if choice == "1":
        fetch_chemicals()
    elif choice == "2":
        create_test()
    elif choice == "3":
        run_test()
    elif choice == "4":
        show_results()
    elif choice == "5":
        break
    else:
        print("Invalid option.")
