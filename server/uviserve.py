import time
from typing import Annotated
from webbrowser import get
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from PIL import Image
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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
    with open(f"output.{file.filename[-3:]}" , "wb") as f:
        f.write( await file.read())
    return {"filename": file.filename}


@app.get("/",response_class = HTMLResponse)
async def getpage(request : Request):
    return templates.TemplateResponse("./index.html",{"request":request}) 



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)