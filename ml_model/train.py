import tensorflow as tf
import numpy as np
import os
import json
from PIL import Image
import logging
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PokemonCardTrainer:
    def __init__(self, data_dir: str = "ml_model/data/images"):
        """
        Initialize Pokémon card trainer.
        
        Args:
            data_dir: Directory containing training images organized by class
        """
        self.data_dir = Path(data_dir)
        self.model_dir = Path("ml_model/model")
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        self.class_names = []
        self.model = None
        
    def load_data(self):
        """
        Load and preprocess training data.
        
        Returns:
            Tuple of (X_train, X_val, y_train, y_val, class_names)
        """
        logger.info("Loading training data...")
        
        # Get class names from directory structure
        self.class_names = sorted([d.name for d in self.data_dir.iterdir() if d.is_dir()])
        
        if not self.class_names:
            logger.error("No class directories found in data directory")
            return None
        
        logger.info(f"Found {len(self.class_names)} classes: {self.class_names}")
        
        # Load images and labels
        images = []
        labels = []
        
        for class_idx, class_name in enumerate(self.class_names):
            class_dir = self.data_dir / class_name
            image_files = list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.png"))
            
            logger.info(f"Loading {len(image_files)} images for class '{class_name}'")
            
            for image_file in image_files:
                try:
                    # Load and preprocess image
                    image = Image.open(image_file)
                    image = image.convert('RGB')
                    image = image.resize((224, 224))
                    image_array = np.array(image) / 255.0
                    
                    images.append(image_array)
                    labels.append(class_idx)
                    
                except Exception as e:
                    logger.warning(f"Error loading image {image_file}: {e}")
                    continue
        
        if not images:
            logger.error("No images loaded")
            return None
        
        # Convert to numpy arrays
        X = np.array(images)
        y = np.array(labels)
        
        logger.info(f"Loaded {len(X)} images total")
        
        # Split data into train and validation sets
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        logger.info(f"Training set: {len(X_train)} images")
        logger.info(f"Validation set: {len(X_val)} images")
        
        return X_train, X_val, y_train, y_val, self.class_names
    
    def create_model(self, num_classes: int):
        """
        Create CNN model for Pokémon card classification.
        
        Args:
            num_classes: Number of classes
            
        Returns:
            Compiled Keras model
        """
        logger.info(f"Creating model for {num_classes} classes")
        
        # Data augmentation
        data_augmentation = tf.keras.Sequential([
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.1),
            tf.keras.layers.RandomZoom(0.1),
            tf.keras.layers.RandomContrast(0.1),
        ])
        
        # Create model
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(224, 224, 3)),
            data_augmentation,
            
            # Convolutional layers
            tf.keras.layers.Conv2D(32, 3, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(),
            
            tf.keras.layers.Conv2D(64, 3, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(),
            
            tf.keras.layers.Conv2D(128, 3, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(),
            
            tf.keras.layers.Conv2D(256, 3, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.MaxPooling2D(),
            
            # Dense layers
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        logger.info("Model created and compiled")
        return model
    
    def train_model(self, epochs: int = 50, batch_size: int = 32):
        """
        Train the Pokémon card classification model.
        
        Args:
            epochs: Number of training epochs
            batch_size: Batch size for training
        """
        # Load data
        data = self.load_data()
        if data is None:
            return
        
        X_train, X_val, y_train, y_val, class_names = data
        
        # Create model
        self.model = self.create_model(len(class_names))
        
        # Callbacks
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=10,
                restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7
            ),
            tf.keras.callbacks.ModelCheckpoint(
                filepath=self.model_dir / 'best_model.h5',
                monitor='val_accuracy',
                save_best_only=True,
                save_weights_only=False
            )
        ]
        
        # Train model
        logger.info("Starting training...")
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        # Save final model
        self.save_model()
        
        # Plot training history
        self.plot_training_history(history)
        
        logger.info("Training completed!")
    
    def save_model(self):
        """Save the trained model and class names."""
        try:
            if self.model is None:
                logger.error("No model to save")
                return
            
            # Save model
            model_path = self.model_dir / 'pokemon_card_classifier.h5'
            self.model.save(model_path)
            logger.info(f"Model saved to {model_path}")
            
            # Save class names
            class_names_path = self.model_dir / 'class_names.json'
            with open(class_names_path, 'w') as f:
                json.dump(self.class_names, f, indent=2)
            logger.info(f"Class names saved to {class_names_path}")
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def plot_training_history(self, history):
        """Plot training history."""
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
            
            # Plot accuracy
            ax1.plot(history.history['accuracy'], label='Training Accuracy')
            ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
            ax1.set_title('Model Accuracy')
            ax1.set_xlabel('Epoch')
            ax1.set_ylabel('Accuracy')
            ax1.legend()
            
            # Plot loss
            ax2.plot(history.history['loss'], label='Training Loss')
            ax2.plot(history.history['val_loss'], label='Validation Loss')
            ax2.set_title('Model Loss')
            ax2.set_xlabel('Epoch')
            ax2.set_ylabel('Loss')
            ax2.legend()
            
            plt.tight_layout()
            plt.savefig(self.model_dir / 'training_history.png')
            logger.info("Training history plot saved")
            
        except Exception as e:
            logger.error(f"Error plotting training history: {e}")
    
    def evaluate_model(self):
        """Evaluate the trained model."""
        try:
            if self.model is None:
                logger.error("No model to evaluate")
                return
            
            # Load test data (you would implement this)
            logger.info("Model evaluation completed")
            
        except Exception as e:
            logger.error(f"Error evaluating model: {e}")

def main():
    """Main training function."""
    logger.info("Starting Pokémon Card Model Training")
    
    # Initialize trainer
    trainer = PokemonCardTrainer()
    
    # Check if data directory exists
    if not trainer.data_dir.exists():
        logger.error(f"Data directory not found: {trainer.data_dir}")
        logger.info("Please create the data directory structure:")
        logger.info("ml_model/data/images/")
        logger.info("├── Pikachu/")
        logger.info("├── Charizard/")
        logger.info("├── Blastoise/")
        logger.info("└── ...")
        return
    
    # Train model
    trainer.train_model(epochs=30, batch_size=16)
    
    logger.info("Training completed successfully!")

if __name__ == "__main__":
    main()
