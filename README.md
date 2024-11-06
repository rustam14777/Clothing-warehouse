
# 👔 Clothing Warehouse

## 📋 Description
Clothing Warehouse is an application for managing a clothing inventory. Users can create orders, and administrators can process these orders, issue clothing, and manage stock.

## 🛠 Technologies
- **Python 3.12**: Modern and powerful programming language
- **FastAPI**: Asynchronous web framework for creating API.
- **PostgreSQL**: Relational database.
- **Docker**: For containerizing the application.
- **Docker Compose**: For managing multi-container applications.
- **Alembic**: For database migrations.
- **SQLAlchemy**: ORM for interacting with the database.
- **Pydantic**: For data validation.
- **pytest**: For testing.

## 📦 Installation

### 🐳 Docker Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/rustam14777/Clothing-warehouse.git
   cd Clothing-warehouse
   ```
2. **Create a .env_docker file and add your configuration data as defined in src/config.py,
as well as the following.**
   ```
   POSTGRES_DB=your_name_db
   POSTGRES_USER=your_user_db
   POSTGRES_PASSWORD=your_password    
   ```
3. **Build Docker-images.**
    ```bash
    docker-compose build
    ```
4. **Run the application.**
   ```bash
   docker-compose up
   ```
5. **The application will be available at:**
   http://localhost:8000

### 💻 Local Development Setup
1. **Set up virtual environment.**
   - *Install virtualenv*
   ```
   pip install virtualenv
   ```
   - *Create and activate virtual environment*
   ```
   python -m venv .venv
   ```
   - *Windows*
   ```
   .venv\Scripts\activate
   ```
   - *Linux*
   ```
   source .venv/bin/activate
   ```
   
2. **Install dependencies.**
   ```
   pip install requirements.txt
   ```
3. **Create a .env file and add your configuration data as defined in src/config.py.**

4. **Run the project from the root directory.**
   ```
   uvicorn src.main:app --reload
   ```
5. **The application will be available at:**
   http://localhost:8000

## 🧪 Testing
The application allows for testing directly within the IDE, such as PyCharm.
To run tests, follow these steps:
### Prerequisites
- Activated virtual environment
- Installed dependencies
- Configured .env file
### Run tests
   ```
   pytest
   ```

