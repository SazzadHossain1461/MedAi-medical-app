import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the medical prediction system"""
    
    # ==================== API CONFIGURATION ====================
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # ==================== MODEL PATHS ====================
    MODELS_DIR = "models"
    
    # Model file paths
    DENGUE_MODEL_PATH = os.path.join(MODELS_DIR, "dengue_model.h5")
    KIDNEY_MODEL_PATH = os.path.join(MODELS_DIR, "kidney_model.h5")
    MENTAL_HEALTH_MODEL_PATH = os.path.join(MODELS_DIR, "mental_health_model.h5")
    
    # Scaler file paths
    DENGUE_SCALER_PATH = os.path.join(MODELS_DIR, "dengue_scaler.pkl")
    KIDNEY_SCALER_PATH = os.path.join(MODELS_DIR, "kidney_scaler.pkl")
    MENTAL_HEALTH_SCALER_PATH = os.path.join(MODELS_DIR, "mental_health_scaler.pkl")
    
    # ==================== FEATURE CONFIGURATION ====================
    # All models use 13 features as per API requirements
    INPUT_FEATURES = 13
    
    # Feature names for each model (must match API endpoints exactly)
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
    
    # Feature data types and validation ranges
    FEATURE_VALIDATION = {
        'dengue': {
            'Age': {'min': 0, 'max': 120, 'type': 'int'},
            'Gender': {'min': 0, 'max': 1, 'type': 'int'},
            'Temperature': {'min': 35.0, 'max': 42.0, 'type': 'float'},
            'Platelet_Count': {'min': 0, 'max': 500000, 'type': 'int'},
            'WBC_Count': {'min': 0, 'max': 50000, 'type': 'int'}
        },
        'kidney': {
            'age': {'min': 0, 'max': 120, 'type': 'int'},
            'bp': {'min': 0, 'max': 200, 'type': 'int'},
            'sc': {'min': 0, 'max': 20, 'type': 'float'}  # serum creatinine
        },
        'mental_health': {
            'age': {'min': 0, 'max': 120, 'type': 'int'},
            'stress': {'min': 0, 'max': 10, 'type': 'int'},
            'sleep': {'min': 0, 'max': 24, 'type': 'int'}
        }
    }
    
    # ==================== DATA PATHS ====================
    DATA_DIR = "datasets"
    DENGUE_DATA_PATH = os.path.join(DATA_DIR, "dengue_data.csv")
    KIDNEY_DATA_PATH = os.path.join(DATA_DIR, "kidney_disease_data.csv")
    MENTAL_HEALTH_DATA_PATH = os.path.join(DATA_DIR, "mental_health_data.csv")
    
    # ==================== DATABASE CONFIGURATION ====================
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///instance/medai.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG
    
    # ==================== MODEL TRAINING PARAMETERS ====================
    # Neural Network Architecture
    NN_LAYERS = [128, 64, 32, 16]
    DROPOUT_RATE = 0.3
    LEARNING_RATE = 0.001
    BATCH_SIZE = 32
    EPOCHS = 100
    
    # Model-specific configurations
    MODEL_CONFIGS = {
        'dengue': {
            'layers': [128, 64, 32, 16],
            'dropout': 0.3,
            'learning_rate': 0.001
        },
        'kidney': {
            'layers': [128, 64, 32, 16],
            'dropout': 0.4,
            'learning_rate': 0.001
        },
        'mental_health': {
            'layers': [128, 64, 32, 16],
            'dropout': 0.25,
            'learning_rate': 0.001
        }
    }
    
    # ==================== RL PARAMETERS ====================
    RL_LEARNING_RATE = 0.01
    RL_GAMMA = 0.95
    RL_EPSILON = 0.1
    RL_EPISODES = 500
    
    # ==================== PREDICTION THRESHOLDS ====================
    CONFIDENCE_THRESHOLD = 0.5
    
    # Risk assessment thresholds
    RISK_THRESHOLDS = {
        'critical': 0.8,
        'high': 0.6,
        'moderate': 0.4,
        'low': 0.0
    }
    
    # ==================== LOGGING CONFIGURATION ====================
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = 'api.log'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # ==================== SECURITY CONFIGURATION ====================
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    
    # Rate limiting
    RATE_LIMIT = os.getenv('RATE_LIMIT', '100 per hour')
    
    # ==================== PERFORMANCE CONFIGURATION ====================
    # Prediction batch size for optimal performance
    PREDICTION_BATCH_SIZE = 32
    
    # Cache configuration
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # ==================== HEALTH CHECK CONFIGURATION ====================
    HEALTH_CHECK_INTERVAL = 300  # 5 minutes
    MODEL_HEALTH_TIMEOUT = 30   # 30 seconds
    
    # ==================== ERROR HANDLING ====================
    MAX_REQUEST_SIZE = 16 * 1024 * 1024  # 16MB
    REQUEST_TIMEOUT = 30  # 30 seconds
    
    @classmethod
    def validate_config(cls):
        """Validate configuration settings"""
        errors = []
        
        # Check if models directory exists
        if not os.path.exists(cls.MODELS_DIR):
            errors.append(f"Models directory '{cls.MODELS_DIR}' does not exist")
        
        # Validate feature counts
        if len(cls.DENGUE_FEATURES) != cls.INPUT_FEATURES:
            errors.append(f"Dengue features count mismatch: expected {cls.INPUT_FEATURES}, got {len(cls.DENGUE_FEATURES)}")
        
        if len(cls.KIDNEY_FEATURES) != cls.INPUT_FEATURES:
            errors.append(f"Kidney features count mismatch: expected {cls.INPUT_FEATURES}, got {len(cls.KIDNEY_FEATURES)}")
        
        if len(cls.MENTAL_HEALTH_FEATURES) != cls.INPUT_FEATURES:
            errors.append(f"Mental health features count mismatch: expected {cls.INPUT_FEATURES}, got {len(cls.MENTAL_HEALTH_FEATURES)}")
        
        # Validate port range
        if not (1024 <= cls.API_PORT <= 65535):
            errors.append(f"API port {cls.API_PORT} is not in valid range (1024-65535)")
        
        if errors:
            raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")
        
        return True
    
    @classmethod
    def get_model_config(cls, model_type):
        """Get configuration for specific model type"""
        return cls.MODEL_CONFIGS.get(model_type, cls.MODEL_CONFIGS['dengue'])
    
    @classmethod
    def get_features(cls, disease_type):
        """Get feature names for specific disease type"""
        feature_map = {
            'dengue': cls.DENGUE_FEATURES,
            'kidney': cls.KIDNEY_FEATURES,
            'mental_health': cls.MENTAL_HEALTH_FEATURES
        }
        return feature_map.get(disease_type, cls.DENGUE_FEATURES)
    
    @classmethod
    def get_model_path(cls, disease_type):
        """Get model path for specific disease type"""
        path_map = {
            'dengue': cls.DENGUE_MODEL_PATH,
            'kidney': cls.KIDNEY_MODEL_PATH,
            'mental_health': cls.MENTAL_HEALTH_MODEL_PATH
        }
        return path_map.get(disease_type)
    
    @classmethod
    def get_scaler_path(cls, disease_type):
        """Get scaler path for specific disease type"""
        path_map = {
            'dengue': cls.DENGUE_SCALER_PATH,
            'kidney': cls.KIDNEY_SCALER_PATH,
            'mental_health': cls.MENTAL_HEALTH_SCALER_PATH
        }
        return path_map.get(disease_type)


# Validate configuration on import
try:
    Config.validate_config()
    print("✅ Configuration validated successfully")
except ValueError as e:
    print(f"❌ Configuration error: {e}")
    raise