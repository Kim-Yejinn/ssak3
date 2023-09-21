from fastapi import FastAPI

app = FastAPI(title='Project title',
            description='Description of your project',
            openapi_url='/api/openapi.json')

@app.get("/")
def read_root():
    return {"Hello": "World"}
