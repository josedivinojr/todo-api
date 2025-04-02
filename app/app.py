from fastapi import FastAPI
from app.endpoints import users, auth

app = FastAPI()

app.include_router(users.router, prefix="/v1")
app.include_router(auth.router, prefix="/v1")


@app.get('/')
def read_root():
    return {'message': 'Hello World!'}
