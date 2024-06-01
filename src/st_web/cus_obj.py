from langchain_core.pydantic_v1 import BaseModel, Field, validator
from typing import List

class Action(BaseModel):
    """Define the action to be taken by each servo."""
    servo1: int = Field(description="Angle for servo 1")
    servo2: int = Field(description="Angle for servo 2")
    servo3: int = Field(description="Angle for servo 3")
    servo4: int = Field(description="Angle for servo 4")
    servo5: int = Field(description="Angle for servo 5")
    servo6: int = Field(description="Angle for servo 6")

class Task(BaseModel):
    """A task that the robotic arm needs to complete."""
    action: Action = Field(description="Servo angles for the task")
    check_point: str = Field(description="Description of the check point")
    expected_image_description: str = Field(description="Description of what the scene should look like after the action")

class RoboticArmOperation(BaseModel):
    """Overall goal and tasks for the robotic arm operation."""
    goal: str = Field(description="Overall goal of the operation")
    tasks: List[Task] = Field(description="List of tasks to be completed")
