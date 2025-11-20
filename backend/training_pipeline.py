import numpy as np
import pandas as pd
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os
import logging

# Import from our existing modules
from reinforcement_learning import PredictionEnvironment, QLearningAgent, DQNAgent, train_rl_agent
from reward_system import MedicalRewardCalculator, AdaptiveRewardSystem

logger = logging.getLogger(__name__)

class TrainingPipeline:
    """End-to-end training pipeline compatible with API structure"""
    
    def __init__(self, disease_type='dengue'):
        self.disease_type = disease_type
        self.model = None
        self.scaler = StandardScaler()
        self.reward_calculator = MedicalRewardCalculator()  # FIXED: No parameters needed
        self.optimal_threshold = 0.5
        
        # Use the same configuration as API
        self.models_dir = "models"
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Set paths based on disease type
        if disease_type == 'dengue':
            self.model_path = os.path.join(self.models_dir, "dengue_model.h5")
            self.scaler_path = os.path.join(self.models_dir, "dengue_scaler.pkl")
            self.features = [
                'Age', 'Gender', 'NS1', 'IgG', 'IgM', 'Area', 'AreaType', 
                'HouseType', 'District_encoded', 'Temperature', 'Symptoms', 
                'Platelet_Count', 'WBC_Count'
            ]
        elif disease_type == 'kidney':
            self.model_path = os.path.join(self.models_dir, "kidney_model.h5")
            self.scaler_path = os.path.join(self.models_dir, "kidney_scaler.pkl")
            self.features = [
                'age', 'bp', 'sg', 'al', 'su', 'bgr', 'bu', 'sc', 'sod', 
                'pot', 'hemo', 'pcv', 'wc'
            ]
        else:  # mental_health
            self.model_path = os.path.join(self.models_dir, "mental_health_model.h5")
            self.scaler_path = os.path.join(self.models_dir, "mental_health_scaler.pkl")
            self.features = [
                'age', 'gender', 'employment', 'work_env', 'stress', 'sleep', 
                'activity', 'depression', 'anxiety', 'support', 'productivity', 
                'mh_history', 'treatment'
            ]
    
    def generate_sample_data(self, n_samples=1000):
        """Generate sample training data for demonstration"""
        logger.info(f"Generating sample data for {self.disease_type}...")
        
        np.random.seed(42)
        
        # Create synthetic dataset with the expected features
        data = {}
        for feature in self.features:
            if feature in ['Age', 'age']:
                data[feature] = np.random.randint(18, 80, n_samples)
            elif feature in ['Temperature']:
                data[feature] = np.random.uniform(36.0, 41.0, n_samples)
            elif feature in ['Platelet_Count', 'WBC_Count', 'wc']:
                data[feature] = np.random.randint(50000, 400000, n_samples)
            elif feature in ['bp', 'bgr', 'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv']:
                # Kidney-specific features
                if feature == 'bp': data[feature] = np.random.randint(90, 180, n_samples)
                elif feature == 'bgr': data[feature] = np.random.uniform(70, 200, n_samples)
                elif feature == 'bu': data[feature] = np.random.uniform(10, 50, n_samples)
                elif feature == 'sc': data[feature] = np.random.uniform(0.5, 2.0, n_samples)
                elif feature == 'sod': data[feature] = np.random.uniform(135, 145, n_samples)
                elif feature == 'pot': data[feature] = np.random.uniform(3.5, 6.0, n_samples)
                elif feature == 'hemo': data[feature] = np.random.uniform(8.0, 16.0, n_samples)
                elif feature == 'pcv': data[feature] = np.random.uniform(30, 50, n_samples)
            elif feature == 'sg':
                data[feature] = np.random.choice([1.005, 1.010, 1.015, 1.020, 1.025], n_samples)
            else:
                # Categorical features
                data[feature] = np.random.randint(0, 3, n_samples)
        
        # Create target variable with some meaningful patterns
        df = pd.DataFrame(data)
        
        if self.disease_type == 'dengue':
            # Higher risk with high temperature, low platelets, positive NS1
            risk_score = (
                (df['Temperature'] > 38.5).astype(int) * 0.3 +
                (df['Platelet_Count'] < 150000).astype(int) * 0.3 +
                (df['NS1'] == 1).astype(int) * 0.4
            )
        elif self.disease_type == 'kidney':
            # Higher risk with high creatinine, low GFR (estimated), protein in urine
            risk_score = (
                (df['sc'] > 1.2).astype(int) * 0.4 +
                (df['hemo'] < 12).astype(int) * 0.3 +
                (df['al'] > 0).astype(int) * 0.3  # FIXED: Changed ast(int) to astype(int)
            )
        else:  # mental_health
            # Higher risk with high stress, depression, low support
            risk_score = (
                (df['stress'] > 1).astype(int) * 0.3 +
                (df['depression'] > 1).astype(int) * 0.3 +
                (df['anxiety'] > 1).astype(int) * 0.2 +
                (df['support'] == 0).astype(int) * 0.2
            )
        
        # Convert to binary classification
        y = (risk_score > 0.5).astype(int)
        
        return df[self.features].values, y
    
    def build_model(self):
        """Build a Keras model compatible with API expectations"""
        logger.info(f"Building model for {self.disease_type}...")
        
        model = keras.Sequential([
            keras.layers.Dense(64, activation='relu', input_shape=(len(self.features),)),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')  # Binary classification
        ])
        
        # Use metric objects instead of strings
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
        )
        
        return model
    
    def prepare_data(self, test_size=0.2, val_size=0.2):
        """Prepare data for training"""
        logger.info(f"Preparing {self.disease_type} data...")
        
        # Generate or load your actual data here
        X, y = self.generate_sample_data(1000)
        
        # Split into train, validation, and test sets
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Further split temp into train and validation
        val_ratio = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_ratio, random_state=42, stratify=y_temp
        )
        
        # Scale the features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)
        
        print(f"Data shapes - Train: {X_train_scaled.shape}, Val: {X_val_scaled.shape}, Test: {X_test_scaled.shape}")
        print(f"Class distribution - Train: {np.bincount(y_train)}, Val: {np.bincount(y_val)}, Test: {np.bincount(y_test)}")
        
        return X_train_scaled, X_val_scaled, X_test_scaled, y_train, y_val, y_test
    
    def train_supervised_model(self, X_train, X_val, X_test, y_train, y_val, y_test, epochs=100):
        """Train supervised neural network"""
        logger.info(f"Training supervised model for {self.disease_type}...")
        
        self.model = self.build_model()
        
        # Callbacks for better training
        callbacks = [
            keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
            keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5)
        ]
        
        # Train model
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=32,
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate on test set
        test_results = self.model.evaluate(X_test, y_test, verbose=0)
        
        # Extract metrics from results
        test_loss = test_results[0]
        test_accuracy = test_results[1]
        test_precision = test_results[2]
        test_recall = test_results[3]
        test_f1 = 2 * (test_precision * test_recall) / (test_precision + test_recall + 1e-7)
        
        logger.info(f"Test Metrics - Loss: {test_loss:.4f}, Accuracy: {test_accuracy:.4f}, "
                   f"Precision: {test_precision:.4f}, Recall: {test_recall:.4f}, F1: {test_f1:.4f}")
        
        print(f"\nTest Metrics:")
        print(f"Loss: {test_loss:.4f}")
        print(f"Accuracy: {test_accuracy:.4f}")
        print(f"Precision: {test_precision:.4f}")
        print(f"Recall: {test_recall:.4f}")
        print(f"F1-Score: {test_f1:.4f}")
        
        # Save model and scaler
        self.model.save(self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        
        print(f"Model saved to: {self.model_path}")
        print(f"Scaler saved to: {self.scaler_path}")
        
        return history
    
    def optimize_with_rl(self, X_test, y_test):
        """Optimize model predictions using RL"""
        logger.info(f"Optimizing {self.disease_type} model with RL...")
        
        # Get predictions from supervised model
        y_pred_proba = self.model.predict(X_test, verbose=0).flatten()
        
        # Find optimal threshold using reward calculator - FIXED: Pass disease_type as parameter
        self.optimal_threshold, best_reward, best_metrics = self.reward_calculator.find_optimal_threshold(
            y_test, y_pred_proba, self.disease_type  # FIXED: Added disease_type parameter
        )
        
        logger.info(f"Optimal threshold: {self.optimal_threshold:.3f}, Best reward: {best_reward:.4f}")
        print(f"Optimal threshold: {self.optimal_threshold:.3f}")
        print(f"Best reward: {best_reward:.4f}")
        
        # Train RL agent for threshold optimization
        rl_agent = train_rl_agent(
            {'temp': self.model},  # Pass model in expected format
            {'temp': self.scaler},  # Pass scaler in expected format
            X_test,  # Use original (unscaled) features for RL
            y_test,
            self.disease_type
        )
        
        return rl_agent, self.optimal_threshold
    
    def evaluate_with_optimal_threshold(self, X_test, y_test):
        """Evaluate model performance with optimal threshold"""
        logger.info("Evaluating with optimal threshold...")
        
        # Get probability predictions
        y_pred_proba = self.model.predict(X_test, verbose=0).flatten()
        
        # Apply optimal threshold
        y_pred_optimal = (y_pred_proba >= self.optimal_threshold).astype(int)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred_optimal)
        precision = precision_score(y_test, y_pred_optimal, zero_division=0)
        recall = recall_score(y_test, y_pred_optimal, zero_division=0)
        f1 = f1_score(y_test, y_pred_optimal, zero_division=0)
        
        # Compare with default threshold (0.5)
        y_pred_default = (y_pred_proba >= 0.5).astype(int)
        accuracy_default = accuracy_score(y_test, y_pred_default)
        
        improvement = accuracy - accuracy_default
        
        results = {
            'optimal_threshold': self.optimal_threshold,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'default_accuracy': accuracy_default,
            'improvement': improvement,
            'disease_type': self.disease_type
        }
        
        print(f"\nPerformance with Optimal Threshold ({self.optimal_threshold:.3f}):")
        print(f"Accuracy: {accuracy:.4f} (Default: {accuracy_default:.4f})")
        print(f"Improvement: {improvement:+.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-Score: {f1:.4f}")
        
        return results
    
    def run_full_pipeline(self, epochs=100):
        """Run complete training pipeline"""
        logger.info(f"Starting training pipeline for {self.disease_type.upper()}")
        print(f"\n{'='*60}")
        print(f"Starting training pipeline for {self.disease_type.upper()}")
        print(f"{'='*60}")
        
        try:
            # Prepare data
            X_train, X_val, X_test, y_train, y_val, y_test = self.prepare_data()
            
            # Train supervised model
            print(f"\n📊 Training Supervised Model...")
            history = self.train_supervised_model(X_train, X_val, X_test, y_train, y_val, y_test, epochs)
            
            # Optimize with RL
            print(f"\n🤖 Optimizing with Reinforcement Learning...")
            rl_agent, optimal_threshold = self.optimize_with_rl(X_test, y_test)
            
            # Evaluate with optimal threshold
            print(f"\n📈 Evaluating with Optimal Threshold...")
            results = self.evaluate_with_optimal_threshold(X_test, y_test)
            
            # Save training results
            training_summary = {
                'disease_type': self.disease_type,
                'optimal_threshold': optimal_threshold,
                'test_metrics': results,
                'features_used': self.features,
                'model_architecture': 'Sequential_64_32_16_1',
                'training_samples': len(X_train),
                'validation_samples': len(X_val),
                'test_samples': len(X_test)
            }
            
            # Save training summary
            summary_path = os.path.join(self.models_dir, f"{self.disease_type}_training_summary.json")
            with open(summary_path, 'w') as f:
                import json
                # Convert numpy values to Python types for JSON serialization
                summary_serializable = {}
                for key, value in training_summary.items():
                    if hasattr(value, 'tolist'):  # numpy array
                        summary_serializable[key] = value.tolist()
                    elif isinstance(value, (np.integer, np.floating)):
                        summary_serializable[key] = float(value)
                    else:
                        summary_serializable[key] = value
                json.dump(summary_serializable, f, indent=2)
            
            logger.info(f"Training pipeline completed for {self.disease_type.upper()}")
            print(f"\n{'='*60}")
            print(f"✅ Training pipeline completed for {self.disease_type.upper()}")
            print(f"📁 Model saved: {self.model_path}")
            print(f"📁 Scaler saved: {self.scaler_path}")
            print(f"📁 Summary saved: {summary_path}")
            print(f"🎯 Optimal threshold: {optimal_threshold:.3f}")
            print(f"{'='*60}\n")
            
            return training_summary
            
        except Exception as e:
            logger.error(f"Error in training pipeline for {self.disease_type}: {str(e)}")
            print(f"❌ Error in training pipeline: {str(e)}")
            raise


