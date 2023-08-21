from fastapi import FastAPI
from router import cpu_GET
from router import cpu_POST

# reload - uvicorn main:app --reload

app = FastAPI()
app.include_router(cpu_GET.router)
app.include_router(cpu_POST.router)

# basic function
@app.get('/', tags=['Default'])
def index():
    return {'message': 'main page of PC Compatibility Checker'}

