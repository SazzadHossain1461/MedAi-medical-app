import numpy as np
import pandas as pd
from sklearn.metrics import (confusion_matrix, classification_report, 
                            roc_curve, auc, precision_recall_curve,
                            accuracy_score, precision_score, recall_score, 
                            f1_score, roc_auc_score, matthews_corrcoef)
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import logging

# Configure logging directly since Config is not available
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ModelEvaluator:
    """Comprehensive model evaluation utilities"""
    
    @staticmethod
    def evaluate_model(y_true, y_pred, y_pred_proba=None, model_name='Model'):
        """Comprehensive model evaluation"""
        
        metrics = {
            'model_name': model_name,
            'timestamp': datetime.now().isoformat(),
            'accuracy': float(accuracy_score(y_true, y_pred)),
            'precision': float(precision_score(y_true, y_pred, zero_division=0)),
            'recall': float(recall_score(y_true, y_pred, zero_division=0)),
            'f1_score': float(f1_score(y_true, y_pred, zero_division=0)),
            'matthews_corrcoef': float(matthews_corrcoef(y_true, y_pred))
        }
        
        if y_pred_proba is not None:
            try:
                metrics['roc_auc'] = float(roc_auc_score(y_true, y_pred_proba))
            except Exception as e:
                logger.warning(f"Could not calculate ROC AUC: {str(e)}")
                metrics['roc_auc'] = None
        
        return metrics
    
    @staticmethod
    def plot_confusion_matrix(y_true, y_pred, save_path=None):
        """Plot confusion matrix"""
        try:
            cm = confusion_matrix(y_true, y_pred)
            
            plt.figure(figsize=(8, 6))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True)
            plt.ylabel('Actual')
            plt.xlabel('Predicted')
            plt.title('Confusion Matrix')
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"Confusion matrix saved to {save_path}")
            
            plt.close()
        except Exception as e:
            logger.error(f"Error plotting confusion matrix: {str(e)}")
    
    @staticmethod
    def plot_roc_curve(y_true, y_pred_proba, save_path=None):
        """Plot ROC curve"""
        try:
            fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
            roc_auc = auc(fpr, tpr)
            
            plt.figure(figsize=(10, 8))
            plt.plot(fpr, tpr, color='darkorange', lw=2.5, 
                    label=f'ROC curve (AUC = {roc_auc:.3f})')
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate', fontsize=12)
            plt.ylabel('True Positive Rate', fontsize=12)
            plt.title('ROC Curve', fontsize=14, fontweight='bold')
            plt.legend(loc="lower right", fontsize=10)
            plt.grid(alpha=0.3)
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"ROC curve saved to {save_path}")
            
            plt.close()
        except Exception as e:
            logger.error(f"Error plotting ROC curve: {str(e)}")
    
    @staticmethod
    def plot_precision_recall_curve(y_true, y_pred_proba, save_path=None):
        """Plot precision-recall curve"""
        try:
            precision, recall, _ = precision_recall_curve(y_true, y_pred_proba)
            
            plt.figure(figsize=(10, 8))
            plt.plot(recall, precision, color='blue', lw=2.5, marker='o', markersize=4)
            plt.xlabel('Recall', fontsize=12)
            plt.ylabel('Precision', fontsize=12)
            plt.title('Precision-Recall Curve', fontsize=14, fontweight='bold')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.grid(alpha=0.3)
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"Precision-Recall curve saved to {save_path}")
            
            plt.close()
        except Exception as e:
            logger.error(f"Error plotting precision-recall curve: {str(e)}")
    
    @staticmethod
    def generate_classification_report(y_true, y_pred):
        """Generate detailed classification report"""
        report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
        return report
    
    @staticmethod
    def print_metrics(metrics):
        """Print metrics in formatted way"""
        print("\n" + "="*60)
        print("MODEL EVALUATION METRICS")
        print("="*60)
        print(f"Model: {metrics.get('model_name', 'N/A')}")
        print(f"Timestamp: {metrics.get('timestamp', 'N/A')}")
        print("-"*60)
        print(f"Accuracy:           {metrics.get('accuracy', 0):.4f}")
        print(f"Precision:          {metrics.get('precision', 0):.4f}")
        print(f"Recall:             {metrics.get('recall', 0):.4f}")
        print(f"F1 Score:           {metrics.get('f1_score', 0):.4f}")
        print(f"Matthews Corrcoef:  {metrics.get('matthews_corrcoef', 0):.4f}")
        if metrics.get('roc_auc'):
            print(f"ROC AUC:            {metrics.get('roc_auc'):.4f}")
        print("="*60 + "\n")


