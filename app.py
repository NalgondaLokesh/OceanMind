import streamlit as st
import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import tempfile

# Import the detector
from utils.detector import OceanMindDetector

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="OceanMind - Marine Debris Detection",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3d59;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #2e5a7e;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-card-2 {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .severity-low {
        color: #2ecc71;
        font-weight: bold;
    }
    .severity-medium {
        color: #f1c40f;
        font-weight: bold;
    }
    .severity-high {
        color: #e67e22;
        font-weight: bold;
    }
    .severity-critical {
        color: #e74c3c;
        font-weight: bold;
    }
    .detection-box {
        background-color: #f8f9fa;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.3rem 0;
        border-left: 4px solid #667eea;
    }
    .footer {
        text-align: center;
        color: #6c757d;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3095/3095586.png", width=80)
    st.markdown("## 🌊 OceanMind")
    st.markdown("### Marine Pollution Intelligence")
    
    st.markdown("---")
    
    # Model settings
    st.markdown("### ⚙️ Settings")
    
    conf_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.1,
        max_value=0.9,
        value=0.4,
        step=0.05,
        help="Minimum confidence score for detections"
    )
    
    iou_threshold = st.slider(
        "IoU Threshold",
        min_value=0.1,
        max_value=0.9,
        value=0.45,
        step=0.05,
        help="Intersection over Union threshold for NMS"
    )
    
    st.markdown("---")
    
    # Model info
    st.markdown("### 📊 Model Info")
    st.info("""
    **Model:** YOLO11s (Fine-tuned)
    **mAP50:** 70.8%
    **Precision:** 81.9%
    **Classes:** 6 marine debris types
    """)
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("### 📈 Performance")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("mAP50", "70.8%", "+9.4%")
    with col2:
        st.metric("Precision", "81.9%", "+2.7%")

# ============================================
# MAIN CONTENT
# ============================================

st.markdown('<div class="main-header">🌊 OceanMind</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Marine Debris Detection & Environmental Intelligence</div>', unsafe_allow_html=True)

# ============================================
# LOAD MODEL
# ============================================

@st.cache_resource
def load_model():
    """Load the OceanMind detector"""
    model_path = "models/oceanmind_best.pt"
    
    # Check if model exists in current directory
    if not os.path.exists(model_path):
        # Try relative path
        model_path = "oceanmind_best.pt"
    
    if not os.path.exists(model_path):
        st.error(f"❌ Model not found at: {model_path}")
        st.warning("Please make sure 'oceanmind_best.pt' is in the 'models/' folder or root directory.")
        st.stop()
    
    detector = OceanMindDetector(
        model_path=model_path,
        conf_threshold=conf_threshold,
        iou_threshold=iou_threshold
    )
    return detector

try:
    detector = load_model()
    st.success("✅ Model loaded successfully!")
except Exception as e:
    st.error(f"❌ Error loading model: {str(e)}")
    st.stop()

# ============================================
# INPUT SECTION
# ============================================

st.markdown("### 📤 Upload Image")

# Create tabs for different input methods
tab1, tab2, tab3 = st.tabs(["📷 Upload Image", "📁 Sample Images", "📹 Batch Process"])

with tab1:
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
        help="Upload an image containing marine debris"
    )

