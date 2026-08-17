from fastapi import FastAPI

app = FastAPI(title="Movie DB API")

@app.get("/")
def read_root():
    return {"status": "Бэкенд запущен и работает!"}
