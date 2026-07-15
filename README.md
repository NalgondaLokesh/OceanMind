# 🌊 OceanMind - Marine Debris Detection System

AI-Powered Marine Pollution Intelligence using YOLO11s

## Overview

OceanMind is an advanced computer vision system designed to detect and analyze marine debris in images. Built with YOLO11s and Streamlit, it provides real-time detection, pollution severity assessment, and batch processing capabilities for environmental monitoring.

## Features

- **Real-time Detection**: Detect marine debris using fine-tuned YOLO11s model
- **Multiple Debris Classes**: Identifies 6-7 types of marine debris
- **Pollution Severity Assessment**: Automatic severity scoring (Low, Medium, High, Critical)
- **Interactive Web Interface**: Beautiful Streamlit dashboard with visualizations
- **Batch Processing**: Process multiple images simultaneously
- **Rich Visualizations**: Detection bounding boxes, class distribution charts, and severity gauges
- **Export Results**: Download detection results as CSV files

## Model Performance

- **Model**: YOLO11s (Fine-tuned)
- **mAP50**: 70.8%
- **Precision**: 81.9%
- **Classes**: 6-7 marine debris types
- **Inference Speed**: ~750-900ms per image (640x640)

## Installation

### Prerequisites

- Python 3.10 or higher
- CUDA-capable GPU (recommended for faster inference)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd OceanMind
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the model:
   - Place `oceanmind_best.pt` in the `models/` directory
   - Or place it in the root directory

## Usage

### Running the Web Application

```bash
streamlit run app.py
```

The application will launch in your browser at `http://localhost:8501`

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
├── app.py                 # Streamlit web application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── models/               # Model weights directory
│   └── oceanmind_best.pt
├── utils/                # Utility modules
│   └── detector.py       # OceanMindDetector class
├── uploads/              # User uploaded images
│   └── samples/          # Sample images for testing
├── outputs/              # Processed image outputs
└── assets/               # Static assets
```

## Web Interface Features

### Single Image Detection
- Upload images via file uploader
- Use sample images from the gallery
- View detection results with bounding boxes
- Analyze class distribution
- Monitor pollution severity with gauge charts

### Batch Processing
- Upload multiple images at once
- Progress tracking during processing
- Summary table of all results
- Export results as CSV

### Settings
 - Adjustable confidence threshold (0.1 - 0.9)
- Adjustable IoU threshold (0.1 - 0.9)
- Real-time model performance metrics

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

- streamlit>=1.28.0
- ultralytics>=8.0.0
- opencv-python>=4.8.0
- numpy>=1.24.0
- pandas>=2.0.0
- plotly>=5.14.0
- Pillow>=10.0.0

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with [Ultralytics YOLO11](https://github.com/ultralytics/ultralytics)
- Web interface powered by [Streamlit](https://streamlit.io/)
- Visualizations using [Plotly](https://plotly.com/)

---

🌊 OceanMind - Protecting our oceans with AI-powered detection
