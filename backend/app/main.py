from fastapi import FastAPI

app = FastAPI(title="Retail Portal API")

@app.get("/")
def health():
    return {"status": "ok", "message": "Retail Portal API is running"}