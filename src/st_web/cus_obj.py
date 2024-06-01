from langchain_core.pydantic_v1 import BaseModel, Field, validator
from typing import List

class Action(BaseModel):
    """Define the action to be taken by each servo."""
    servo1: int = Field(description="Angle for servo 1, located at the base of the robotic arm, responsible for rotating the arm around the vertical axis.")
    servo2: int = Field(description="Angle for servo 2, located at the shoulder of the robotic arm, responsible for moving the arm up and down.")
    servo3: int = Field(description="Angle for servo 3, located at the elbow of the robotic arm, responsible for extending or retracting the arm.")
    servo4: int = Field(description="Angle for servo 4, located at the wrist of the robotic arm, responsible for rotational movement of the wrist.")
    servo5: int = Field(description="Angle for servo 5, located at the wrist rotation part of the robotic arm, controls the orientation of the end effector.")
    servo6: int = Field(description="Angle for servo 6, located at the end of the robotic arm, controls the operation of the end effector such as a gripper or tool.")

class Task(BaseModel):
    """A task that the robotic arm needs to complete."""
    action: Action = Field(description="Servo angles for the task")
    check_point: str = Field(description="Description of the check point")
    expected_image_description: str = Field(description="Description of what the scene should look like after the action")

class RoboticArmOperation(BaseModel):
    """Overall goal and tasks for the robotic arm operation."""
    goal: str = Field(description="Overall goal of the operation")
    tasks: List[Task] = Field(description="List of tasks to be completed")
