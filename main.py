from fastapi import FastAPI, HTTPException, UploadFile, File
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)
app = FastAPI()
origins = [
    "http://localhost:3000",  # Cho React/Vue chạy cục bộ
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        return {
            "meta":{
                "status" : "success",
                "message" : "Image uploaded successfully",
                "code" : 200
            },
            "result": upload_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Photo processing error : {str(e)}")
    

@app.post("/upload-gif")
async def upload_image(folder : str | None = None,file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".gif"):
            raise HTTPException(status_code=400, detail="Chỉ chấp nhận file GIF")

        upload_result = cloudinary.uploader.upload(
            file.file,
            resource_type="image", 
            folder=folder or "uploads",
            public_id=file.filename.split('.')[0]
        )

        return {
            "meta":{
                "status" : "success",
                "message" : "GIF uploaded successfully",
                "code" : 200
            },
            "result": upload_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Photo processing error : {str(e)}")
@app.get("/list-gif")
async def list_gif(folder : str = "gifs"):
    try:
        list_result = cloudinary.Search().expression('folder:'+folder).execute()
        return {
            "meta":{
                "status" : "success",
                "message" : "List GIF",
                "code" : 200
            },
            "result": list_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Photo processing error : {str(e)}")