from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session
from db.db import engine, get_db
from schemas import tables
from schemas.models import DBItemBase ,DBItem
from schemas.tables import DBItemsTable
from fastapi.middleware.cors import CORSMiddleware

# Creating an instance of FastAPI
app = FastAPI()

# DB dependency injection
db_dependency = Annotated[Session, Depends(get_db)]

# Creating tables
tables.Base.metadata.create_all(bind=engine)

# Adding origins that can access this backend
origins = [
    "http://localhost:5173" # Change this with http://localhost:5173 - for local testing
]

# Adding middleware that enables communication between backend and frontend
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

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
async def get_task(db: db_dependency, task_id: int):
    task = db.query(DBItemsTable).get(task_id)
    if task:
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found!")

# PUT Route - for updating one task
@app.put("/tasks/{task_id}/", response_model=DBItem)
async def update_task(db: db_dependency, task_id: int, task_update: DBItemBase):
    task = db.query(DBItemsTable).filter(DBItemsTable.id == task_id).one_or_none() # Getting the task item from table
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    
    update_task = task_update.model_dump(exclude_unset=True) # Extracting field and values
    for field, value in update_task.items():
        setattr(task, field, value) # Updating items in the task

    db.commit()
    db.refresh(task)

    return task

@app.delete("/tasks/{task_id}/", response_model=DBItem)
async def delete_task(db: db_dependency, task_id: int):
    task = db.query(DBItemsTable).filter(DBItemsTable.id == task_id).one_or_none() # Getting the task item from table to be deleted
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    
    db.delete(task) # Deleting the task
    db.commit()

    return task


# To run with "python main.py" command
# Preferred to run with "fastapi dev main.py" -- requires "fastapi[standard]" module
if __name__ == ("__main__"):
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port="8000")