def train_all_models():
    """Train models for all disease types"""
    diseases = ['dengue', 'kidney', 'mental_health']
    results = {}
    
    successful = 0
    for disease in diseases:
        try:
            print(f"\n{'#'*70}")
            print(f"Training {disease.upper()} Model")
            print(f"{'#'*70}")
            
            pipeline = TrainingPipeline(disease_type=disease)
            results[disease] = pipeline.run_full_pipeline(epochs=50)  # Fewer epochs for demo
            successful += 1
            
        except Exception as e:
            print(f"Failed to train {disease} model: {str(e)}")
            results[disease] = {'error': str(e)}
    
    print(f"\n==================================================")
    print(f"TRAINING SUMMARY")
    print(f"==================================================")
    print(f"Successful: {successful}/{len(diseases)}")
    
    if successful < len(diseases):
        logger.warning(f"Only {successful}/{len(diseases)} models trained successfully")
        print(f"⚠️  Only {successful}/{len(diseases)} models trained successfully")
    else:
        print(f"✅ All {successful} models trained successfully!")
    
    return results


if __name__ == '__main__':
    # Train a specific model or all models
    import sys
    
    if len(sys.argv) > 1:
        disease_type = sys.argv[1]
        if disease_type in ['dengue', 'kidney', 'mental_health']:
            pipeline = TrainingPipeline(disease_type=disease_type)
            pipeline.run_full_pipeline(epochs=100)
        else:
            print("Invalid disease type. Use: dengue, kidney, or mental_health")
    else:
        # Train all models
        train_all_models()