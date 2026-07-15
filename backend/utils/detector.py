import os
import cv2
import json
import numpy as np
from ultralytics import YOLO
from datetime import datetime

class OceanMindDetector:
    """
    OceanMind Marine Debris Detector
    """
    def __init__(self, model_path, conf_threshold=0.4, iou_threshold=0.45):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.class_names = self.model.names
        self.class_colors = self._generate_colors(len(self.class_names))
        print(f"✅ OceanMind Detector initialized with {len(self.class_names)} classes")
    
    def _generate_colors(self, num_classes):
        """Generate distinct colors for each class"""
        colors = []
        for i in range(num_classes):
            hue = i / num_classes
            color = cv2.cvtColor(np.uint8([[[hue * 180, 255, 255]]]), cv2.COLOR_HSV2BGR)[0][0]
            colors.append(tuple(map(int, color)))
        return colors
    
    def detect(self, image_path):
        """Run detection on an image"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        results = self.model(image_path, conf=self.conf_threshold, iou=self.iou_threshold)
        return results
    
    def get_detections(self, image_path):
        """Get structured detections"""
        results = self.detect(image_path)
        detections = []
        
        if len(results) > 0 and len(results[0].boxes) > 0:
            for box in results[0].boxes:
                class_id = int(box.cls[0])
                class_name = self.class_names[class_id]
                confidence = float(box.conf[0])
                bbox = box.xyxy[0].tolist()
                
                detections.append({
                    'class_id': class_id,
                    'class_name': class_name,
                    'confidence': confidence,
                    'bbox': {
                        'x1': bbox[0],
                        'y1': bbox[1],
                        'x2': bbox[2],
                        'y2': bbox[3]
                    }
                })
        
        return detections
    
    def get_pollution_summary(self, image_path):
        """Get pollution summary"""
        detections = self.get_detections(image_path)
        
        class_counts = {}
        for det in detections:
            class_name = det['class_name']
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
        
        total_items = len(detections)
        
        # Severity based on number of items
        if total_items == 0:
            severity = "Low"
            severity_color = "🟢"
        elif total_items < 3:
            severity = "Medium"
            severity_color = "🟡"
        elif total_items < 6:
            severity = "High"
            severity_color = "🟠"
        else:
            severity = "Critical"
            severity_color = "🔴"
        
        return {
            'total_items': total_items,
            'class_counts': class_counts,
            'severity': severity,
            'severity_color': severity_color,
            'detections': detections
        }
    
    def visualize(self, image_path, save_path=None):
        """Visualize detections"""
        results = self.detect(image_path)
        annotated_img = results[0].plot()
        
        if save_path:
            os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
            cv2.imwrite(save_path, cv2.cvtColor(annotated_img, cv2.COLOR_RGB2BGR))
        
        return annotated_img
    
    def process_batch(self, image_paths, output_dir=None):
        """Process multiple images"""
        results = []
        for img_path in image_paths:
            summary = self.get_pollution_summary(img_path)
            
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                save_path = os.path.join(output_dir, f"result_{os.path.basename(img_path)}")
                self.visualize(img_path, save_path)
                summary['output_path'] = save_path
            
            results.append(summary)
        
        return results