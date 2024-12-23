import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base
from models import TodoItem as TodoItemModel
from datetime import datetime, timedelta
from database import engine, SessionLocal

TestingSessionLocal = SessionLocal

# Подготовка базы данных
Base.metadata.create_all(bind=engine)

# Заменяем зависимость базы данных для тестирования
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Фикстура для очистки базы данных перед каждым тестом
@pytest.fixture(autouse=True)
def clean_db():
    db = TestingSessionLocal()
    db.query(TodoItemModel).delete()
    db.commit()
    db.close()

# Тесты
def test_create_item():
    response = client.post(
        "/items",
        json={"title": "Test Todo", "description": "Test description", "completed": False},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test description"
    assert data["completed"] is False

def test_get_items():
    # Создаем задачу
    client.post("/items", json={"title": "Test Todo", "description": "Test description", "completed": False})

    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Todo"

def test_get_item_by_id():
    # Создаем задачу
    response = client.post("/items", json={"title": "Test Todo", "description": "Test description", "completed": False})
    item_id = response.json()["id"]

    # Проверяем получение задачи по ID
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id

def test_update_item():
    # Создаем задачу
    response = client.post("/items", json={"title": "Test Todo", "description": "Test description", "completed": False})
    item_id = response.json()["id"]

    # Обновляем задачу
    response = client.put(f"/items/{item_id}", json={"title": "Updated Title", "description": "Updated description", "completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated description"
    assert data["completed"] is True

def test_delete_item():
    # Создаем задачу
    response = client.post("/items", json={"title": "Test Todo", "description": "Test description", "completed": False})
    item_id = response.json()["id"]

    # Удаляем задачу
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Item deleted"

def test_get_completed_items():
    # Создаем задачи
    client.post("/items", json={"title": "Completed Task", "description": None, "completed": True})
    client.post("/items", json={"title": "Incomplete Task", "description": None, "completed": False})

    # Получаем завершенные задачи
    response = client.get("/completed")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Completed Task"

def test_get_incomplete_items():
    # Создаем задачи
    client.post("/items", json={"title": "Completed Task", "description": None, "completed": True})
    client.post("/items", json={"title": "Incomplete Task", "description": None, "completed": False})

    # Получаем незавершенные задачи
    response = client.get("/incomplete")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Incomplete Task"

def test_get_items_by_date():
    # Создаем задачи с заданной датой
    response = client.post(
        "/items",
        json={"title": "Test Todo", "description": "Test description", "completed": False},
    )
    assert response.status_code == 200

    # Получаем задачи за период
    dt_to_str = lambda dt:  dt.strftime("%Y-%m-%d")
    start = datetime.now()
    end = dt_to_str(start + timedelta(days=1))
    response = client.get(f"/date_range?start_date={dt_to_str(start)}&end_date={end}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_search_items():
    # Создаем задачи
    client.post("/items", json={"title": "Buy Milk", "description": None, "completed": False})
    client.post("/items", json={"title": "Buy Bread", "description": None, "completed": False})

    # Поиск задач
    response = client.get("/search?query=Milk")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Buy Milk"

def test_delete_all_items():
    # Создаем задачи
    client.post("/items", json={"title": "Task 1", "description": None, "completed": False})
    client.post("/items", json={"title": "Task 2", "description": None, "completed": False})

    # Удаляем все задачи
    response = client.delete("/items")
    assert response.status_code == 200
    assert response.json()["message"] == "All items deleted"

    # Проверяем, что задач больше нет
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0
