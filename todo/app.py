import uvicorn

from fastapi import FastAPI, HTTPException
from pymongo import ReturnDocument
from bson import ObjectId

from .database import todo_collection
from .models import LocationTask, TodoStatus

app = FastAPI(
    title="LyteForge Todo App"
)

@app.get(
    "/location",
    description="Gets all tasks near location at given lat, long",
    tags=["location"]
)
def get_tasks_at_location(lat: float, long: float, search: str = ""):
    query_point = {"type": "Point", "coordinates": [long, lat]}
    geo_results = todo_collection.aggregate([
        {
            "$geoNear": {
                "near": query_point,
                "distanceField": "distance",
                "spherical": True,
                "maxDistance": 5000 # in meters
            }
        },
    ]).to_list()

    results = geo_results

    # get the intersection of the results if we need to search for text too
    # this allows us to take advantage of both indexes
    if search != "":
        text_results = todo_collection.aggregate([
            {
                "$match": {
                    "$text": { "$search": search }
                }
            }
        ]).to_list()
        text_result_ids = set([str(x["_id"]) for x in text_results])
        geo_result_ids = set([str(x["_id"]) for x in geo_results])
        id_intersection = text_result_ids.intersection(geo_result_ids)

        results = [x for x in text_results if str(x["_id"]) in id_intersection]

    for result in results:
        result["_id"] = str(result["_id"])

    return results  #TODO: Return list of LocationTask Pydantic models

@app.post(
    "/location",
    description="Create a location with a task",
    tags=["location"]
)
def create_task(location_task: dict): # TODO: Use LocationTask Pydantic model
    result = todo_collection.insert_one(location_task)
    inserted_task = todo_collection.find_one({"_id": result.inserted_id})
    if not inserted_task:
        raise HTTPException(status_code=500, detail="Failed to retrieve inserted task")

    inserted_task["_id"] = str(inserted_task["_id"])
    return inserted_task


@app.put(
    "/location/{task_id}",
    description="Update a location task",
    tags=["location"]
)
def update_task(task_id: str, status: TodoStatus): # TODO: Use LocationTask Pydantic model
    updated_task = todo_collection.find_one_and_update(
        { "_id": ObjectId(task_id) },
        { "$set": { "status": status.value } },
        return_document=ReturnDocument.AFTER
    )
    if not updated_task:
        raise HTTPException(status_code=500, detail="Failed to update task")

    updated_task["_id"] = str(updated_task["_id"])
    return updated_task


@app.delete(
    "/location/{task_id}",
    description="Delete a location task",
    tags=["location"]
)
def delete_task(task_id: str):
    todo_collection.delete_one({"_id": ObjectId(task_id)})


def run():
    uvicorn.run(
        app,
        host="127.0.0.1",
        port="80",
    )
