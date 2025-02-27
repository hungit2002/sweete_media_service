from fastapi import FastAPI, HTTPException, UploadFile, File
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)
app = FastAPI()

@app.post("/upload-image")
async def upload_image(folder : str | None = None,file: UploadFile = File(...)):
    try:
        image = Image.open(file.file)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=50)
        buffer.seek(0)

        upload_result = cloudinary.uploader.upload(buffer, folder=folder or "uploads", public_id=file.filename.split('.')[0])
        return {"url": upload_result["secure_url"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Photo processing error : {str(e)}")