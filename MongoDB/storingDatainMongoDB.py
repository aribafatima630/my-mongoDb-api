from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv(r"C:\Users\Faizan\Documents\MyAIProjects\MongoDB\.env")

MONGO_URL = os.getenv("MONGO_URL")

client = AsyncIOMotorClient(MONGO_URL)
db = client["my_database"]
data = db["data_coll"]

app = FastAPI()

class myData(BaseModel):
    date : str
    hour : int
    topic : str

def data_helper(docs):
    docs["_id"] = str(docs["_id"])
    return docs

@app.post("/insert/work")
async def insert_workDone(input : myData):
   result = await data.insert_one(input.dict())
   return {
       "Message":"Today's Work Submitted Successfully!",
       "detail" : str(result.inserted_id)
       }

@app.get("/getWork")
async def get_data():
    work = []
    cursor = data.find({})
    async for dt in cursor:
        #dt["_id"] = str(dt["_id"])
        work.append(data_helper(dt))

    return work

@app.delete("/delete/{topic}")
async def delete_work(topic : str):
    result = await data.delete_one({"topic":topic})

    if result.deleted_count==1:
        return {"message":"Data Deleted Success!", "Deleted Topic:": topic}
    else:
        raise HTTPException(status_code=404,detail="Data Not Found")
    
@app.patch("/updateWork/{topic}")
async def update_work(topic : str, input : myData):
    result = await data.update_one(
        {"topic":topic},
        {"$set":input.dict()}
    )

    if result.matched_count==0:
        raise HTTPException(status_code=404,detail="Record Not Found")
    
    return "Record Updated Succesfully"

