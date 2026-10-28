import subprocess
import sys


def critic(test_file="test_generated_code.py"):
    try:
        res = subprocess.run(
            [sys.executable, "-m", "pytest", "-v", test_file],
            capture_output=True,
            text=True,
            timeout=10
        )

    except subprocess.TimeoutExpired:
        return {
            "test_status": "execution error",
            "feedback": "Pytest exceeded the 10-second timeout.",
            "return_code": None
        }


    feedback = res.stdout + "\n" + res.stderr

    if res.returncode == 0:
        return {
            "test_status": "passed",
            "feedback": feedback,
            "return_code": res.returncode
        }

    elif res.returncode == 1:
        return {
            "test_status": "failed",
            "feedback": feedback,
            "return_code": res.returncode
        }

    else:
        return {
            "test_status": "execution error",
            "feedback": feedback,
            "return_code": res.returncode
        }


if __name__ == "__main__":
    result = critic()
    print(result["feedback"])