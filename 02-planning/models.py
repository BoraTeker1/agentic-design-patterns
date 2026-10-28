from dotenv import load_dotenv
from pydantic import BaseModel, Field
from openai import OpenAI
from typing import Literal
from tavily import TavilyClient
import os
import json
from pathlib import Path


load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")
client = OpenAI()
MODEL = "gpt-4o-mini"


class Step(BaseModel):
    id: int
    description: str
    tool: Literal["web_search"] | None
    depends_on: list[int] = Field(default_factory=list)
    status: Literal["pending", "running", "done", "failed"] = Field(default_factory=lambda: "pending")


class Plan(BaseModel):
    goal: str
    steps: list[Step]


class ExecutionOutcome(BaseModel):
    failed: bool
    result: str


def ensure_final_synthesis(plan: Plan) -> Plan:
    if not plan.steps:
        return plan
    if plan.steps[-1].tool is not None:
        plan.steps.append(Step(
            id=max(step.id for step in plan.steps) + 1,
            description=f"Answer the original goal using the research findings: {plan.goal}. Cite source URLs.",
            tool=None,
            depends_on=[step.id for step in plan.steps if step.tool == "web_search"],
        ))
    else:
        final_step = plan.steps[-1]
        for step in plan.steps[:-1]:
            if step.tool == "web_search" and step.id not in final_step.depends_on:
                final_step.depends_on.append(step.id)
    return plan


