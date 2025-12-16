======================================================
FINAL REPOSITORY TEST INSTRUCTIONS (Simulating Professor)
======================================================

These instructions simulate the exact steps a user (like your professor) will take after cloning the repository. The goal is to confirm that the new, secure .env configuration works perfectly.

------------------------------------------------------
PHASE 1: SETUP
------------------------------------------------------

1.  CLONE THE REPO:
    (Navigate to an empty directory, then run the clone command)
    git clone https://github.com/RajaMoaz/FastAPI-Auction-System.git
    cd FastAPI-Auction-System

2.  CREATE AND ACTIVATE VENV:
    python -m venv .venv
    .venv\Scripts\Activate

3.  INSTALL DEPENDENCIES:
    pip install -r requirements.txt

------------------------------------------------------
PHASE 2: DATABASE CONFIGURATION (Crucial Test)
------------------------------------------------------

Since the .env file is hidden by .gitignore, the project needs configuration. We will use the recommended, secure method.

4.  CREATE .ENV FILE:
    Create a new file named **.env** in the root of the 'FastAPI-Auction-System' folder (alongside requirements.txt).

5.  PASTE CREDENTIALS:
    Paste your known, WORKING PostgreSQL credentials into the new .env file:

    -----------------------------------
    # .env
    POSTGRES_USER="auction_admin"
    POSTGRES_PASSWORD="Auction_System_Pass_2025!"
    POSTGRES_HOST="localhost"
    POSTGRES_DB="auction_db"
    -----------------------------------

------------------------------------------------------
PHASE 3: RUN AND VERIFY
------------------------------------------------------

6.  START POSTGRES:
    Ensure your local PostgreSQL server service is running.

7.  START THE SERVER:
    Run the Uvicorn command in the terminal (with the venv activated):
    uvicorn auction_backend_python.main:socketio_app --reload

8.  VERIFY SERVER STARTUP:
    The server should start without a connection error, confirming that 'python-dotenv' successfully loaded the credentials from the new .env file.

9.  TEST FRONTEND FUNCTIONALITY:
    a. Open the **auction_frontend/index.html** file in your web browser.
    b. Verify that the system loads the auction items from the database.
    c. Submit a test bid to ensure the real-time update (via Socket.IO) and the database persistence (via FastAPI/SQLAlchemy) are both working.

======================================================
END OF TEST INSTRUCTIONS
======================================================
