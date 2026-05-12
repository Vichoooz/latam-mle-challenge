from challenge.model import DelayModel
import fastapi 
from pydantic import BaseModel
import pandas as pd

app = fastapi.FastAPI()
model = DelayModel()

# Valores válidos
VALID_MES = set(range(1, 13))
VALID_TIPOVUELO = {"N", "I"}

#Train the model when the API starts


data = pd.read_csv("data/data.csv")
features, target = model.preprocess(data, target_column="delay")
model.fit(features, target)


    
@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(request: dict) -> dict:

    try:
        flights = request["flights"]
        # Validar
        for flight in flights:
            mes = flight.get("MES")
            tipovuelo = flight.get("TIPOVUELO")
            
            if mes not in VALID_MES:
                raise ValueError(f"MES {mes} inválido")
            if tipovuelo not in VALID_TIPOVUELO:
                raise ValueError(f"TIPOVUELO {tipovuelo} inválido")
        
        features = model.preprocess(pd.DataFrame(flights))
        predictions = model._model.predict(features)
        return {"predict": predictions.tolist()}
    except Exception as e:
        raise fastapi.HTTPException(status_code=400, detail=str(e))


