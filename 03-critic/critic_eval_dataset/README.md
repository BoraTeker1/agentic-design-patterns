# Reflection / Critic — 20-spec evaluation dataset

This dataset implements the **20 specification** benchmark requested in section 2.3 of *Agentic Design Patterns*. It contains 20 standalone, deterministic Python function tasks, each with its own pytest file.

## Contents

- `specs.json`: IDs, titles, difficulty, exact function names and signatures, unambiguous task specifications, and associated test-file paths.
- `tests/test_XX_name.py`: pytest tests for each specification.
- `README.md`: usage notes.

## Using it with your current project

1. Keep this folder within your `03-critic` directory, or point your evaluation runner to its absolute path.
2. Load `specs.json`, select one entry, and pass its `spec` string to `generator()` or `reflection_loop(spec)`.
3. Write the resulting source to `generated_code.py` in the **same working directory used by pytest**.
4. Modify `critic()` so it accepts a `test_file` path, rather than always running `test_generated_code.py`. Select the matching `test_file` from the entry. Only execute **that one** file per specification.
5. Example manual command, run from `03-critic`: `python -m pytest -v critic_eval_dataset/tests/test_01_palindrome.py`.

Your current `reflection_loop(spec)` uses a no-argument `critic()` that always selects the palindrome tests. That must be updated before a valid 20-spec evaluation. Also, the current loop prompts for approval each attempt, so it is **not** an unattended benchmark runner.

## Experimental design for a fair comparison

- For each specification, generate **one initial candidate**. Test that candidate once as the **baseline**.
- Reuse the **same initial candidate** for the reflection condition. Only if it fails, feed test feedback back and allow at most **two more candidate generations**, for **three tested candidates total**.
- This pairing removes noise from comparing two independently sampled initial generations.
- Record each task's baseline status and reflection status separately, plus number of tested attempts. A result counts as a pass only if all tests in that task's selected pytest file pass.
- Report baseline pass rate = (# baseline tasks passing / 20) × 100%; reflection pass rate = (# reflection tasks passing / 20) × 100%; and the percentage-point difference. Do not treat this 20-task set as a statistically strong general benchmark.
- Do not provide the tests to the generator up front; give the specification alone, then provide **failure feedback only on revision attempts**.

## Safety

The tests are static and were validated with reference implementations before packaging. **Model-generated Python is not trusted code**. Do not run it automatically with unsandboxed pytest. Continue reviewing candidate code before executing it, or set up a properly isolated sandbox with resource/time/memory limits before automated evaluation. A subprocess timeout by itself is not sufficient containment.

## Notes

The signatures require Python 3.10+ for union type syntax. Only Python's standard library and pytest are required. Task inputs in tests follow the explicitly documented contracts. These tests check selected cases, not mathematical correctness for every possible input. No test pass rates have been measured for your LLM; the dataset does not claim any model performance.
