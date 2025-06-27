from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
  return {"Hello": "World"}

@app.get("/stats/{device_id}")
def read_stat(device_id: int, q: str | None = None):
  return {"device_id": device_id, "q": q}
