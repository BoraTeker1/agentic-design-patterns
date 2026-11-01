from pydantic import BaseModel, Field
from typing import Literal



#I am defining what a valid routing decision looks like

class Router(BaseModel):
    #forcing the router to only return the categories that are explicitly given. 
    category: Literal["coding", "research", "support", "unclear"]
    confidence: float = Field(ge=0, le=1.0)
    #extracted: dict = Field(default_factory=dict)


#r1 = Router(category="coding", confidence=0.9)
#r3 = Router(category="finance", confidence=0.8)
#r2 = Router(category="coding", confidence=1.5)

