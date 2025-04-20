from fastapi import FastAPI, HTTPException
from google.cloud import firestore
from google.oauth2 import service_account
import vertexai
from vertexai.preview.generative_models import GenerativeModel
import datetime

# === CONFIG ===
PROJECT_ID = "astute-asset-456404-r9"
LOCATION = "us-east1"
MODEL_ID = "projects/astute-asset-456404-r9/locations/us-east1/endpoints/6023753617608015872"
SERVICE_ACCOUNT_PATH = "env.json"
LIMIT = 100
COUNTER_DOC = "request_counter/daily"

# === INIT GOOGLE CLOUD ===
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH)
vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)
db = firestore.Client(project=PROJECT_ID, credentials=credentials)

# Use your fine-tuned endpoint as a GenerativeModel
model = GenerativeModel(model_name=MODEL_ID)

# === FASTAPI APP ===
app = FastAPI()

@app.post("/generate")
def generate(payload: dict):
    input_text = payload.get("input", "")
    if not input_text:
        raise HTTPException(status_code=400, detail="Missing 'input'")

    # === RATE LIMIT ===
    today = datetime.date.today().isoformat()
    doc_ref = db.document(COUNTER_DOC)
    doc = doc_ref.get()

    if not doc.exists or doc.to_dict().get("date") != today:
        doc_ref.set({"count": 1, "date": today})
    else:
        count = doc.to_dict().get("count", 0)
        if count >= LIMIT:
            raise HTTPException(status_code=429, detail="Daily request limit reached")
        doc_ref.update({"count": firestore.Increment(1)})

    # === CALL GEMINI-LITE-BASED FINE-TUNED MODEL ===
    try:
        response = model.generate_content(input_text)
        return {"output": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ping")
def ping():
    return {"status": "ok"}


# === LOCAL DEV (OPTIONAL) ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
