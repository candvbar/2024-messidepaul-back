from app.models.goal import Goal
from fastapi import HTTPException
from app.service.goal_service import create_goal

def create_goal_controller(goal: Goal):
    try:
        # Ensure that title and description are not empty
        if not goal.title.strip():
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        
        if not goal.description.strip():
            raise HTTPException(status_code=400, detail="Description cannot be empty")
        
        # Ensure that expected_income is a positive integer
        if goal.expected_income <= 0:
            raise HTTPException(status_code=400, detail="Expected income must be a positive number")
        
        # Call the service function to save the goal
        goal_id = create_goal(goal)
        return {"message": "Goal created successfully", "id": goal_id}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

