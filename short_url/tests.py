import pytest
from fastapi.testclient import TestClient
from main import app, generate_short_id

client = TestClient(app)


def test_generate_short_id():
    """Тестирует генерацию короткого идентификатора."""
    short_id = generate_short_id()
    assert len(short_id) == 6
    assert short_id.isalnum()


def test_shorten_url():
    """Тестирует создание короткой ссылки."""
    response = client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data
    assert data["short_url"].startswith("http://localhost:8000/")


def test_shorten_url_invalid():
    """Тестирует обработку некорректного URL."""
    response = client.post("/shorten", json={"url": "not-a-url"})
    assert response.status_code == 422  # Ошибка валидации данных


def test_redirect_to_full_not_found():
    """Тестирует перенаправление по несуществующей короткой ссылке."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Короткая ссылка не найдена"


def test_health_check():
    """Тестирует состояние сервиса."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


def test_list_urls():
    """Тестирует получение списка всех сокращенных ссылок."""
    # Создаем несколько ссылок
    client.post("/shorten", json={"url": "https://example.com/1"})
    client.post("/shorten", json={"url": "https://example.com/2"})
    
    response = client.get("/list")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # Проверяем, что ссылки добавились
    for item in data:
        assert "short_id" in item
        assert "full_url" in item


def test_delete_short_url():
    """Тестирует удаление короткой ссылки."""
    # Сначала создаем короткую ссылку
    create_response = client.post(url="/shorten", json={"url": "https://example.com"})
    assert create_response.status_code == 200
    short_url = create_response.json()["short_url"]
    short_id = short_url.split("/")[-1]

    # Удаляем созданную ссылку
    delete_response = client.delete(url=f"/{short_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == "Короткая ссылка удалена"

    # Проверяем, что ссылка больше недоступна
    redirect_response = client.get(url=f"/{short_id}")
    assert redirect_response.status_code == 404


def test_update_url():
    """Тестирует обновление оригинального URL."""
    # Создаем короткую ссылку
    create_response = client.post(url="/shorten", json={"url": "https://eeeeee.com"})
    assert create_response.status_code == 200
    short_url = create_response.json()["short_url"]
    short_id = short_url.split("/")[-1]

    # Обновляем ссылку
    update_response = client.put(url=f"/{short_id}", json={"url": "https://pornhub.com"})
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["detail"] == "URL обновлен"
    assert updated_data["full_url"] == "https://pornhub.com"

    # Проверяем, что редирект работает на новый URL
    redirect_response = client.get(url=f"/{short_id}")
    assert redirect_response.status_code == 200
    assert redirect_response.url == "https://pornhub.com"
