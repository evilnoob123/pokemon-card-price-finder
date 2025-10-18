import tensorflow as tf
import numpy as np
from PIL import Image
import logging
import os
from typing import Optional, List, Tuple
import json

logger = logging.getLogger(__name__)

class PokemonCardModel:
    def __init__(self, model_path: str = None):
        """
        Initialize Pokémon card recognition model.
        
        Args:
            model_path: Path to the trained model file
        """
        self.model = None
        self.class_names = []
        self.model_path = model_path or "ml_model/model/pokemon_card_classifier.h5"
        self.class_names_path = "ml_model/model/class_names.json"
        
        self._load_model()
    
    def _load_model(self):
        """Load the trained model and class names."""
        try:
            if os.path.exists(self.model_path):
                self.model = tf.keras.models.load_model(self.model_path)
                logger.info(f"Model loaded from {self.model_path}")
                
                # Load class names
                if os.path.exists(self.class_names_path):
                    with open(self.class_names_path, 'r') as f:
                        self.class_names = json.load(f)
                    logger.info(f"Loaded {len(self.class_names)} class names")
                else:
                    logger.warning("Class names file not found")
            else:
                logger.warning(f"Model file not found at {self.model_path}")
                logger.info("Creating a placeholder model for demonstration")
                self._create_placeholder_model()
                
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self._create_placeholder_model()
    
    def _create_placeholder_model(self):
        """Create a placeholder model for demonstration purposes."""
        try:
            # Create a simple CNN model for demonstration
            model = tf.keras.Sequential([
                tf.keras.layers.Input(shape=(224, 224, 3)),
                tf.keras.layers.Conv2D(32, 3, activation='relu'),
                tf.keras.layers.MaxPooling2D(),
                tf.keras.layers.Conv2D(64, 3, activation='relu'),
                tf.keras.layers.MaxPooling2D(),
                tf.keras.layers.Conv2D(64, 3, activation='relu'),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(64, activation='relu'),
                tf.keras.layers.Dense(10, activation='softmax')  # 10 classes for demo
            ])
            
            model.compile(
                optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy']
            )
            
            self.model = model
            self.class_names = [
                'Pikachu', 'Charizard', 'Blastoise', 'Venusaur',
                'Mewtwo', 'Mew', 'Lugia', 'Ho-Oh', 'Rayquaza', 'Arceus'
            ]
            
            logger.info("Created placeholder model for demonstration")
            
        except Exception as e:
            logger.error(f"Error creating placeholder model: {e}")
            self.model = None
    
    def predict_card(self, image_path: str) -> Optional[dict]:
        """
        Predict Pokémon card from image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with prediction results
        """
        if not self.model:
            logger.error("Model not loaded")
            return None
        
        try:
            # Load and preprocess image
            image = self._preprocess_image(image_path)
            
            if image is None:
                return None
            
            # Make prediction
            predictions = self.model.predict(np.expand_dims(image, axis=0))
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            
            # Get class name
            if predicted_class_idx < len(self.class_names):
                predicted_class = self.class_names[predicted_class_idx]
            else:
                predicted_class = f"Class_{predicted_class_idx}"
            
            result = {
                'predicted_class': predicted_class,
                'confidence': confidence,
                'all_predictions': {
                    self.class_names[i] if i < len(self.class_names) else f"Class_{i}": 
                    float(predictions[0][i]) 
                    for i in range(len(predictions[0]))
                }
            }
            
            logger.info(f"Prediction: {predicted_class} (confidence: {confidence:.2f})")
            return result
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return None
    
    def _preprocess_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Preprocess image for model input.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed image array or None
        """
        try:
            # Load image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize to model input size
            image = image.resize((224, 224))
            
            # Convert to numpy array and normalize
            image_array = np.array(image) / 255.0
            
            return image_array
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            return None
    
    def train_model(self, data_dir: str, epochs: int = 10):
        """
        Train the model on Pokémon card images.
        
        Args:
            data_dir: Directory containing training images organized by class
            epochs: Number of training epochs
        """
        try:
            # This is a simplified training function
            # In practice, you would implement proper data loading, augmentation, etc.
            
            logger.info(f"Training model on data from {data_dir}")
            logger.info("Note: This is a placeholder implementation")
            logger.info("For production use, implement proper data loading and training pipeline")
            
            # Placeholder training code
            # You would implement:
            # 1. Data loading and preprocessing
            # 2. Data augmentation
            # 3. Model compilation with appropriate loss and metrics
            # 4. Training loop with validation
            # 5. Model saving
            
            logger.info("Training completed (placeholder)")
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
    
    def save_model(self, model_path: str = None):
        """
        Save the trained model and class names.
        
        Args:
            model_path: Path to save the model
        """
        try:
            if not self.model:
                logger.error("No model to save")
                return
            
            save_path = model_path or self.model_path
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Save model
            self.model.save(save_path)
            logger.info(f"Model saved to {save_path}")
            
            # Save class names
            class_names_path = os.path.join(os.path.dirname(save_path), "class_names.json")
            with open(class_names_path, 'w') as f:
                json.dump(self.class_names, f, indent=2)
            logger.info(f"Class names saved to {class_names_path}")
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def get_model_info(self) -> dict:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        if not self.model:
            return {"status": "No model loaded"}
        
        return {
            "status": "Model loaded",
            "model_path": self.model_path,
            "num_classes": len(self.class_names),
            "class_names": self.class_names,
            "input_shape": self.model.input_shape,
            "output_shape": self.model.output_shape
        }
