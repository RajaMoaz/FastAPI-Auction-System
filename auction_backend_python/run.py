# run.py

import uvicorn

if __name__ == "__main__":
    # Ensure all parameters are set correctly
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)