import io
import random
from webbrowser import get
import cv2
import numpy as np
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from numpy import nansum
from fastapi.templating import Jinja2Templates
app = FastAPI()
handler = nansum(app)
templates = Jinja2Templates(directory = "templates")

# Allow all origins for simplicity (configure this appropriately for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # Read the file into a NumPy array
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)

    # Decode the NumPy array into an image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Define font and text properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (random.randint(0, image.shape[1] - 1), random.randint(0, image.shape[0] - 1))  # Random position
    fontScale = 1
    color = (255, 0, 0)  # Blue color in BGR
    thickness = 2

    # Using cv2.putText() method to add text to the image
    image = cv2.putText(image, 'Simple', org, font, fontScale, color, thickness, cv2.LINE_AA)

    # Save the modified image
    cv2.imwrite("output.jpg", image)

    return {"filename": file.filename}



@app.get("/latest_image")
async def get_latest_image():
    with open("output.jpg","rb") as f:
        
        return StreamingResponse(io.BytesIO(f.read()), media_type="image/jpeg")
    return {"error": "No image available"}

@app.get("/",response_class = HTMLResponse)
async def getpage(request : Request):
    return templates.TemplateResponse("./index.html",{"request":request}) 



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)