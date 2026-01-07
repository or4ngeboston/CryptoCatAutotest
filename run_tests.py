import pytest
import sys

if __name__ == "__main__":
    print("Running Cryptocat Automated Tests...")
    # Pass command line arguments to pytest, or default to verbose and allure reporting
    args = sys.argv[1:] if len(sys.argv) > 1 else ["-v", "--alluredir=allure-results"]
    exit_code = pytest.main(args)
    sys.exit(exit_code)