def planner(goal: str) -> Plan:
    response = client.responses.parse(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": """You are a planning agent. Break the user's goal into 3-6 actionable web_search steps, followed by one final synthesis step. Preserve the original goal and its constraints.

                Available tools:
                - web_search: For researching information.
                - None: For the final synthesis using existing findings.

                Each step must:
                - have a unique integer ID.
                - have a clear, actionable description.
                - specify either "web_search" or None as its tool.
                - reference earlier step IDs in depends_on when necessary.
                - start with status "pending".

                Planning rules:
                - Create 3-6 distinct steps with tool="web_search".
                - Avoid unnecessary searches and repeated research.
                - Ensure dependencies reference valid earlier steps.
                - Preserve the context and constraints of the original goal.
                - Make the last step synthesize the findings into an answer that directly addresses the goal.
                - Require the final synthesis to cite supporting source URLs found in search results.
                - The last step must use tool=None and depend on all search steps needed for synthesis.

                Do not execute the steps or perform the research yourself.
                Return only a structured Plan object.
                """
            },
            {
                "role": "user",
                "content": goal
            },
        ],
        text_format=Plan
    )

    research_plan = response.output_parsed

    if research_plan is None:
        raise RuntimeError(
            f"Planner returned no parsed plan. "
            f"Status: {response.status}, "
            f"Details: {response.incomplete_details}"
        )

    return ensure_final_synthesis(research_plan)


def executor(step: Step, ctx, is_final=False):
    try:
        if step.tool == "web_search":
            tavily_client = TavilyClient(api_key=api_key)
            response = tavily_client.search(query=step.description)

            search_results = response.get("results", [])
            if not search_results or not any(item.get("url") for item in search_results):
                return ExecutionOutcome(failed=True, result=f"No citable results for: {step.description}")

            result = json.dumps([
                {
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "content": item.get("content")
                }
                for item in search_results
            ])

        elif step.tool is None:
            response = client.responses.create(
                model=MODEL,
                input=f"""
                Task: {step.description}

                Previous research findings:
                {ctx}

                Complete the task using only the provided findings.
                Cite the exact source URLs next to the claims they support; do not invent citations.
                """
            )

            result = response.output_text
            if not result.strip():
                return ExecutionOutcome(failed=True, result="Synthesis returned no text")

            if is_final:
                source_urls = set()
                for saved_result in execution_results.values():
                    try:
                        items = json.loads(saved_result)
                    except (ValueError, TypeError):
                        continue
                    if isinstance(items, list):
                        source_urls.update(item["url"] for item in items if isinstance(item, dict) and item.get("url"))
                if not source_urls or not any(url in result for url in source_urls):
                    return ExecutionOutcome(failed=True, result="Final summary does not cite a retrieved source URL")

        return ExecutionOutcome(
            failed=False,
            result=result
        )

    except Exception as e:
        return ExecutionOutcome(
            failed=True,
            result=str(e)
        )


execution_results = {}


def save(step_id, result):
    execution_results[step_id] = result


def save_plan_json(plan: Plan, filename="plan.json"):
    Path(filename).write_text(plan.model_dump_json(indent=2), encoding="utf-8")


def results_for(depends_on):
    res_dict = {}

    for step_id in depends_on:
        if step_id in execution_results:
            res_dict[step_id] = execution_results[step_id]

    return res_dict


def replanner(
    goal: str,
    plan: Plan,
    outcome: ExecutionOutcome,
) -> Plan:
    replanner_system_prompt = """
        You are a re-planning agent.
        Your job is to revise an existing research plan after an execution failure.

        Preserve the user's original goal.

        Recovery Rules:
        - Preserve successfully completed steps, their IDs, statuses, and descriptions exactly. Do not execute them again.
        - Use the failure information to determine whether a failed step should be retried or replaced.
        - Revise unfinished steps when necessary to recover from the failure.
        - Ensure dependencies reference valid earlier step IDs.
        - Update downstream dependencies if any step IDs change.
        - Keep the final step focused on synthesizing the research findings. It must use tool=None.
        - Avoid unnecessary steps or repeated research.
        - Every unfinished or retried step must have status="pending".
        - Only previously completed steps may have status="done".
        - Never return steps with status="failed" or "running".

        Return a structured Plan object.
    """

    user_message = f"""
                    Original goal:
                    {goal},

                    Current plan:
                    {plan.model_dump_json(indent=2)}

                    Failure information:
                    {outcome.model_dump_json(indent=2)}

                    Research findings:
                    {json.dumps(execution_results, indent=2)}
                """

    response = client.responses.parse(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": replanner_system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        text_format=Plan
    )

    replan = response.output_parsed

    if replan is None:
        raise RuntimeError("replanner returned no parsed plan")

    return ensure_final_synthesis(replan)


goal = "Compare MongoDB and PostgreSQL for an early-stage startup."

TEST_MODE = False

if TEST_MODE:
    plan = Plan(
        goal=goal,
        steps=[
            Step(
                id=1,
                description="Research MongoDB",
                tool="web_search",
                depends_on=[]
            ),
            Step(
                id=2,
                description="Research PostgreSQL",
                tool="web_search",
                depends_on=[]
            ),
            Step(
                id=3,
                description="Research MongoDB vs PostgreSQL scalability and operational trade-offs",
                tool="web_search",
                depends_on=[]
            ),
            Step(
                id=4,
                description="Compare MongoDB and PostgreSQL for an early-stage startup. Provide a recommendation and cite source URLs.",
                tool=None,
                depends_on=[1, 2, 3]
            )
        ]
    )
else:
    plan = planner(goal)

if not plan.steps:
    raise ValueError("Planner returned an empty plan")

if plan.steps[-1].tool is not None:
    raise ValueError("Final step must use tool=None")

if not 3 <= sum(step.tool == "web_search" for step in plan.steps) <= 6:
    raise ValueError("Plan must contain 3-6 web_search steps")

execution_results.clear()
save_plan_json(plan)

MAX_REPLANS = 2
replan_count = 0

while True:
    failed_outcome = None
    steps_by_id = {}

    for step in plan.steps:
        if step.id in steps_by_id:
            raise ValueError("Duplicate step ID")

        for dep_id in step.depends_on:
            if dep_id not in steps_by_id:
                raise ValueError(
                    f"Invalid dependency {dep_id} in Step {step.id}"
                )

        steps_by_id[step.id] = step

    for step in plan.steps:
        print(f"Checking Step {step.id}: {step.status}")
        if step.status == "done":
            if step.id not in execution_results:
                raise ValueError("Completed step has no saved result")

            print(f"Skipping completed Step {step.id}")
            continue

        if step.status != "pending":
            raise ValueError(
                f"Step {step.id} is not ready: {step.status}"
            )

        for dep_id in step.depends_on:
            if steps_by_id[dep_id].status != "done":
                raise RuntimeError(
                    f"Dependency {dep_id} is not completed"
                )

        ctx = results_for(step.depends_on)

        step.status = "running"
        save_plan_json(plan)
        print(f"\nRunning Step {step.id}: {step.description}")

        if TEST_MODE and step.id == 2 and replan_count == 0:
            outcome = ExecutionOutcome(
                failed=True,
                result="Simulated Tavily connection error"
            )
        else:
            outcome = executor(step, ctx, is_final=(step is plan.steps[-1]))

        if outcome.failed:
            step.status = "failed"
            save_plan_json(plan)
            failed_outcome = outcome

            print(f"Step {step.id} failed: {outcome.result}")
            break

        step.status = "done"
        save(step.id, outcome.result)
        save_plan_json(plan)

        print(f"Step {step.id} completed!")

    if failed_outcome is None:
        for step in plan.steps:
            if step.status != "done":
                raise RuntimeError("Plan has unfinished steps")

        print("\nPlan completed successfully!")
        break

    if replan_count >= MAX_REPLANS:
        raise RuntimeError("Maximum re-planning attempts reached; plan.json contains the failed plan")

    revised_plan = replanner(goal, plan, failed_outcome)

    print("\nRevised plan before validation:")
    print(revised_plan.model_dump_json(indent=2))

    for step in revised_plan.steps:
        if step.status != "done":
            step.status = "pending"

    if revised_plan.goal != goal:
        raise ValueError("Re-planner changed the original goal")

    if not revised_plan.steps:
        raise ValueError("Re-planner returned an empty plan")

    if revised_plan.steps[-1].tool is not None:
        raise ValueError("Final step must use tool=None")

    if not 3 <= sum(step.tool == "web_search" for step in revised_plan.steps) <= 6:
        raise ValueError("Revised plan must contain 3-6 web_search steps")

    revised_steps = {}

    for step in revised_plan.steps:
        if step.id in revised_steps:
            raise ValueError("Duplicate step ID in revised plan")

        for dep_id in step.depends_on:
            if dep_id not in revised_steps:
                raise ValueError("Invalid dependency in revised plan")

        if step.status not in ("pending", "done"):
            raise ValueError(
                f"Step {step.id} has invalid status: {step.status}"
            )

        if step.status == "done" and step.id not in execution_results:
            raise ValueError("Completed step has no saved result")

        revised_steps[step.id] = step

    for old_step in plan.steps:
        if old_step.status == "done":
            if old_step.id not in revised_steps:
                raise ValueError("Completed step was removed")

            if revised_steps[old_step.id] != old_step:
                raise ValueError("Completed step was modified")

    plan = revised_plan
    save_plan_json(plan)
    replan_count += 1

    print(f"\nRe-planning attempt {replan_count}")

    continue


print("\nFinal plan statuses:")

for step in plan.steps:
    print(f"Step {step.id}: {step.status}")

if all(step.status == "done" for step in plan.steps):
    print("\nFinal research result:")
    print(execution_results[plan.steps[-1].id])