with tab2:
    st.markdown("Or use a sample image:")
    
    # Check for sample images
    sample_dir = "uploads/samples"
    sample_images = []
    
    if os.path.exists(sample_dir):
        sample_images = [f for f in os.listdir(sample_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    if sample_images:
        selected_sample = st.selectbox("Select sample image:", sample_images)
        use_sample = st.button("🔍 Process Sample Image")
        
        if use_sample:
            sample_path = os.path.join(sample_dir, selected_sample)
            # Create a file-like object
            with open(sample_path, 'rb') as f:
                uploaded_file = f.read()
            uploaded_file = type('obj', (object,), {'name': selected_sample, 'read': lambda: uploaded_file})()
            st.rerun()
    else:
        st.info("No sample images found. Upload your own images to get started!")

with tab3:
    st.markdown("### 📹 Batch Processing")
    
    batch_files = st.file_uploader(
        "Upload multiple images...",
        type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
        accept_multiple_files=True
    )
    
    if batch_files:
        st.info(f"📁 {len(batch_files)} images selected")

# ============================================
# PROCESSING
# ============================================

if uploaded_file is not None:
    # Save uploaded file
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, uploaded_file.name)
    
    with open(temp_path, 'wb') as f:
        f.write(uploaded_file.read())
    
    # Process image
    with st.spinner('🔍 Analyzing image...'):
        # Get detections and summary
        summary = detector.get_pollution_summary(temp_path)
        annotated_img = detector.visualize(temp_path)
    
    # ============================================
    # DISPLAY RESULTS
    # ============================================
    
    st.markdown("---")
    st.markdown("### 📊 Detection Results")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Items", summary['total_items'], delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="metric-card-2">', unsafe_allow_html=True)
        st.metric("Severity", summary['severity'], delta=summary['severity_color'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        unique_classes = len(summary['class_counts'])
        st.metric("Unique Debris Types", unique_classes)
    
    with col4:
        avg_conf = np.mean([d['confidence'] for d in summary['detections']]) if summary['detections'] else 0
        st.metric("Avg Confidence", f"{avg_conf:.1%}")
    
    # Image and detections side by side
    col_img, col_det = st.columns([2, 1])
    
    with col_img:
        st.image(annotated_img, caption="Detected Objects")
    
    with col_det:
        st.markdown("#### 📋 Detections")
        
        if summary['detections']:
            # Create a table of detections
            det_data = []
            for det in summary['detections']:
                det_data.append({
                    'Class': det['class_name'],
                    'Confidence': f"{det['confidence']:.1%}",
                    'x1': int(det['bbox']['x1']),
                    'y1': int(det['bbox']['y1']),
                    'x2': int(det['bbox']['x2']),
                    'y2': int(det['bbox']['y2'])
                })
            
            df = pd.DataFrame(det_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No objects detected in this image.")
    
    # Class distribution chart
    st.markdown("#### 📊 Class Distribution")
    
    if summary['class_counts']:
        # Create bar chart
        classes = list(summary['class_counts'].keys())
        counts = list(summary['class_counts'].values())
        
        # Color mapping
        colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#43e97b']
        
        fig = px.bar(
            x=classes,
            y=counts,
            title="Detected Debris by Class",
            labels={'x': 'Debris Type', 'y': 'Count'},
            color=classes,
            color_discrete_sequence=colors[:len(classes)]
        )
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No detections to display.")
    
    # Pollution severity gauge
    st.markdown("#### 🎯 Pollution Severity")
    
    severity_scores = {
        'Low': 25,
        'Medium': 50,
        'High': 75,
        'Critical': 95
    }
    
    score = severity_scores.get(summary['severity'], 0)
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        title = {'text': f"Severity: {summary['severity']}"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 60], 'color': "yellow"},
                {'range': [60, 85], 'color': "orange"},
                {'range': [85, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)

# ============================================
# BATCH PROCESSING
# ============================================

if 'batch_files' in locals() and batch_files:
    st.markdown("---")
    st.markdown("### 📹 Batch Processing Results")
    
    # Process each image
    batch_results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, file in enumerate(batch_files):
        status_text.text(f"Processing {i+1}/{len(batch_files)}: {file.name}")
        
        # Save temp file
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, file.name)
        
        with open(temp_path, 'wb') as f:
            f.write(file.read())
        
        # Process
        summary = detector.get_pollution_summary(temp_path)
        summary['filename'] = file.name
        batch_results.append(summary)
        
        # Cleanup
        shutil.rmtree(temp_dir)
        progress_bar.progress((i + 1) / len(batch_files))
    
    status_text.text("✅ Batch processing complete!")
    
    # Display batch results
    st.success(f"✅ Processed {len(batch_results)} images successfully!")
    
    # Summary table
    batch_data = []
    for res in batch_results:
        batch_data.append({
            'Image': res['filename'],
            'Total Items': res['total_items'],
            'Severity': res['severity'],
            'Classes': len(res['class_counts'])
        })
    
    df_batch = pd.DataFrame(batch_data)
    st.dataframe(df_batch, use_container_width=True, hide_index=True)
    
    # Download results
    csv = df_batch.to_csv(index=False)
    st.download_button(
        label="📥 Download Results CSV",
        data=csv,
        file_name=f"oceanmind_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
<div class="footer">
    🌊 OceanMind - Marine Pollution Intelligence System
    <br>
    Powered by YOLO11s | mAP50: 70.8% | 6 Debris Classes
</div>
""", unsafe_allow_html=True)