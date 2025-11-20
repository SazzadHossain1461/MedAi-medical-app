import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MedicalRewardCalculator:
    """Calculate medical-specific rewards for RL agent with disease-aware optimization"""
    
    def __init__(self):
        # Disease-specific reward weights
        self.disease_weights = {
            'dengue': {
                'weight_accuracy': 0.25,
                'weight_precision': 0.20,  # Lower false positives for dengue
                'weight_recall': 0.30,     # Higher recall - don't miss dengue cases
                'weight_f1': 0.15,
                'weight_auc': 0.10,
                'false_negative_penalty': -2.0,  # Heavy penalty for missing dengue
                'false_positive_penalty': -0.5
            },
            'kidney': {
                'weight_accuracy': 0.20,
                'weight_precision': 0.25,  # Important for kidney disease staging
                'weight_recall': 0.25,
                'weight_f1': 0.20,
                'weight_auc': 0.10,
                'false_negative_penalty': -1.5,
                'false_positive_penalty': -1.0
            },
            'mental_health': {
                'weight_accuracy': 0.30,
                'weight_precision': 0.15,  # Lower precision weight for mental health
                'weight_recall': 0.25,     # Higher recall - don't miss mental health issues
                'weight_f1': 0.20,
                'weight_auc': 0.10,
                'false_negative_penalty': -1.8,  # Heavy penalty for missing mental health issues
                'false_positive_penalty': -0.3
            }
        }
    
    def calculate_medical_reward(self, y_true, y_pred, y_pred_proba=None, disease_type='dengue'):
        """Calculate comprehensive medical reward with disease-specific optimization"""
        if disease_type not in self.disease_weights:
            disease_type = 'dengue'  # Default to dengue
        
        weights = self.disease_weights[disease_type]
        
        try:
            # Handle different label formats
            y_true = np.array(y_true).flatten()
            y_pred = np.array(y_pred).flatten()
            
            # Calculate basic metrics
            accuracy = accuracy_score(y_true, y_pred)
            precision = precision_score(y_true, y_pred, zero_division=0)
            recall = recall_score(y_true, y_pred, zero_division=0)
            f1 = f1_score(y_true, y_pred, zero_division=0)
            
            # Calculate confusion matrix for penalty calculation
            tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
            
            # Base reward from metrics
            base_reward = (
                weights['weight_accuracy'] * accuracy +
                weights['weight_precision'] * precision +
                weights['weight_recall'] * recall +
                weights['weight_f1'] * f1
            )
            
            # Add AUC if probabilities available
            if y_pred_proba is not None:
                try:
                    y_pred_proba = np.array(y_pred_proba).flatten()
                    auc = roc_auc_score(y_true, y_pred_proba)
                    base_reward += weights['weight_auc'] * auc
                except Exception as e:
                    logger.warning(f"Could not calculate ROC AUC for {disease_type}: {str(e)}")
            
            # Apply medical penalties
            medical_penalty = 0
            if fn > 0:  # False negatives - missed cases
                medical_penalty += weights['false_negative_penalty'] * (fn / len(y_true))
            if fp > 0:  # False positives - unnecessary alerts
                medical_penalty += weights['false_positive_penalty'] * (fp / len(y_true))
            
            total_reward = base_reward + medical_penalty
            
            metrics = {
                'accuracy': round(accuracy, 4),
                'precision': round(precision, 4),
                'recall': round(recall, 4),
                'f1': round(f1, 4),
                'true_negatives': int(tn),
                'false_positives': int(fp),
                'false_negatives': int(fn),
                'true_positives': int(tp),
                'base_reward': round(base_reward, 4),
                'medical_penalty': round(medical_penalty, 4),
                'total_reward': round(total_reward, 4),
                'disease_type': disease_type
            }
            
            logger.debug(f"Medical reward calculated for {disease_type}: {total_reward:.4f}")
            
            return total_reward, metrics
            
        except Exception as e:
            logger.error(f"Error calculating medical reward for {disease_type}: {str(e)}")
            return -1.0, {'error': str(e)}
    
    def calculate_threshold_reward(self, y_true, y_pred_proba, threshold, disease_type='dengue'):
        """Calculate reward for specific threshold with medical context"""
        y_pred = (np.array(y_pred_proba) >= threshold).astype(int).flatten()
        reward, metrics = self.calculate_medical_reward(y_true, y_pred, y_pred_proba, disease_type)
        metrics['threshold'] = threshold
        return reward, metrics
    
    def find_optimal_threshold(self, y_true, y_pred_proba, disease_type='dengue'):
        """Find optimal prediction threshold with medical considerations"""
        best_threshold = 0.5
        best_reward = -float('inf')
        best_metrics = {}
        
        # Disease-specific threshold ranges
        threshold_ranges = {
            'dengue': np.arange(0.3, 0.8, 0.02),      # Lower thresholds for dengue (don't miss cases)
            'kidney': np.arange(0.4, 0.9, 0.02),      # Moderate thresholds for kidney
            'mental_health': np.arange(0.2, 0.7, 0.02) # Lower thresholds for mental health
        }
        
        threshold_range = threshold_ranges.get(disease_type, np.arange(0.3, 0.8, 0.05))
        
        for threshold in threshold_range:
            reward, metrics = self.calculate_threshold_reward(y_true, y_pred_proba, threshold, disease_type)
            if reward > best_reward:
                best_reward = reward
                best_threshold = threshold
                best_metrics = metrics
        
        logger.info(f"Optimal threshold for {disease_type}: {best_threshold:.3f} with reward: {best_reward:.4f}")
        
        return best_threshold, best_reward, best_metrics


