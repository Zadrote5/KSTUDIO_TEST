# Тестовое задание для K-Studio
## Микросервис для конвертации аудиозаписей в MP3 с сохранением в PostgreSQL и предоставлением ссылок для скачивания.

## 🚀 Возможности
### Создание пользователей: Уникальные токены доступа для каждого пользователя

### Конвертация аудио: WAV → MP3 с настройками качества (192k битрейт)

### Безопасность: Авторизация по токену для загрузки файлов

### Ссылки для скачивания: Генерация уникальных URL с проверкой прав доступа

### Docker-развёртывание: Готовый образ с PostgreSQL и всеми зависимостями

## 📋 Требования
### Docker: 20.10+

### Docker Compose: 2.0+

### Дисковое пространство: 100+ МБ (зависит от объёма аудиофайлов)

## 🛠 Быстрый старт
```bash
git clone https://github.com/yourusername/audio-conversion-service.git
cd audio-conversion-service
```

## Запуск сервиса
```bash
docker-compose up --build -d
```

## Проверка работы
```bash
curl -X POST "http://localhost:8000/users/" -H "Content-Type: application/json" -d '{"username": "test_user"}'
```

## 📡 API Endpoints
### 🆕 Создание пользователя
POST /users/
```bash
curl -X POST "http://localhost:8000/users/"
-H "Content-Type: application/json"
-d '{"username": "music_lover"}'
```
Ответ:
```json
{
"id": 1,
"username": "music_lover",
"token": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 🎧 Загрузка аудио
POST /audios/
```bash
curl -X POST "http://localhost:8000/audios/"
-F "user_id=1"
-F "token=550e8400-e29b-41d4-a716-446655440000"
-F "file=@/path/to/audio.wav"
```
Ответ:
```json
{
"download_url": "http://localhost:8000/record?id=3c8a8793-2e9b-4b6d-a7f2-91d0e4b5c7a2&user=1"
}
```

### 📥 Скачивание аудио
GET /record
```bash
curl -OJ "http://localhost:8000/record?id=3c8a8793-2e9b-4b6d-a7f2-91d0e4b5c7a2&user=1"
```
Результат:
Файл audio_3c8a8793-2e9b-4b6d-a7f2-91d0e4b5c7a2.mp3 будет сохранён в текущую директорию.


## 🚨 Устранение неполадок
1. Ошибки подключения к БД
```bash
docker-compose logs db | grep -i "error"

