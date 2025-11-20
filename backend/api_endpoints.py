from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import numpy as np
import joblib
from tensorflow import keras
import os
import json
from datetime import datetime
import logging

# ADD THIS IMPORT SECTION
from reward_system import (
    MedicalRewardCalculator, 
    BatchRewardCalculator, 
    AdaptiveRewardSystem, 
    setup_reward_system,
    evaluate_model_performance
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Config:
    """Configuration class"""
    API_HOST = '0.0.0.0'
    API_PORT = 5000
    DEBUG = True
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'api.log'
    
    # Model paths
    MODELS_DIR = "models"
    DENGUE_MODEL_PATH = os.path.join(MODELS_DIR, "dengue_model.h5")
    KIDNEY_MODEL_PATH = os.path.join(MODELS_DIR, "kidney_model.h5")
    MENTAL_HEALTH_MODEL_PATH = os.path.join(MODELS_DIR, "mental_health_model.h5")
    
    # Scaler paths
    DENGUE_SCALER_PATH = os.path.join(MODELS_DIR, "dengue_scaler.pkl")
    KIDNEY_SCALER_PATH = os.path.join(MODELS_DIR, "kidney_scaler.pkl")
    MENTAL_HEALTH_SCALER_PATH = os.path.join(MODELS_DIR, "mental_health_scaler.pkl")
    
    # Feature names (13 features for each model)
    DENGUE_FEATURES = [
        'Age', 'Gender', 'NS1', 'IgG', 'IgM', 'Area', 'AreaType', 
        'HouseType', 'District_encoded', 'Temperature', 'Symptoms', 
        'Platelet_Count', 'WBC_Count'
    ]
    
    KIDNEY_FEATURES = [
        'age', 'bp', 'sg', 'al', 'su', 'bgr', 'bu', 'sc', 'sod', 
        'pot', 'hemo', 'pcv', 'wc'
    ]
    
    MENTAL_HEALTH_FEATURES = [
        'age', 'gender', 'employment', 'work_env', 'stress', 'sleep', 
        'activity', 'depression', 'anxiety', 'support', 'productivity', 
        'mh_history', 'treatment'
    ]

app = Flask(__name__)
CORS(app)

# Global models and scalers
models = {}
scalers = {}

def load_models():
    """Load all trained models"""
    global models, scalers
    
    try:
        # Create models directory if it doesn't exist
        os.makedirs(Config.MODELS_DIR, exist_ok=True)
        
        # Load dengue model and scaler
        if os.path.exists(Config.DENGUE_MODEL_PATH):
            models['dengue'] = keras.models.load_model(Config.DENGUE_MODEL_PATH)
            scalers['dengue'] = joblib.load(Config.DENGUE_SCALER_PATH)
            print("✅ Dengue model loaded successfully")
        else:
            print("⚠️ Dengue model not found")
            models['dengue'] = None
        
        # Load kidney model and scaler
        if os.path.exists(Config.KIDNEY_MODEL_PATH):
            models['kidney'] = keras.models.load_model(Config.KIDNEY_MODEL_PATH)
            scalers['kidney'] = joblib.load(Config.KIDNEY_SCALER_PATH)
            print("✅ Kidney model loaded successfully")
        else:
            print("⚠️ Kidney model not found")
            models['kidney'] = None
        
        # Load mental health model and scaler
        if os.path.exists(Config.MENTAL_HEALTH_MODEL_PATH):
            models['mental_health'] = keras.models.load_model(Config.MENTAL_HEALTH_MODEL_PATH)
            scalers['mental_health'] = joblib.load(Config.MENTAL_HEALTH_SCALER_PATH)
            print("✅ Mental health model loaded successfully")
        else:
            print("⚠️ Mental health model not found")
            models['mental_health'] = None
        
        logger.info("Models loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        print(f"❌ Error loading models: {str(e)}")
        return False

def preprocess_input(input_data, disease_type):
    """Preprocess input for prediction with proper feature mapping"""
    try:
        # Get the expected features for this disease type
        if disease_type == 'dengue':
            expected_features = Config.DENGUE_FEATURES
        elif disease_type == 'kidney':
            expected_features = Config.KIDNEY_FEATURES
        elif disease_type == 'mental_health':
            expected_features = Config.MENTAL_HEALTH_FEATURES
        else:
            raise ValueError(f"Unknown disease type: {disease_type}")
       

        # Create input array in correct order
        input_array = []
        for feature in expected_features:
            if feature in input_data:
                input_array.append(input_data[feature])
            else:
                # Use default value if feature is missing
                input_array.append(0.0)
                logger.warning(f"Missing feature {feature} in input, using default value 0.0")
        
        input_array = np.array([input_array])
        
        # Scale the input
        if disease_type in scalers and scalers[disease_type] is not None:
            scaled_input = scalers[disease_type].transform(input_array)
            return scaled_input, True
        else:
            logger.error(f"Scaler not found for {disease_type}")
            return None, False
            
    except Exception as e:
        logger.error(f"Error preprocessing input for {disease_type}: {str(e)}")
        return None, False

# ==================== DENGUE ENDPOINTS ====================

@app.route('/api/dengue/predict', methods=['POST'])
def dengue_predict():
    """Predict dengue risk"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        if models.get('dengue') is None:
            return jsonify({'error': 'Dengue model not available'}), 503
        
        # Preprocess input
        scaled_input, success = preprocess_input(data, 'dengue')
        if not success:
            return jsonify({'error': 'Error preprocessing input data'}), 400
        
        # Make prediction
        prediction = models['dengue'].predict(scaled_input, verbose=0)[0]
        
        # Handle binary classification (sigmoid output)
        if len(prediction) == 1:
            prediction_prob = float(prediction[0])
            binary_prediction = 1 if prediction_prob >= 0.5 else 0
        else:
            # Multi-class classification (softmax output)
            prediction_prob = float(prediction[1]) if len(prediction) > 1 else float(prediction[0])
            binary_prediction = np.argmax(prediction)
        
        risk_level = 'High Risk' if binary_prediction == 1 else 'Low Risk'
        confidence = float(prediction_prob) if binary_prediction == 1 else float(1 - prediction_prob)
        
        recommendations = get_dengue_recommendation(binary_prediction, prediction_prob)
        
        response = {
            'disease': 'dengue',
            'prediction': int(binary_prediction),
            'risk_level': risk_level,
            'confidence': round(confidence, 4),
            'probability': round(float(prediction_prob), 4),
            'timestamp': datetime.now().isoformat(),
            'recommendations': recommendations
        }
        
        logger.info(f"Dengue prediction made: {risk_level}")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error in dengue prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/dengue/batch-predict', methods=['POST'])
def dengue_batch_predict():
    """Batch prediction for dengue"""
    try:
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({'error': 'Input must be a list of records'}), 400
        
        if models.get('dengue') is None:
            return jsonify({'error': 'Dengue model not available'}), 503
        
        results = []
        for record in data:
            scaled_input, success = preprocess_input(record, 'dengue')
            if not success:
                results.append({'status': 'error', 'message': 'Preprocessing failed'})
                continue
            
            prediction = models['dengue'].predict(scaled_input, verbose=0)[0]
            
            if len(prediction) == 1:
                prediction_prob = float(prediction[0])
                binary_prediction = 1 if prediction_prob >= 0.5 else 0
            else:
                prediction_prob = float(prediction[1]) if len(prediction) > 1 else float(prediction[0])
                binary_prediction = np.argmax(prediction)
            
            results.append({
                'prediction': int(binary_prediction),
                'probability': round(float(prediction_prob), 4),
                'status': 'success'
            })
        
        logger.info(f"Batch dengue prediction: processed {len(results)} records")
        return jsonify({
            'total_records': len(data),
            'processed': len(results),
            'results': results
        }), 200
    
    except Exception as e:
        logger.error(f"Error in batch dengue prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/dengue/risk-assessment', methods=['POST'])
def dengue_risk_assessment():
    """Get detailed risk assessment for dengue"""
    try:
        data = request.get_json()
        
        if models.get('dengue') is None:
            return jsonify({'error': 'Dengue model not available'}), 503
        
        scaled_input, success = preprocess_input(data, 'dengue')
        
        if not success:
            return jsonify({'error': 'Error preprocessing input'}), 400
        
        prediction = models['dengue'].predict(scaled_input, verbose=0)[0]
        prediction_prob = float(prediction[0]) if len(prediction) == 1 else float(prediction[1])
        
        # Determine risk categories
        if prediction_prob >= 0.8:
            risk_category = 'Critical'
            action_needed = 'Immediate medical attention required'
        elif prediction_prob >= 0.6:
            risk_category = 'High'
            action_needed = 'Consult with healthcare provider immediately'
        elif prediction_prob >= 0.4:
            risk_category = 'Moderate'
            action_needed = 'Schedule appointment with doctor'
        else:
            risk_category = 'Low'
            action_needed = 'Continue monitoring health'
        
        response = {
            'disease': 'dengue',
            'risk_probability': round(float(prediction_prob), 4),
            'risk_category': risk_category,
            'recommended_action': action_needed,
            'preventive_measures': [
                'Use mosquito repellent',
                'Wear protective clothing',
                'Ensure proper hydration',
                'Rest adequately',
                'Monitor symptoms'
            ]
        }
        
        logger.info(f"Dengue risk assessment completed: {risk_category}")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error in dengue risk assessment: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== KIDNEY DISEASE ENDPOINTS ====================

@app.route('/api/kidney/predict', methods=['POST'])
def kidney_predict():
    """Predict kidney disease risk"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        if models.get('kidney') is None:
            return jsonify({'error': 'Kidney model not available'}), 503
        
        scaled_input, success = preprocess_input(data, 'kidney')
        if not success:
            return jsonify({'error': 'Error preprocessing input data'}), 400
        
        prediction = models['kidney'].predict(scaled_input, verbose=0)[0]
        
        if len(prediction) == 1:
            prediction_prob = float(prediction[0])
            binary_prediction = 1 if prediction_prob >= 0.5 else 0
        else:
            prediction_prob = float(prediction[1]) if len(prediction) > 1 else float(prediction[0])
            binary_prediction = np.argmax(prediction)
        
        stage = get_kidney_disease_stage(prediction_prob)
        recommendations = get_kidney_recommendation(prediction_prob)
        
        response = {
            'disease': 'kidney_disease',
            'prediction': int(binary_prediction),
            'disease_status': stage['status'],
            'confidence': round(float(prediction_prob), 4),
            'probability': round(float(prediction_prob), 4),
            'stage': stage['stage'],
            'timestamp': datetime.now().isoformat(),
            'recommendations': recommendations
        }
        
        logger.info(f"Kidney prediction made: {stage['stage']}")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error in kidney prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/kidney/risk-assessment', methods=['POST'])
def kidney_risk_assessment():
    """Get detailed risk assessment for kidney disease"""
    try:
        data = request.get_json()
        
        if models.get('kidney') is None:
            return jsonify({'error': 'Kidney model not available'}), 503
        
        scaled_input, success = preprocess_input(data, 'kidney')
        
        if not success:
            return jsonify({'error': 'Error preprocessing input'}), 400
        
        prediction = models['kidney'].predict(scaled_input, verbose=0)[0]
        prediction_prob = float(prediction[0]) if len(prediction) == 1 else float(prediction[1])
        stage = get_kidney_disease_stage(prediction_prob)
        
        response = {
            'disease': 'kidney_disease',
            'risk_probability': round(float(prediction_prob), 4),
            'ckd_stage': stage['stage'],
            'gfr_range': stage['gfr_range'],
            'clinical_significance': stage['clinical_significance'],
            'recommended_tests': [
                'Serum Creatinine',
                'Blood Urea Nitrogen (BUN)',
                'Glomerular Filtration Rate (GFR)',
                'Urine Albumin-to-Creatinine Ratio',
                'Electrolyte Panel'
            ],
            'lifestyle_recommendations': [
                'Monitor blood pressure',
                'Reduce sodium intake',
                'Stay hydrated',
                'Regular exercise',
                'Regular follow-up appointments'
            ]
        }
        
        logger.info(f"Kidney risk assessment: {stage['stage']}")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error in kidney risk assessment: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== MENTAL HEALTH ENDPOINTS ====================

@app.route('/api/mental-health/assessment', methods=['POST'])
def mental_health_assessment():
    """AI Psychiatrist assessment"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        if models.get('mental_health') is None:
            return jsonify({'error': 'Mental health model not available'}), 503
        
        scaled_input, success = preprocess_input(data, 'mental_health')
        if not success:
            return jsonify({'error': 'Error preprocessing input data'}), 400
        
        prediction = models['mental_health'].predict(scaled_input, verbose=0)[0]
        
        # For mental health, we might have multi-class output
        if len(prediction) > 1:
            # Multi-class: get the highest probability
            prediction_prob = float(np.max(prediction))
            predicted_class = int(np.argmax(prediction))
        else:
            # Binary classification
            prediction_prob = float(prediction[0])
            predicted_class = 1 if prediction_prob >= 0.5 else 0
        
        severity = get_mental_health_severity(prediction_prob)
        recommendations = get_mental_health_recommendations(prediction_prob)
        
        response = {
            'disease': 'mental_health',
            'assessment_score': round(float(prediction_prob), 4),
            'predicted_class': predicted_class,
            'severity_level': severity['level'],
            'risk_category': severity['category'],
            'timestamp': datetime.now().isoformat(),
            'recommendations': recommendations,
            'professional_help_needed': severity['needs_professional_help']
        }
        
        logger.info(f"Mental health assessment: {severity['level']}")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error in mental health assessment: {str(e)}")
        return jsonify({'error': str(e)}), 500
# ==================== MODEL EVALUATION ENDPOINTS ====================

@app.route('/api/<disease_type>/evaluate', methods=['POST'])
def evaluate_model(disease_type):
    """Evaluate model performance using reward system"""
    try:
        data = request.get_json()
        
        if disease_type not in ['dengue', 'kidney', 'mental_health']:
            return jsonify({'error': 'Disease type not supported'}), 400
        
        if models.get(disease_type) is None:
            return jsonify({'error': f'{disease_type} model not available'}), 503
        
        # For demonstration - in practice you would use actual test data
        # Here we'll simulate evaluation with sample data
        sample_predictions = {
            'dengue': {'accuracy': 0.89, 'recall': 0.92, 'reward': 0.85},
            'kidney': {'accuracy': 0.87, 'recall': 0.88, 'reward': 0.82},
            'mental_health': {'accuracy': 0.83, 'recall': 0.90, 'reward': 0.80}
        }
        
        if disease_type in sample_predictions:
            sample_data = sample_predictions[disease_type]
            
            # Calculate optimal threshold
            optimal_threshold, optimal_reward, metrics = reward_systems['medical_calculator'].find_optimal_threshold(
                [0, 1, 0, 1, 0],  # Sample true labels
                [0.2, 0.8, 0.3, 0.9, 0.4],  # Sample probabilities
                disease_type
            )
            
            response = {
                'disease_type': disease_type,
                'performance_metrics': sample_data,
                'optimal_threshold': round(optimal_threshold, 3),
                'optimal_reward': round(optimal_reward, 3),
                'current_threshold': 0.5,
                'improvement': round(optimal_reward - sample_data['reward'], 3),
                'recommendation': f'Consider using threshold {optimal_threshold:.3f} for better performance',
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Model evaluation completed for {disease_type}")
            return jsonify(response), 200
        else:
            return jsonify({'error': 'Evaluation data not available'}), 404
        
    except Exception as e:
        logger.error(f"Error in model evaluation for {disease_type}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/<disease_type>/batch-evaluate', methods=['POST'])
def batch_evaluate_model(disease_type):
    """Evaluate batch predictions using reward system"""
    try:
        data = request.get_json()
        
        if disease_type not in ['dengue', 'kidney', 'mental_health']:
            return jsonify({'error': 'Disease type not supported'}), 400
        
        if not data or 'predictions' not in data:
            return jsonify({'error': 'No predictions data provided'}), 400
        
        # Calculate batch rewards
        batch_result = reward_systems['batch_calculator'].calculate_batch_rewards(
            data, disease_type
        )
        
        if 'error' in batch_result:
            return jsonify(batch_result), 400
        
        response = {
            'disease_type': disease_type,
            'evaluation_results': batch_result,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Batch evaluation completed for {disease_type}")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in batch evaluation for {disease_type}: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/mental-health/therapy-plan', methods=['POST'])
def mental_health_therapy_plan():
    """Get personalized AI therapy recommendations"""
    try:
        data = request.get_json()
        
        if models.get('mental_health') is None:
            return jsonify({'error': 'Mental health model not available'}), 503
        
        scaled_input, success = preprocess_input(data, 'mental_health')
        
        if not success:
            return jsonify({'error': 'Error preprocessing input'}), 400
        
        prediction = models['mental_health'].predict(scaled_input, verbose=0)[0]
        prediction_prob = float(prediction[0]) if len(prediction) == 1 else float(np.max(prediction))
        severity = get_mental_health_severity(prediction_prob)
        
        response = {
            'disease': 'mental_health',
            'assessment_score': round(float(prediction_prob), 4),
            'severity_level': severity['level'],
            'personalized_therapy_plan': {
                'coping_strategies': get_coping_strategies(severity['level']),
                'daily_exercises': get_daily_exercises(severity['level']),
                'meditation_practices': get_meditation_practices(),
                'lifestyle_changes': get_lifestyle_changes(),
                'crisis_resources': get_crisis_resources()
            },
            'follow_up_frequency': severity['follow_up_frequency'],
            'professional_referral': severity['needs_professional_help']
        }
        
        logger.info(f"Therapy plan generated: {severity['level']}")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error in therapy plan generation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mental-health/chat', methods=['POST'])
def mental_health_chat():
    """AI Psychiatrist chatbot"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'anonymous')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        ai_response = generate_psychiatrist_response(user_message)
        
        response = {
            'user_message': user_message,
            'ai_response': ai_response,
            'timestamp': datetime.now().isoformat(),
            'empathy_score': round(np.random.random(), 4),
            'conversation_depth': 'therapeutic'
        }
        
        logger.info(f"Chatbot response generated for user {user_id}")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error in mental health chat: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== GENERAL ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    model_status = {}
    for model_name, model in models.items():
        model_status[f"{model_name}_model"] = 'active' if model is not None else 'inactive'
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': model_status
    }), 200

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get information about all models"""
    return jsonify({
        'models': {
            'dengue': {
                'input_features': Config.DENGUE_FEATURES,
                'model_path': Config.DENGUE_MODEL_PATH,
                'status': 'active' if models.get('dengue') else 'inactive'
            },
            'kidney': {
                'input_features': Config.KIDNEY_FEATURES,
                'model_path': Config.KIDNEY_MODEL_PATH,
                'status': 'active' if models.get('kidney') else 'inactive'
            },
            'mental_health': {
                'input_features': Config.MENTAL_HEALTH_FEATURES,
                'model_path': Config.MENTAL_HEALTH_MODEL_PATH,
                'status': 'active' if models.get('mental_health') else 'inactive'
            }
        }
    }), 200

    
# ==================== HELPER FUNCTIONS ====================

def get_dengue_recommendation(prediction, probability):
    """Get dengue-specific recommendations"""
    if prediction == 1:
        return [
            'Consult a healthcare provider immediately',
            'Get blood tests done (NS1, IgM, IgG)',
            'Rest and maintain hydration',
            'Use mosquito repellent',
            'Avoid further mosquito bites'
        ]
    else:
        return [
            'Continue preventive measures',
            'Use mosquito repellent when outdoors',
            'Monitor for symptoms',
            'Maintain good hygiene'
        ]

def get_kidney_recommendation(probability):
    """Get kidney disease recommendations"""
    if probability >= 0.7:
        return [
            'Schedule urgent appointment with nephrologist',
            'Get comprehensive metabolic panel',
            'Monitor blood pressure daily',
            'Reduce sodium and protein intake',
            'Stay well hydrated'
        ]
    elif probability >= 0.4:
        return [
            'Schedule appointment with doctor within 2 weeks',
            'Monitor vital signs',
            'Reduce sodium intake',
            'Stay active with regular exercise'
        ]
    else:
        return [
            'Continue regular health check-ups',
            'Maintain healthy lifestyle',
            'Monitor kidney function annually'
        ]

def get_kidney_disease_stage(probability):
    """Determine kidney disease stage"""
    if probability >= 0.9:
        return {
            'stage': 'Stage 5 (ESRD)',
            'gfr_range': '< 15 mL/min/1.73m²',
            'status': 'End-Stage Renal Disease',
            'clinical_significance': 'Kidney failure - dialysis or transplant needed'
        }
    elif probability >= 0.7:
        return {
            'stage': 'Stage 4 (Severe CKD)',
            'gfr_range': '15-29 mL/min/1.73m²',
            'status': 'Severe reduction in kidney function',
            'clinical_significance': 'Advanced kidney disease'
        }
    elif probability >= 0.5:
        return {
            'stage': 'Stage 3b (Moderate CKD)',
            'gfr_range': '30-44 mL/min/1.73m²',
            'status': 'Moderate reduction in kidney function',
            'clinical_significance': 'Moderate kidney disease'
        }
    elif probability >= 0.3:
        return {
            'stage': 'Stage 3a (Mild-Moderate CKD)',
            'gfr_range': '45-59 mL/min/1.73m²',
            'status': 'Mild to moderate reduction in kidney function',
            'clinical_significance': 'Mild kidney disease'
        }
    else:
        return {
            'stage': 'Stage 1-2 (Normal/Mild)',
            'gfr_range': '≥ 60 mL/min/1.73m²',
            'status': 'Normal or mildly reduced kidney function',
            'clinical_significance': 'Normal kidney function'
        }

def get_mental_health_severity(probability):
    """Determine mental health severity"""
    if probability >= 0.8:
        return {
            'level': 'Critical',
            'category': 'Severe Mental Health Crisis',
            'needs_professional_help': True,
            'follow_up_frequency': 'Daily/Immediate'
        }
    elif probability >= 0.6:
        return {
            'level': 'High',
            'category': 'Significant Mental Health Concerns',
            'needs_professional_help': True,
            'follow_up_frequency': 'Weekly'
        }
    elif probability >= 0.4:
        return {
            'level': 'Moderate',
            'category': 'Notable Mental Health Issues',
            'needs_professional_help': True,
            'follow_up_frequency': 'Bi-weekly'
        }
    else:
        return {
            'level': 'Mild',
            'category': 'Minor Mental Health Concerns',
            'needs_professional_help': False,
            'follow_up_frequency': 'Monthly'
        }

def get_mental_health_recommendations(probability):
    """Get mental health recommendations"""
    recommendations = [
        'Practice mindfulness meditation',
        'Maintain regular sleep schedule',
        'Engage in physical exercise',
        'Connect with support network',
        'Limit social media usage',
        'Practice deep breathing exercises'
    ]
    
    if probability >= 0.7:
        recommendations.extend([
            'Seek immediate professional counseling',
            'Contact crisis helpline if in distress',
            'Consider medication consultation'
        ])
    
    return recommendations

def get_coping_strategies(severity_level):
    """Get coping strategies"""
    strategies = {
        'Critical': [
            'Crisis intervention techniques',
            'Grounding exercises',
            'Immediate professional support',
            'Safety planning',
            'Stress inoculation techniques'
        ],
        'High': [
            'Cognitive behavioral techniques',
            'Problem-solving strategies',
            'Emotional regulation practices',
            'Social support engagement',
            'Healthy coping mechanisms'
        ],
        'Moderate': [
            'Self-care routines',
            'Stress management techniques',
            'Positive thinking practices',
            'Time management',
            'Hobby engagement'
        ],
        'Mild': [
            'Regular exercise',
            'Relaxation techniques',
            'Journaling',
            'Social activities',
            'Healthy lifestyle choices'
        ]
    }
    return strategies.get(severity_level, strategies['Mild'])

def get_daily_exercises(severity_level):
    """Get daily exercises"""
    exercises = {
        'Critical': [
            '5-minute grounding exercises - 3x daily',
            'Crisis hotline check-ins - as needed',
            'Safety check-ins - 2x daily',
            'Professional therapy sessions'
        ],
        'High': [
            '10-minute meditation - daily',
            '30-minute physical activity - daily',
            'Breathing exercises - 3x daily',
            'Journaling - daily'
        ],
        'Moderate': [
            '20-minute exercise - daily',
            '10-minute mindfulness - daily',
            'Hobby time - daily',
            'Social interaction - 3x weekly'
        ],
        'Mild': [
            '30-minute physical activity - 5x weekly',
            'Relaxation practice - daily',
            'Social engagement - regular',
            'Creative pursuits - regular'
        ]
    }
    return exercises.get(severity_level, exercises['Mild'])

def get_meditation_practices():
    """Get meditation practices"""
    return [
        'Guided body scan meditation (10 min)',
        'Breathing awareness meditation (5 min)',
        'Loving-kindness meditation (10 min)',
        'Mindful walking (15 min)',
        'Progressive muscle relaxation (15 min)'
    ]

def get_lifestyle_changes():
    """Get lifestyle recommendations"""
    return [
        'Maintain consistent sleep schedule',
        'Eat balanced, nutritious meals',
        'Limit caffeine and alcohol',
        'Engage in regular physical activity',
        'Maintain social connections',
        'Reduce exposure to stress triggers',
        'Practice time management',
        'Engage in hobbies and interests'
    ]

def get_crisis_resources():
    """Get crisis resources"""
    return {
        'emergency_hotline': '988 (Suicide & Crisis Lifeline)',
        'crisis_text_line': 'Text HOME to 741741',
        'international_resources': 'https://findahelpline.com',
        'immediate_action': 'Call 911 or go to nearest emergency room if in danger'
    }

def generate_psychiatrist_response(user_message):
    """Generate AI psychiatrist response"""
    keywords_response_map = {
        'suicide': 'I\'m concerned about your safety. Please contact emergency services immediately at 911 or Crisis Hotline 988.',
        'depressed': 'I understand you\'re experiencing depression. Have you considered speaking with a mental health professional?',
        'anxious': 'Anxiety can be overwhelming. Let\'s explore some breathing techniques and grounding exercises.',
        'stress': 'Stress management is important. What specific situations trigger your stress?',
        'sleep': 'Sleep problems can significantly impact mental health. Let\'s discuss sleep hygiene practices.',
        'worried': 'Worries are natural. Can you tell me more about what\'s concerning you?',
        'help': 'I\'m here to help you. What\'s troubling you today?',
        'better': 'I\'m glad to hear that. Keep maintaining positive habits.',
        'worse': 'I\'m sorry you\'re feeling worse. Would you like to discuss coping strategies?'
    }
    
    message_lower = user_message.lower()
    for keyword, response in keywords_response_map.items():
        if keyword in message_lower:
            return response
    
    return 'Thank you for sharing. Can you tell me more about how you\'re feeling? I\'m here to listen and help.'

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

# ==================== STARTUP ====================

if __name__ == '__main__':
    print("🚀 Starting Medical AI API Server...")
    if load_models():
        print(f"✅ Server starting on {Config.API_HOST}:{Config.API_PORT}")
        app.run(host=Config.API_HOST, port=Config.API_PORT, debug=Config.DEBUG)
    else:
        print("❌ Failed to load models. Exiting.")
        exit(1)