from generator import generator
from critic import critic


#test status = passed -> return the generated code
#test status = failed -> request a revision
#test status = execution error -> handle the execution problem seperately. 

def reflection_loop(spec: str, test_file: str = "test_generated_code.py") -> str | None:
    step = 0
    MAX_STEPS = 3
    next_candidate = generator(spec, previous_code=None, feedback=None)

    while step < MAX_STEPS:
        #writing the generated candidate to the file
        with open("generated_code.py", "w", encoding="utf-8") as file:
            file.write(next_candidate)

        print(f"\nAttempt {step + 1}:")
        print(next_candidate)

        approval = input("Review the code. Type 'run' to test it: ")
        if approval.strip().lower() != "run":
            return None
        
        result = critic(test_file)
        step += 1

        if result["test_status"] == "passed":
            return next_candidate

        elif result["test_status"] == "execution error":
            print("Execution error:", result['feedback'])
            return None

        #request a revision
        elif result['test_status'] == 'failed':
            print("Test feedback: ", result["feedback"])

            if step < MAX_STEPS:
                    revision = generator(spec, next_candidate, result["feedback"])
                    next_candidate = revision

        
        else:
            raise ValueError("Unexpected critic status")

    
    print("Maximum attempts reached. No correct solution found")
    return None




if __name__ == "__main__":
    spec = """
    Write a function called is_palindrome that takes a string
    and returns True if the string reads the same forwards
    and backwards, otherwise False.
    """
    final_code = reflection_loop(
        spec,
        test_file="critic_eval_dataset/tests/test_01_palindrome.py"
    )

    if final_code is not None:
        print("\nFinal validated code:")
        print(final_code)
