from pathlib import Path

import reflection
from generator import generator as real_generator
from critic import critic as real_critic

counts = {"generator": 0, "critic": 0}


def controlled_generator(spec, previous_code=None, feedback=None):
    counts["generator"] += 1
    print(f"\n[TEST] Generating intentionally wrong candidate {counts['generator']}.")


    return "def is_palindrome(s):\n    return s != s[::-1]\n"


def counting_critic(test_file="test_generated_code.py"):
    counts["critic"] += 1
    return real_critic(test_file)


if __name__ == "__main__":
    spec = """
    Write a function called is_palindrome that takes a string
    and returns True if the string reads the same forwards
    and backwards, otherwise False.
    """

    code_file = Path(__file__).with_name("generated_code.py")

    original_code = code_file.read_text(encoding="utf-8") if code_file.exists() else None

    try:
        reflection.generator = controlled_generator
        reflection.critic = counting_critic

       
        final_code = reflection.reflection_loop(spec)

        print("\n--- CONTROLLED TEST RESULTS ---")
        print("Generator calls:", counts["generator"])
        print("Critic calls:", counts["critic"])

        if final_code is None and counts["generator"] == 3 and counts["critic"] == 3:
            print("PASS: Stopped after three failed attempts without returning code.")
        else:
            print("FAIL: The reflection loop did not behave as expected.")

    finally:
        reflection.generator = real_generator
        reflection.critic = real_critic

        if original_code is None:
            code_file.unlink(missing_ok=True)
        else:
            code_file.write_text(original_code, encoding="utf-8")