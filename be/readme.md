# Backend installation - structure guide
## Installation
    1. Requirements:
        - Python 3.11.9
        - docker if needed
        - PostgreSQL 16.10
        - be folder
    2. venv setup:
       `python -m venv .venv
        # Linux:
        .venv\Scripts\activate
        # Windows:
        .venv\Scripts\Activate.ps1
        pip install -r requirements.txt`
    3. Database setup:
        `docker run -d --name db \
        -e POSTGRES_PASSWORD=123456 \
        -p 5432:5432 \
        postgres:16`
    4. Run:
        - Create a .env file in `be/app/` using .env.example
        - `uvicorn app.main:app --reload`

## Structure
be/
|-- app/                // root folder
|   |-- db/             // database modules (connect, models, etc)
|   |-- models/         // Pydantic/ORM models
|   |-- routers/        // routers, app
|   |-- utils/          // utilities modules (auth, log, mockdb, etc)
|   |-- .env.example    // example env config
|   |-- __init__.py     // initialize something idk
|   └-- main.py         // main application
|-- test/               // unit test (idk)
└-- requirements.txt    // python venv requirements
