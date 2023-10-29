from fastapi import FastAPI, HTTPException
from model import DelayModel
import pandas as pd


app = FastAPI.FastAPI()
model = DelayModel()

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(flight_data: dict) -> dict:
    try:
        # Checks if the model has been trained
        if model._model is None:
            raise HTTPException(status_code=400, detail="Model not trained")

        # Converts the received data to DataFrame
        df = pd.DataFrame([flight_data])

        # Preprocessing and prediction
        features = model.preprocess(df)
        prediction = model.predict(features)

        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