class DataValidator:
    """Validate input data"""
    
    @staticmethod
    def validate_prediction_input(input_dict, expected_features):
        """Validate prediction input"""
        if not isinstance(input_dict, dict):
            return False, "Input must be a dictionary"
        
        missing_features = set(expected_features) - set(input_dict.keys())
        if missing_features:
            return False, f"Missing features: {missing_features}"
        
        extra_features = set(input_dict.keys()) - set(expected_features)
        if extra_features:
            return False, f"Extra features: {extra_features}"
        
        for key, value in input_dict.items():
            try:
                float_value = float(value)
                if np.isnan(float_value) or np.isinf(float_value):
                    return False, f"Feature '{key}' contains NaN or infinity"
            except (ValueError, TypeError):
                return False, f"Feature '{key}' must be numeric, got {type(value)}"
        
        return True, "Valid"
    
    @staticmethod
    def check_missing_values(df):
        """Check for missing values"""
        missing = df.isnull().sum()
        missing_percent = (missing / len(df)) * 100
        return pd.DataFrame({
            'Missing_Count': missing,
            'Percentage': missing_percent
        })
    
    @staticmethod
    def check_data_types(df):
        """Check data types"""
        return df.dtypes
    
    @staticmethod
    def get_data_statistics(df):
        """Get data statistics"""
        return df.describe()
    
    @staticmethod
    def validate_csv_file(filepath):
        """Validate CSV file"""
        try:
            df = pd.read_csv(filepath)
            info = {
                'file_path': filepath,
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist(),
                'dtypes': df.dtypes.to_dict(),
                'missing_values': df.isnull().sum().to_dict(),
                'duplicates': df.duplicated().sum()
            }
            return True, info
        except Exception as e:
            return False, str(e)


class ReportGenerator:
    """Generate comprehensive reports"""
    
    @staticmethod
    def generate_prediction_report(prediction_data, output_file=None):
        """Generate prediction report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'prediction_data': prediction_data,
            'confidence_interpretation': ReportGenerator.interpret_confidence(prediction_data.get('confidence', 0)),
            'clinical_notes': ReportGenerator.generate_clinical_notes(prediction_data)
        }
        
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    json.dump(report, f, indent=2)
                logger.info(f"Report saved to {output_file}")
            except Exception as e:
                logger.error(f"Error saving report: {str(e)}")
        
        return report
    
    @staticmethod
    def generate_batch_report(predictions, output_file=None):
        """Generate batch prediction report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_predictions': len(predictions),
            'positive_predictions': sum(1 for p in predictions if p.get('prediction') == 1),
            'negative_predictions': sum(1 for p in predictions if p.get('prediction') == 0),
            'average_confidence': np.mean([p.get('confidence', 0) for p in predictions]),
            'predictions': predictions
        }
        
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    json.dump(report, f, indent=2)
                logger.info(f"Batch report saved to {output_file}")
            except Exception as e:
                logger.error(f"Error saving batch report: {str(e)}")
        
        return report
    
    @staticmethod
    def interpret_confidence(confidence):
        """Interpret confidence score"""
        if confidence >= 0.9:
            return "Very High Confidence"
        elif confidence >= 0.7:
            return "High Confidence"
        elif confidence >= 0.5:
            return "Moderate Confidence"
        elif confidence >= 0.3:
            return "Low Confidence"
        else:
            return "Very Low Confidence"
    
    @staticmethod
    def generate_clinical_notes(prediction_data):
        """Generate clinical notes based on prediction"""
        disease = prediction_data.get('disease', '')
        confidence = prediction_data.get('confidence', 0)
        
        notes = f"Patient risk assessment for {disease}. "
        notes += f"Model confidence: {ReportGenerator.interpret_confidence(confidence)}. "
        
        if prediction_data.get('prediction') == 1:
            notes += "Patient presents elevated risk indicators. "
            notes += "Clinical follow-up and further testing recommended."
        else:
            notes += "Patient presents low risk indicators. "
            notes += "Continue routine monitoring."
        
        return notes


# Standalone functions for backward compatibility
def interpret_confidence(confidence):
    """Interpret confidence score"""
    return ReportGenerator.interpret_confidence(confidence)

def generate_clinical_notes(prediction_data):
    """Generate clinical notes based on prediction"""
    return ReportGenerator.generate_clinical_notes(prediction_data)