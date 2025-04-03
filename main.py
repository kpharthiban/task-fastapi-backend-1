from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session
from db.db import engine, get_db
from schemas import tables
from schemas.models import DBItemBase ,DBItem
from schemas.tables import DBItemsTable

# Creating an instance of FastAPI
app = FastAPI()

# DB dependency injection
db_dependency = Annotated[Session, Depends(get_db)]

# Creating tables
tables.Base.metadata.create_all(bind=engine)

# Routes
# GET Route - for all tasks
@app.get("/tasks/", response_model=List[DBItem])
async def get_tasks(db: db_dependency, skip: int = 0):
    tasks = db.query(DBItemsTable).offset(skip).all()
    return tasks

# POST Route - to create a task
@app.post("/tasks/", response_model=DBItem)
async def post_one_task(item: DBItemBase, db: db_dependency):
    db_task = tables.DBItemsTable(**item.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# GET Route - for one task
@app.get("/tasks/{task_id}/", response_model=DBItem)
async def get_tasks(db: db_dependency, task_id: int):
    task = db.query(DBItemsTable).get(task_id)
    return task




# To run with "python main.py" command
# Preferred to run with "fastapi dev main.py" -- requires "fastapi[standart]" module
if __name__ == ("__main__"):
    import uvicorn
    uvicorn.run(app, host="localhost", port="8000")