
# Clothing warehouse

## Description
Clothing Warehouse is an application for managing a clothing inventory. Users can create orders, and administrators can process these orders, issue clothing, and manage stock.

## Technologies
- <strong>Python 3.12</strong>: Programing Language. 
- <strong>FastAPI</strong>: Asynchronous web framework for creating API.
- <strong>PostgreSQL</strong>: Relational database.
- <strong>Docker</strong>: For containerizing the application.
- <strong>Docker Compose</strong>: For managing multi-container applications.
- <strong>Alembic</strong>:  For database migrations.
- <strong>SQLAlchemy</strong>: ORM for interacting with the database.
- <strong>Pydantic</strong>: For data validation.
- <strong>pytest</strong>: For testing.

## Installation

- <strong>Docker</strong>
1. Clone the repositories:
        
        bash
        git clone https://github.com/rustam14777/Clothing-warehouse.git
        cd your_repositories

2. Create a .env_docker file and add your configuration data as defined in src/config.py,
as well as the following:

        POSTGRES_DB=your_name_db
        POSTGRES_USER=your_user_db
        POSTGRES_PASSWORD=your_password    

3. Build Docker-images:

        bash
        docker-compose build

4. Run the application:
 
       bash
       docker-compose up

5. The application will be available at:

       http://localhost:8002

- <strong>IDE</strong>
1. Install and activate a virtual environment:

       Terminal
       pip install virtualenv
       cd project_folder
       python -m venv .venv
       .venv\Scripts\activate (Windows)
       .venv/bin/activate (Linux)

2. Install dependencies:

       Terminal
       pip install requirements.txt

3. Create a .env file and add your configuration data as defined in src/config.py:

4. Run the project from the root directory:
       
       Terminal
       uvicorn src.main:app --reload

5. The application will be available at:
    
       http://localhost:8000

## Testing

The application allows for testing directly within the IDE, such as PyCharm.
To run tests, follow these steps:

1. Install and activate a virtual environment:
    
       Terminal
       pip install virtualenv
       cd project_folder
       python -m venv .venv
       .venv\Scripts\activate (Windows)
       .venv/bin/activate (Linux)

2. Install dependencies:

       Terminal
       pip install requirements.txt

3. Create a .env file and add your configuration data as defined in src/config.py.

4. Run tests:

       Terminal
       pytest

