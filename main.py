# 1. Implement venv >python -m venv fastapi-venv
# 2. Activate the venv >C:\*\Scripts\activate.bat
# 3. Install uvicorn >pip install uvicorn
# 4. Install uvicorn >pip install fastapi
# 5. Check installation success >uvicorn --version
# 6. Running uvicorn >uvicorn main:app --reload
# Extra note:
# Syntax to get all requirement installation: pip freeze > requirements.txt
# Can install all requirement in requirements.txt: pip3 install -r requirements.txt

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import cpu_handler
from router import mb_handler
from router import input_handler
import logging

app = FastAPI()


# Configure CORS to allow requests from your extension's origin
origins = [

    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cpu_handler.router)
app.include_router(mb_handler.router)
app.include_router(input_handler.router)

#Debug handling, remove # to enable
logging.basicConfig(level=logging.DEBUG)

# Default route
@app.get("/", tags=["Default"])
def index():
    return {"message": "Main page of PC Compatibility Checker"}
