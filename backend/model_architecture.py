import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.regularizers import l2
import logging

logger = logging.getLogger(__name__)

class MedicalModelConfig:
    """Configuration for medical models"""
    # Network architecture
    NN_LAYERS = [128, 64, 32, 16]
    DROPOUT_RATE = 0.3
    LEARNING_RATE = 0.001
    EPOCHS = 100
    BATCH_SIZE = 32
    
    # Model-specific configurations
    MODEL_CONFIGS = {
        'dengue': {
            'input_features': 13,
            'layers': [128, 64, 32, 16],
            'dropout': 0.3
        },
        'kidney': {
            'input_features': 13, 
            'layers': [128, 64, 32, 16],
            'dropout': 0.4
        },
        'mental_health': {
            'input_features': 13,
            'layers': [128, 64, 32, 16],
            'dropout': 0.25
        }
    }

class HybridMedicalModel:
    """Hybrid model combining supervised Deep Neural Networks with RL optimization"""
    
    def __init__(self, input_features=13, model_type='dengue'):
        self.input_features = input_features
        self.model_type = model_type
        self.model = None
        self.history = None
        self.config = MedicalModelConfig.MODEL_CONFIGS.get(model_type, MedicalModelConfig.MODEL_CONFIGS['dengue'])
        
    def build_supervised_network(self):
        """Build deep neural network for supervised learning"""
        layers_config = self.config['layers']
        dropout_rate = self.config['dropout']
        
        model = models.Sequential([
            layers.Input(shape=(self.input_features,)),
            
            layers.Dense(layers_config[0], activation='relu', 
                        kernel_regularizer=l2(0.001)),
            layers.BatchNormalization(),
            layers.Dropout(dropout_rate),
            
            layers.Dense(layers_config[1], activation='relu',
                        kernel_regularizer=l2(0.001)),
            layers.BatchNormalization(),
            layers.Dropout(dropout_rate),
            
            layers.Dense(layers_config[2], activation='relu',
                        kernel_regularizer=l2(0.001)),
            layers.BatchNormalization(),
            layers.Dropout(dropout_rate),
            
            layers.Dense(layers_config[3], activation='relu',
                        kernel_regularizer=l2(0.001)),
            layers.Dropout(dropout_rate),
            
            layers.Dense(1, activation='sigmoid')  # Binary classification
        ])
        
        logger.info(f"Supervised network created for {self.model_type} with {self.input_features} features")
        return model
    
    def build_attention_network(self):
        """Build neural network with attention mechanism"""
        layers_config = self.config['layers']
        dropout_rate = self.config['dropout']
        
        inputs = layers.Input(shape=(self.input_features,))
        
        # Main branch
        x = layers.Dense(layers_config[0], activation='relu')(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(dropout_rate)(x)
        
        # Attention branch
        attention = layers.Dense(layers_config[0], activation='softmax')(inputs)
        x = layers.Multiply()([x, attention])
        
        x = layers.Dense(layers_config[1], activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(dropout_rate)(x)
        
        x = layers.Dense(layers_config[2], activation='relu')(x)
        x = layers.Dropout(dropout_rate)(x)
        
        x = layers.Dense(layers_config[3], activation='relu')(x)
        
        outputs = layers.Dense(1, activation='sigmoid')(x)
        
        model = models.Model(inputs=inputs, outputs=outputs)
        logger.info(f"Attention network created for {self.model_type}")
        return model
    
    def build_multi_class_network(self, num_classes=2):
        """Build network for multi-class classification (for mental health)"""
        layers_config = self.config['layers']
        dropout_rate = self.config['dropout']
        
        model = models.Sequential([
            layers.Input(shape=(self.input_features,)),
            
            layers.Dense(layers_config[0], activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(dropout_rate),
            
            layers.Dense(layers_config[1], activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(dropout_rate),
            
            layers.Dense(layers_config[2], activation='relu'),
            layers.Dropout(dropout_rate),
            
            layers.Dense(layers_config[3], activation='relu'),
            layers.Dropout(dropout_rate),
            
            layers.Dense(num_classes, activation='softmax')  # Multi-class classification
        ])
        
        logger.info(f"Multi-class network created for {self.model_type} with {num_classes} classes")
        return model
    
    def compile_model(self, learning_rate=None, is_multi_class=False):
        """Compile the model"""
        if learning_rate is None:
            learning_rate = MedicalModelConfig.LEARNING_RATE
        
        optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
        
        if is_multi_class:
            loss = 'sparse_categorical_crossentropy'
            metrics = ['accuracy', keras.metrics.AUC()]
        else:
            loss = 'binary_crossentropy'
            metrics = ['accuracy', keras.metrics.AUC(), keras.metrics.Precision(), 
                      keras.metrics.Recall()]
        
        self.model.compile(
            optimizer=optimizer,
            loss=loss,
            metrics=metrics
        )
        logger.info(f"Model compiled with learning rate: {learning_rate}, multi-class: {is_multi_class}")
    
    def train(self, X_train, y_train, X_val, y_val, epochs=None, batch_size=None):
        """Train the model"""
        if epochs is None:
            epochs = MedicalModelConfig.EPOCHS
        if batch_size is None:
            batch_size = MedicalModelConfig.BATCH_SIZE
        
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        )
        
        reduce_lr = keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6,
            verbose=1
        )
        
        logger.info(f"Starting training for {epochs} epochs, batch size: {batch_size}")
        
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        return self.history
    
    def predict(self, X):
        """Make predictions"""
        return self.model.predict(X, verbose=0)
    
    def predict_proba(self, X):
        """Predict probabilities"""
        predictions = self.model.predict(X, verbose=0)
        # For binary classification with sigmoid, return probability of class 1
        if predictions.shape[1] == 1:
            return predictions
        else:
            # For multi-class, return probability of positive class (class 1)
            return predictions[:, 1] if predictions.shape[1] > 1 else predictions
    
    def evaluate(self, X_test, y_test):
        """Evaluate model on test set"""
        return self.model.evaluate(X_test, y_test, verbose=0)
    
    def save_model(self, filepath):
        """Save model to disk"""
        self.model.save(filepath)
        logger.info(f"Model saved to {filepath}")
        print(f"✅ Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load model from disk"""
        self.model = keras.models.load_model(filepath)
        logger.info(f"Model loaded from {filepath}")
        print(f"✅ Model loaded from {filepath}")
    
    def summary(self):
        """Print model summary"""
        if self.model:
            return self.model.summary()
        else:
            print("Model not built yet.")

# Utility function to create disease-specific models
def create_disease_model(model_type='dengue', use_attention=False, is_multi_class=False):
    """Factory function to create disease-specific models"""
    model = HybridMedicalModel(model_type=model_type)
    
    if is_multi_class:
        model.model = model.build_multi_class_network(num_classes=2)
    elif use_attention:
        model.model = model.build_attention_network()
    else:
        model.model = model.build_supervised_network()
    
    model.compile_model(is_multi_class=is_multi_class)
    return model

# Example usage:
if __name__ == "__main__":
    # Create a dengue model
    dengue_model = create_disease_model('dengue')
    dengue_model.summary()
    
    # Create a mental health model (multi-class)
    mental_health_model = create_disease_model('mental_health', is_multi_class=True)
    mental_health_model.summary()