from router import route
from specialists import specialist

def classification(goal: str) -> str:
    classify = route(goal)
    if classify.category == "unclear" or classify.confidence < 0.7:
        return 'ask a clarifying question'

    else:
        return specialist[classify.category](goal)


print(classification("Fix my Python IndexError"))