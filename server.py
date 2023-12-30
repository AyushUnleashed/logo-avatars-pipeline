from fastapi import FastAPI, HTTPException
from pipeline.generate_image import run_generate
from models.base_request_model import BaseSDRequest
from datetime import datetime

app = FastAPI()

# Heartbeat endpoint
@app.get("/heartbeat")
async def heartbeat():
    return {"status": "alive"}

# Inpaint Endpoint
@app.post("/generate_image")
async def generate_image(base_request: BaseSDRequest):
    try:

        req_id = datetime.now().strftime("%Y%m%d%H%M%S")
        print(req_id)
        # Call the inpainting function
        generated_image_encoded = run_generate(base_request, req_id)

        return {
            "prompt": base_request.prompt,
            "generated_image_encoded": generated_image_encoded
        }

    except Exception as e:
        print(f"Exception occurred with error as {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8125)