import cv2
import numpy as np
from typing import Dict, List, Optional
import logging
from PIL import Image
import io

class ImageProcessor:
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the ImageProcessor with configuration.
        
        Args:
            config: Configuration dictionary with processing parameters
        """
        self.config = config or {
            'min_billboard_area': 5000,  # Minimum area to be considered a billboard (pixels)
            'max_billboard_area': 1000000,  # Maximum area to avoid false positives
            'confidence_threshold': 0.6,  # Minimum confidence score
            'blur_faces': True,  # Whether to blur faces in the image
            'blur_strength': 25,  # Strength of the blur (higher = more blur)
            'max_image_dimension': 2000,  # Maximum dimension for processing (pixels)
        }
        self.logger = logging.getLogger(__name__)

    def preprocess_image(self, image_data: bytes) -> np.ndarray:
        """
        Preprocess the image for analysis.
        
        Args:
            image_data: Binary image data
            
        Returns:
            Preprocessed image as a numpy array
        """
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Resize if too large (for performance)
            h, w = img.shape[:2]
            max_dim = self.config['max_image_dimension']
            if max(h, w) > max_dim:
                scale = max_dim / max(h, w)
                img = cv2.resize(img, (int(w * scale), int(h * scale)))
                
            return img
        except Exception as e:
            self.logger.error(f"Error preprocessing image: {str(e)}")
            raise

    def protect_privacy(self, image: np.ndarray) -> np.ndarray:
        """
        Apply privacy protections to the image.
        
        Args:
            image: Input image as a numpy array
            
        Returns:
            Image with privacy protections applied
        """
        if not self.config['blur_faces']:
            return image
            
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Load the pre-trained face detector
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Blur detected faces
        for (x, y, w, h) in faces:
            # Expand the region slightly to ensure full face coverage
            x = max(0, x - 10)
            y = max(0, y - 10)
            w = min(image.shape[1] - x, w + 20)
            h = min(image.shape[0] - y, h + 20)
            
            # Apply blur to the face region
            face_roi = image[y:y+h, x:x+w]
            face_roi = cv2.GaussianBlur(
                face_roi, 
                (self.config['blur_strength'], self.config['blur_strength']), 
                0
            )
            image[y:y+h, x:x+w] = face_roi
            
        return image

    def detect_billboards(self, image: np.ndarray) -> List[Dict]:
        """
        Detect billboards in the image.
        
        Args:
            image: Input image as a numpy array
            
        Returns:
            List of detected billboards with their properties
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply edge detection
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            
            # Find contours
            contours, _ = cv2.findContours(
                edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
            )
            
            detected = []
            min_area = self.config['min_billboard_area']
            max_area = self.config['max_billboard_area']
            
            for contour in contours:
                # Approximate the contour
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Check if it's a quadrilateral (4 sides)
                if len(approx) == 4:
                    area = cv2.contourArea(contour)
                    if min_area < area < max_area:
                        x, y, w, h = cv2.boundingRect(contour)
                        
                        # Calculate aspect ratio (billboards are typically wider than tall)
                        aspect_ratio = float(w) / h
                        
                        # Basic confidence calculation
                        confidence = min(1.0, area / max_area * 0.8 + 0.2)
                        
                        if confidence >= self.config['confidence_threshold']:
                            detected.append({
                                'bbox': [int(x), int(y), int(w), int(h)],
                                'area': float(area),
                                'aspect_ratio': float(aspect_ratio),
                                'confidence': float(confidence)
                            })
            
            return detected
            
        except Exception as e:
            self.logger.error(f"Error detecting billboards: {str(e)}")
            return []

    def process_image(self, image_data: bytes) -> Dict:
        """
        Process an image to detect billboards while protecting privacy.
        
        Args:
            image_data: Binary image data
            
        Returns:
            Dictionary containing processing results
        """
        try:
            # Preprocess the image
            image = self.preprocess_image(image_data)
            
            # Apply privacy protections
            protected_image = self.protect_privacy(image.copy())
            
            # Detect billboards
            billboards = self.detect_billboards(protected_image)
            
            # Prepare result
            result = {
                'detected_billboards': billboards,
                'image_dimensions': {
                    'height': int(image.shape[0]),
                    'width': int(image.shape[1]),
                    'channels': int(image.shape[2]) if len(image.shape) > 2 else 1
                },
                'privacy_protected': self.config['blur_faces']
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing image: {str(e)}")
            raise

    def draw_detections(self, image: np.ndarray, detections: List[Dict]) -> bytes:
        """
        Draw detection boxes on the image.
        
        Args:
            image: Input image as a numpy array
            detections: List of detections from detect_billboards()
            
        Returns:
            Image with detections drawn as bytes (JPEG format)
        """
        try:
            # Create a copy of the image to draw on
            img_draw = image.copy()
            
            for det in detections:
                x, y, w, h = det['bbox']
                confidence = det.get('confidence', 0)
                
                # Draw rectangle
                color = (0, 255, 0)  # Green for detected billboards
                thickness = 2
                cv2.rectangle(img_draw, (x, y), (x+w, y+h), color, thickness)
                
                # Add confidence score
                label = f"Billboard: {confidence:.2f}"
                cv2.putText(
                    img_draw, label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness
                )
            
            # Convert back to bytes
            _, buffer = cv2.imencode('.jpg', img_draw)
            return buffer.tobytes()
            
        except Exception as e:
            self.logger.error(f"Error drawing detections: {str(e)}")
            raise