class BatchRewardCalculator:
    """Calculate rewards for batch predictions"""
    
    def __init__(self):
        self.medical_calculator = MedicalRewardCalculator()
    
    def calculate_batch_rewards(self, predictions_data, disease_type='dengue'):
        """Calculate rewards for batch prediction results"""
        try:
            if not predictions_data or 'results' not in predictions_data:
                return {'error': 'Invalid predictions data format'}
            
            results = predictions_data['results']
            rewards = []
            total_reward = 0
            
            for i, result in enumerate(results):
                if result.get('status') != 'success':
                    continue
                
                # Simulate true labels for demonstration (in practice, these would be actual labels)
                # This is where you'd integrate with your labeled test data
                simulated_true_label = np.random.randint(0, 2)  # Replace with actual labels
                
                reward, metrics = self.medical_calculator.calculate_medical_reward(
                    [simulated_true_label],
                    [result.get('prediction', 0)],
                    [result.get('probability', 0.5)],
                    disease_type
                )
                
                rewards.append({
                    'record_index': i,
                    'reward': reward,
                    'metrics': metrics,
                    'prediction': result.get('prediction'),
                    'probability': result.get('probability')
                })
                total_reward += reward
            
            avg_reward = total_reward / len(rewards) if rewards else 0
            
            return {
                'total_records': len(results),
                'processed_records': len(rewards),
                'average_reward': round(avg_reward, 4),
                'total_reward': round(total_reward, 4),
                'individual_rewards': rewards,
                'disease_type': disease_type,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating batch rewards: {str(e)}")
            return {'error': str(e)}


class AdaptiveRewardSystem:
    """Adaptive reward system that learns from model performance"""
    
    def __init__(self):
        self.performance_history = {}
        self.reward_calculator = MedicalRewardCalculator()
    
    def update_performance(self, disease_type, reward, metrics):
        """Update performance history for adaptive learning"""
        if disease_type not in self.performance_history:
            self.performance_history[disease_type] = {
                'rewards': [],
                'metrics_history': [],
                'best_reward': -float('inf'),
                'adaptation_count': 0
            }
        
        history = self.performance_history[disease_type]
        history['rewards'].append(reward)
        history['metrics_history'].append(metrics)
        
        if reward > history['best_reward']:
            history['best_reward'] = reward
            history['adaptation_count'] = 0
        else:
            history['adaptation_count'] += 1
        
        # Keep only recent history
        if len(history['rewards']) > 100:
            history['rewards'] = history['rewards'][-50:]
            history['metrics_history'] = history['metrics_history'][-50:]
    
    def get_adaptive_weights(self, disease_type):
        """Get adaptive weights based on performance history"""
        if disease_type not in self.performance_history:
            return self.reward_calculator.disease_weights[disease_type]
        
        history = self.performance_history[disease_type]
        if len(history['rewards']) < 10:
            return self.reward_calculator.disease_weights[disease_type]
        
        # Analyze recent performance to adjust weights
        recent_rewards = history['rewards'][-10:]
        avg_reward = np.mean(recent_rewards)
        
        base_weights = self.reward_calculator.disease_weights[disease_type].copy()
        
        # Adaptive logic based on performance
        if avg_reward < 0.5:  # Poor performance
            # Increase recall weight to reduce false negatives
            base_weights['weight_recall'] *= 1.2
            base_weights['weight_precision'] *= 0.9
        elif history['adaptation_count'] > 5:  # Stagnant performance
            # Try different weight balance
            base_weights['weight_accuracy'] *= 0.9
            base_weights['weight_f1'] *= 1.1
        
        # Normalize weights
        total = sum(base_weights.values())
        for key in base_weights:
            if key.startswith('weight_'):
                base_weights[key] /= total
        
        logger.info(f"Adaptive weights for {disease_type}: {base_weights}")
        
        return base_weights
    
    def calculate_adaptive_reward(self, y_true, y_pred, y_pred_proba=None, disease_type='dengue'):
        """Calculate reward with adaptive weights"""
        adaptive_weights = self.get_adaptive_weights(disease_type)
        
        # Temporarily override weights
        original_weights = self.reward_calculator.disease_weights[disease_type]
        self.reward_calculator.disease_weights[disease_type] = adaptive_weights
        
        try:
            reward, metrics = self.reward_calculator.calculate_medical_reward(
                y_true, y_pred, y_pred_proba, disease_type
            )
            
            # Update performance history
            self.update_performance(disease_type, reward, metrics)
            
            return reward, metrics
        finally:
            # Restore original weights
            self.reward_calculator.disease_weights[disease_type] = original_weights


# Integration with API endpoints
def setup_reward_system():
    """Setup reward system for API integration"""
    return {
        'medical_calculator': MedicalRewardCalculator(),
        'batch_calculator': BatchRewardCalculator(),
        'adaptive_system': AdaptiveRewardSystem()
    }


# Example usage with API models
def evaluate_model_performance(models, scalers, test_data, disease_type):
    """Evaluate model performance using reward system"""
    try:
        if disease_type not in models or models[disease_type] is None:
            return {'error': f'Model for {disease_type} not available'}
        
        reward_system = setup_reward_system()
        X_test, y_test = test_data
        
        # Make predictions using API preprocessing
        predictions = []
        probabilities = []
        
        for i, sample in enumerate(X_test):
            # Scale input like in API
            scaled_input = scalers[disease_type].transform(sample.reshape(1, -1))
            prediction = models[disease_type].predict(scaled_input, verbose=0)[0]
            
            # Handle different prediction formats like API
            if len(prediction) == 1:
                prob = float(prediction[0])
                pred = 1 if prob >= 0.5 else 0
            else:
                prob = float(np.max(prediction))
                pred = np.argmax(prediction)
            
            predictions.append(pred)
            probabilities.append(prob)
        
        # Calculate reward
        reward, metrics = reward_system['medical_calculator'].calculate_medical_reward(
            y_test, predictions, probabilities, disease_type
        )
        
        # Find optimal threshold
        optimal_threshold, optimal_reward, threshold_metrics = reward_system['medical_calculator'].find_optimal_threshold(
            y_test, probabilities, disease_type
        )
        
        return {
            'disease_type': disease_type,
            'performance_reward': reward,
            'performance_metrics': metrics,
            'optimal_threshold': optimal_threshold,
            'optimal_reward': optimal_reward,
            'threshold_metrics': threshold_metrics,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error evaluating model performance for {disease_type}: {str(e)}")
        return {'error': str(e)}