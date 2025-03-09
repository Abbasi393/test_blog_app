# A FastAPI Blog Application

A FastAPI-based blog application with PostgreSQL as the database and Redis for caching.

## Prerequisites

Ensure you have the following installed:

- Python 3.10+
- PostgreSQL
- Redis
- Docker (optional for containerized deployment)

## Environment Variables

Create a `.env` file in the project root and add the following:

```env
ENVIRONMENT=dev
VERSION=0.0.1
DATABASE_URL=postgresql://username:password@localhost:5432/blog_db
API_URL_PREFIX=tiny
BASE_URL=http://127.0.0.1:8000
SECRET_KEY=secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0
cache_expiry=1000
```

## Run the Application without Docker

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Abbasi393/test_blog_app
   cd test_blog_app
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   Run the following script to set up the database:

   ```bash
   bash scripts/alembic_setup_test_database.sh
   ```
5. **Run database migrations:**

   ```bash
   alembic upgrade head
   ```

6. **Start the FastAPI application:**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

7. **Access the API documentation:**

   Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

## Run the Application with Docker

### Docker Setup

Ensure Docker and Docker Compose are installed.

1. **Build and start the containers:**

   ```bash
   docker-compose up --build
   ```

2. **Apply database migrations:**

   ```bash
   docker-compose exec app alembic upgrade head
   ```

3. **Access the application:**

   Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

![Docs](img.png)


## Useful Docker Commands

- **Stop all services:**

  ```bash
  docker-compose down
  ```

- **View logs:**

  ```bash
  docker-compose logs -f
  ```

- **Rebuild containers:**

  ```bash
  docker-compose up --build
  
