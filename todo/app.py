import uvicorn
from fastapi import FastAPI, HTTPException
from .database import todo_collection
from .models import LocationTask

app = FastAPI(
    title="LyteForge Todo App"
)

@app.get(
    "/location",
    description="Gets all tasks near location at given lat, long",
    tags=["location"]
)
def get_tasks_at_location(lat: float, long: float):
    query_point = {"type": "Point", "coordinates": [long, lat]}
    results = todo_collection.aggregate([
        {
            "$geoNear": {
                "near": query_point,
                "distanceField": "distance",
                "spherical": True,
                "maxDistance": 5000 # in meters
            }
        }
    ])

    results_list = results.to_list()
    for result in results_list:
        result["_id"] = str(result["_id"])

    return results_list

@app.post(
    "/location",
    description="Create a location with a task",
    tags=["location"]
)
def create_task_at_location(location_task: dict): # TODO: Use LocationTask Pydantic model
    result = todo_collection.insert_one(location_task)
    inserted_task = todo_collection.find_one({"_id": result.inserted_id})
    if not inserted_task:
        raise HTTPException(status_code=500, detail="Failed to retrieve inserted task")

    inserted_task["_id"] = str(inserted_task["_id"])
    return inserted_task

def run():
    uvicorn.run(
        app,
        host="127.0.0.1",
        port="80",
    )
