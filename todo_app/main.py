from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import TodoItem as TodoItemModel
from datetime import datetime
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items", response_model=List[TodoItem])
def get_items(db: Session = Depends(get_db)):
    items = db.query(TodoItemModel).all()
    return items

@app.get("/items/{item_id}", response_model=TodoItem)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(TodoItemModel).filter(TodoItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=TodoItem)
def create_item(item: TodoCreate, db: Session = Depends(get_db)):
    new_item = TodoItemModel(
        title=item.title,
        description=item.description,
        completed=item.completed
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@app.put("/items/{item_id}", response_model=TodoItem)
def update_item(item_id: int, item: TodoCreate, db: Session = Depends(get_db)):
    db_item = db.query(TodoItemModel).filter(TodoItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.title = item.title
    db_item.description = item.description
    db_item.completed = item.completed
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(TodoItemModel).filter(TodoItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted"}

# Получение всех завершенных задач
@app.get("/completed", response_model=List[TodoItem])
def get_completed_items(db: Session = Depends(get_db)):
    items = db.query(TodoItemModel).filter(TodoItemModel.completed == True).all()
    return items  # Возвращаем пустой список [], если задач нет

# Получение всех незавершенных задач
@app.get("/incomplete", response_model=List[TodoItem])
def get_incomplete_items(db: Session = Depends(get_db)):
    items = db.query(TodoItemModel).filter(TodoItemModel.completed == False).all()
    return items  # Возвращаем пустой список [], если задач нет


# Получение задач за определенный период
@app.get("/date_range", response_model=List[TodoItem])
def get_items_by_date(start_date: str, end_date: str, db: Session = Depends(get_db)):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    print(start, end)
    items = db.query(TodoItemModel).filter(TodoItemModel.updated_at >= start, TodoItemModel.updated_at <= end).all()
    return items

# Завершение задачи
@app.put("/items/{item_id}/complete", response_model=TodoItem)
def mark_item_complete(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(TodoItemModel).filter(TodoItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.completed = True
    db.commit()
    db.refresh(db_item)
    return db_item

# Поиск задач по названию
@app.get("/search", response_model=List[TodoItem])
def search_items(query: str, db: Session = Depends(get_db)):
    items = db.query(TodoItemModel).filter(TodoItemModel.title.ilike(f"%{query}%")).all()
    return items

# Удаление всех задач
@app.delete("/items")
def delete_all_items(db: Session = Depends(get_db)):
    db.query(TodoItemModel).delete()
    db.commit()
    return {"message": "All items deleted"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)