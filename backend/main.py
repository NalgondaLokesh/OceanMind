from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import tempfile
import shutil
from pathlib import Path
import base64
import cv2
import numpy as np

from utils.detector import OceanMindDetector

# Initialize FastAPI app
app = FastAPI(
    title="OceanMind API",
    description="Marine Debris Detection API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global detector instance
detector = None

# Model settings
class DetectionSettings(BaseModel):
    conf_threshold: float = 0.4
    iou_threshold: float = 0.45

# Pydantic models for responses
class BBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

class Detection(BaseModel):
    class_id: int
    class_name: str
    confidence: float
    bbox: BBox

class PollutionSummary(BaseModel):
    total_items: int
    class_counts: dict
    severity: str
    severity_color: str
    detections: List[Detection]
    annotated_image: Optional[str] = None

# Startup event
@app.on_event("startup")
async def startup_event():
    global detector
    # Get the directory where this script is located
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(backend_dir, "models", "oceanmind_best.pt")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at: {model_path}")
    
    detector = OceanMindDetector(
        model_path=model_path,
        conf_threshold=0.4,
        iou_threshold=0.45
    )
    print("✅ OceanMind Detector loaded successfully")

@app.get("/")
async def root():
    return {
        "message": "OceanMind Marine Debris Detection API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "detect": "/detect",
            "batch_detect": "/batch-detect",
            "model_info": "/model-info"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "detector_loaded": detector is not None}

@app.get("/model-info")
async def get_model_info():
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not initialized")
    
    return {
        "model": "YOLO11s (Fine-tuned)",
        "mAP50": "70.8%",
        "precision": "81.9%",
        "num_classes": len(detector.class_names),
        "class_names": detector.class_names,
        "conf_threshold": detector.conf_threshold,
        "iou_threshold": detector.iou_threshold
    }

@app.post("/settings")
async def update_settings(settings: DetectionSettings):
    global detector
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not initialized")
    
    detector.conf_threshold = settings.conf_threshold
    detector.iou_threshold = settings.iou_threshold
    
    return {
        "message": "Settings updated",
        "conf_threshold": detector.conf_threshold,
        "iou_threshold": detector.iou_threshold
    }

def image_to_base64(image_array):
    """Convert numpy image array to base64 string"""
    _, buffer = cv2.imencode('.jpg', image_array)
    return base64.b64encode(buffer).decode('utf-8')

@app.post("/detect", response_model=PollutionSummary)
async def detect_image(
    file: UploadFile = File(...),
    return_image: str = Form("false")
):
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not initialized")
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Convert return_image to boolean
    should_return_image = return_image.lower() in ['true', '1', 'yes']
    
    # Save uploaded file temporarily
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Read and save file
        contents = await file.read()
        with open(temp_path, 'wb') as f:
            f.write(contents)
        
        # Get detection summary
        summary = detector.get_pollution_summary(temp_path)
        
        # Add annotated image if requested
        if should_return_image:
            print(f"Generating annotated image for {temp_path}")
            annotated_img = detector.visualize(temp_path)
            print(f"Annotated image shape: {annotated_img.shape}")
            summary['annotated_image'] = image_to_base64(annotated_img)
            print(f"Base64 encoded image length: {len(summary['annotated_image'])}")
        else:
            print(f"Annotated image not requested (return_image={return_image})")
        
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")
    
    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)

@app.post("/batch-detect")
async def batch_detect_images(files: List[UploadFile] = File(...)):
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not initialized")
    
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed for batch processing")
    
    results = []
    
    for file in files:
        if not file.content_type.startswith('image/'):
            results.append({
                "filename": file.filename,
                "error": "File must be an image"
            })
            continue
        
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, file.filename)
        
        try:
            contents = await file.read()
            with open(temp_path, 'wb') as f:
                f.write(contents)
            
            summary = detector.get_pollution_summary(temp_path)
            summary['filename'] = file.filename
            results.append(summary)
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
        
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    return {
        "total_processed": len(results),
        "successful": sum(1 for r in results if 'error' not in r),
        "results": results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
