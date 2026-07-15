# 🌊 OceanMind - Marine Debris Detection System

AI-Powered Marine Pollution Intelligence using YOLO11s

## Overview

OceanMind is an advanced computer vision system designed to detect and analyze marine debris in images. Built with YOLO11s, FastAPI backend, and React frontend, it provides real-time detection, pollution severity assessment, and batch processing capabilities for environmental monitoring.

## Features

- **Real-time Detection**: Detect marine debris using fine-tuned YOLO11s model
- **Multiple Debris Classes**: Identifies 6-7 types of marine debris
- **Pollution Severity Assessment**: Automatic severity scoring (Low, Medium, High, Critical)
- **Modern Web Interface**: Beautiful React frontend with TailwindCSS styling
- **FastAPI Backend**: RESTful API for image detection and analysis
- **Batch Processing**: Process multiple images simultaneously
- **Rich Visualizations**: Detection bounding boxes, class distribution charts, and severity gauges
- **Separate Architecture**: Frontend and backend are completely decoupled

## Model Performance

- **Model**: YOLO11s (Fine-tuned)
- **mAP50**: 70.8%
- **Precision**: 81.9%
- **Classes**: 6-7 marine debris types
- **Inference Speed**: ~750-900ms per image (640x640)

## Installation

### Prerequisites

- Python 3.10 or higher
- Node.js 16+ and npm
- CUDA-capable GPU (recommended for faster inference)

### Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd OceanMind
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Download the model:
   - Place `oceanmind_best.pt` in the `backend/models/` directory

4. Start the FastAPI backend:
```bash
cd backend
python main.py
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

### Using the Detector Programmatically

```python
from utils.detector import OceanMindDetector

# Initialize detector
detector = OceanMindDetector(
    model_path="models/oceanmind_best.pt",
    conf_threshold=0.4,
    iou_threshold=0.45
)

# Detect objects in an image
detections = detector.get_detections("path/to/image.jpg")

# Get pollution summary
summary = detector.get_pollution_summary("path/to/image.jpg")

# Visualize detections
annotated_img = detector.visualize("path/to/image.jpg")

# Batch process multiple images
results = detector.process_batch(
    image_paths=["img1.jpg", "img2.jpg"],
    output_dir="outputs"
)
```

## Project Structure

```
OceanMind/
├── backend/              # FastAPI backend
│   ├── main.py          # FastAPI application with API endpoints
│   ├── models/          # Model weights directory
│   │   └── oceanmind_best.pt
│   └── utils/           # Utility modules
│       └── detector.py  # OceanMindDetector class
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   │   ├── Header.js
│   │   │   ├── Sidebar.js
│   │   │   ├── ImageUpload.js
│   │   │   ├── DetectionResults.js
│   │   │   └── ModelInfo.js
│   │   ├── App.js       # Main React application
│   │   ├── index.js     # React entry point
│   │   └── index.css    # Global styles with TailwindCSS
│   ├── public/
│   │   └── index.html   # HTML template
│   ├── package.json     # Node.js dependencies
│   ├── tailwind.config.js
│   └── postcss.config.js
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## API Endpoints

The FastAPI backend provides the following endpoints:

- `GET /` - API information and available endpoints
- `GET /health` - Health check endpoint
- `GET /model-info` - Get model information and performance metrics
- `POST /settings` - Update detection settings (confidence and IoU thresholds)
- `POST /detect` - Detect marine debris in a single image
- `POST /batch-detect` - Detect marine debris in multiple images (max 10)

## Web Interface Features

### Single Image Detection
- Upload images via drag-and-drop or file picker
- Real-time image preview
- View detection results with annotated bounding boxes
- Analyze class distribution with interactive charts
- Monitor pollution severity with color-coded indicators

### Settings Panel
- Adjustable confidence threshold (0.1 - 0.9)
- Adjustable IoU threshold (0.1 - 0.9)
- Real-time model performance metrics display
- Model information panel

### Detection Results
- Total items detected
- Pollution severity assessment (Low, Medium, High, Critical)
- Detailed detection table with class names and confidence scores
- Class distribution bar chart
- Annotated image with bounding boxes

## Detected Debris Classes

The model can detect various types of marine debris including:
- Tires
- Bottles
- Plastic containers
- Fishing gear
- And other marine waste items

## Pollution Severity Levels

- **Low** (🟢): 0 items detected
- **Medium** (🟡): 1-2 items detected
- **High** (🟠): 3-5 items detected
- **Critical** (🔴): 6+ items detected

## Requirements

### Backend (Python)
- fastapi>=0.104.0
- uvicorn[standard]>=0.24.0
- python-multipart>=0.0.6
- pydantic>=2.0.0
- ultralytics>=8.0.0
- opencv-python>=4.8.0
- numpy>=1.24.0
- pandas>=2.0.0
- Pillow>=10.0.0

### Frontend (Node.js)
- react>=18.2.0
- react-dom>=18.2.0
- react-scripts>=5.0.1
- axios>=1.6.0
- lucide-react>=0.294.0
- recharts>=2.10.0
- tailwindcss>=3.3.0

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with [Ultralytics YOLO11](https://github.com/ultralytics/ultralytics)
- Backend powered by [FastAPI](https://fastapi.tiangolo.com/)
- Frontend built with [React](https://reactjs.org/) and [TailwindCSS](https://tailwindcss.com/)
- Visualizations using [Recharts](https://recharts.org/)

---

🌊 OceanMind - Protecting our oceans with AI-powered detection
