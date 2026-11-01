def coding_agent(goal: str) -> str:
    return f'coding specialist handled the request: {goal}'


def research_agent(goal: str) -> str:
    return f'research specialist handled the request: {goal}'


def support_agent(goal: str) -> str:
    return f'support agent handled the request {goal}'


specialist = {
    "coding": coding_agent,
    "research": research_agent,
    "support": support_agent,
}
