from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import uvicorn
import os
from inference import TryOnModel  # assuming you expose TryOnModel from model.py
from PIL import Image
import io

app = FastAPI()
model = TryOnModel()  # Initialize your TryOnGAN model

@app.post("/tryon/")
async def tryon(input_image: UploadFile = File(...), clothes_image: UploadFile = File(...)):
    input_bytes = await input_image.read()
    clothes_bytes = await clothes_image.read()

    input_img = Image.open(io.BytesIO(input_bytes)).convert("RGB")
    clothes_img = Image.open(io.BytesIO(clothes_bytes)).convert("RGB")

    output = model.run(input_img, clothes_img)  # You might need to adapt this
    output_path = "output.jpg"
    output.save(output_path)

    return FileResponse(output_path, media_type="image/jpeg")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
