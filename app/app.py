from fastapi import FastAPI

app = FastAPI()

# app.include_router(users.router, prefix="/v1")


@app.get('/')
def read_root():
    return {'message': 'Hello World!'}
