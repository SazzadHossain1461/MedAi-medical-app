"""
Main script to run the complete medical prediction system
"""

import sys
import argparse
from config import Config
import logging
import os

# Configure logging first
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def ensure_directories():
    """Ensure all necessary directories exist"""
    directories = [
        Config.MODELS_DIR, 
        'logs', 
        'datasets', 
        'database',
        'instance'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Directory ensured: {directory}")


def initialize_database():
    """Initialize database before training"""
    try:
        from database import init_db
        from api_endpoints import app
        
        # Initialize database
        init_db(app)
        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        return False


def train_dengue_model():
    """Train dengue prediction model"""
    logger.info("=" * 60)
    logger.info("Starting Dengue Model Training")
    logger.info("=" * 60)
    
    try:
        # Import here to avoid circular imports
        from training_pipeline import TrainingPipeline
        
        pipeline = TrainingPipeline('dengue')
        success = pipeline.run_full_pipeline()
        
        if success:
            logger.info("Dengue model training completed successfully")
            return True
        else:
            logger.error("Dengue model training failed")
            return False
            
    except ImportError as e:
        logger.error(f"Training pipeline not available: {str(e)}")
        print("Training pipeline module not found. Please check the implementation.")
        return False
    except Exception as e:
        logger.error(f"Error training dengue model: {str(e)}")
        return False


def train_kidney_model():
    """Train kidney disease prediction model"""
    logger.info("=" * 60)
    logger.info("Starting Kidney Disease Model Training")
    logger.info("=" * 60)
    
    try:
        from training_pipeline import TrainingPipeline
        
        pipeline = TrainingPipeline('kidney')
        success = pipeline.run_full_pipeline()
        
        if success:
            logger.info("Kidney disease model training completed successfully")
            return True
        else:
            logger.error("Kidney disease model training failed")
            return False
            
    except ImportError as e:
        logger.error(f"Training pipeline not available: {str(e)}")
        print("Training pipeline module not found. Please check the implementation.")
        return False
    except Exception as e:
        logger.error(f"Error training kidney model: {str(e)}")
        return False


def train_mental_health_model():
    """Train mental health assessment model"""
    logger.info("=" * 60)
    logger.info("Starting Mental Health Model Training")
    logger.info("=" * 60)
    
    try:
        from training_pipeline import TrainingPipeline
        
        pipeline = TrainingPipeline('mental_health')
        success = pipeline.run_full_pipeline()
        
        if success:
            logger.info("Mental health model training completed successfully")
            return True
        else:
            logger.error("Mental health model training failed")
            return False
            
    except ImportError as e:
        logger.error(f"Training pipeline not available: {str(e)}")
        print("Training pipeline module not found. Please check the implementation.")
        return False
    except Exception as e:
        logger.error(f"Error training mental health model: {str(e)}")
        return False


def train_all_models():
    """Train all models"""
    logger.info("=" * 60)
    logger.info("Starting Training for All Models")
    logger.info("=" * 60)
    
    # Initialize database first
    if not initialize_database():
        logger.error("Failed to initialize database. Training aborted.")
        return False
    
    success_count = 0
    total_models = 3
    
    try:
        print("\n" + "="*50)
        print("TRAINING ALL MEDICAL AI MODELS")
        print("="*50)
        
        # Train dengue model
        print("\n1. Training Dengue Prediction Model...")
        if train_dengue_model():
            success_count += 1
            print("   [SUCCESS] Dengue model trained successfully")
        else:
            print("   [FAILED] Dengue model training failed")
        
        # Train kidney model
        print("\n2. Training Kidney Disease Model...")
        if train_kidney_model():
            success_count += 1
            print("   [SUCCESS] Kidney model trained successfully")
        else:
            print("   [FAILED] Kidney model training failed")
        
        # Train mental health model
        print("\n3. Training Mental Health Model...")
        if train_mental_health_model():
            success_count += 1
            print("   [SUCCESS] Mental health model trained successfully")
        else:
            print("   [FAILED] Mental health model training failed")
        
        # Summary
        print("\n" + "="*50)
        print("TRAINING SUMMARY")
        print("="*50)
        print(f"Successful: {success_count}/{total_models}")
        
        if success_count == total_models:
            logger.info("All models trained successfully")
            print("SUCCESS: All models trained successfully!")
            return True
        else:
            logger.warning(f"Only {success_count}/{total_models} models trained successfully")
            print(f"WARNING: Only {success_count}/{total_models} models trained successfully")
            return False
            
    except Exception as e:
        logger.error(f"Error in training process: {str(e)}")
        print(f"ERROR: Training process failed: {str(e)}")
        return False


def start_api_server():
    """Start API server"""
    logger.info("=" * 60)
    logger.info("Starting API Server")
    logger.info("=" * 60)
    
    try:
        # Import here to avoid circular imports during training
        from api_endpoints import app, load_models
        
        # Initialize database
        initialize_database()
        
        # Load models before starting server
        if load_models():
            print(f"\nSTARTING Medical AI API Server")
            print(f"Server URL: http://{Config.API_HOST}:{Config.API_PORT}")
            print(f"Debug Mode: {Config.DEBUG}")
            print("\nAvailable Endpoints:")
            print("   POST /api/dengue/predict          - Dengue risk prediction")
            print("   POST /api/kidney/predict          - Kidney disease prediction") 
            print("   POST /api/mental-health/assessment - Mental health assessment")
            print("   GET  /api/health                  - Health check")
            print("   GET  /api/model-info              - Model information")
            print("\nPress CTRL+C to stop the server\n")
            
            logger.info(f"Server starting on {Config.API_HOST}:{Config.API_PORT}")
            app.run(
                host=Config.API_HOST, 
                port=Config.API_PORT, 
                debug=Config.DEBUG,
                use_reloader=False  # Prevent double initialization
            )
        else:
            logger.error("Failed to load models. Server not started.")
            print("ERROR: Failed to load models. Please train models first.")
            print("   Run: python main.py train-all")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Failed to start API server: {str(e)}")
        print(f"ERROR: Failed to start API server: {str(e)}")
        sys.exit(1)


def evaluate_models(model_type=None):
    """Evaluate trained models"""
    logger.info("=" * 60)
    logger.info("Starting Model Evaluation")
    logger.info("=" * 60)
    
    try:
        from model_evaluator import ModelEvaluator
        
        evaluator = ModelEvaluator()
        
        if model_type:
            print(f"\nEvaluating {model_type} model...")
            results = evaluator.evaluate_model(model_type)
        else:
            print("\nEvaluating all models...")
            results = evaluator.evaluate_all_models()
        
        # Print results
        print("\n" + "="*50)
        print("EVALUATION RESULTS")
        print("="*50)
        
        for model_name, metrics in results.items():
            print(f"\n{model_name.upper()} MODEL:")
            for metric, value in metrics.items():
                print(f"   {metric}: {value:.4f}")
                
        logger.info("Model evaluation completed")
        return True
        
    except ImportError:
        logger.warning("Model evaluator not available")
        print("NOTE: Model evaluation feature coming soon...")
        print("   (ModelEvaluator class not implemented yet)")
        return False
    except Exception as e:
        logger.error(f"Error during model evaluation: {str(e)}")
        print(f"ERROR: Evaluation failed: {str(e)}")
        return False


def check_system_health():
    """Check system health and dependencies"""
    logger.info("Performing system health check...")
    
    health_issues = []
    
    # Check Python version
    if sys.version_info < (3, 7):
        health_issues.append("Python 3.7 or higher required")
    
    # Check essential directories
    essential_dirs = [Config.MODELS_DIR, 'datasets']
    for directory in essential_dirs:
        if not os.path.exists(directory):
            health_issues.append(f"Directory '{directory}' does not exist")
    
    # Check if models exist (for API mode)
    model_files = [
        Config.DENGUE_MODEL_PATH,
        Config.KIDNEY_MODEL_PATH, 
        Config.MENTAL_HEALTH_MODEL_PATH
    ]
    
    missing_models = []
    for model_file in model_files:
        if not os.path.exists(model_file):
            missing_models.append(os.path.basename(model_file))
    
    if missing_models:
        health_issues.append(f"Missing model files: {', '.join(missing_models)}")
    
    return health_issues


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Medical Prediction System - Hybrid ML Model',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py train-all          # Train all models
  python main.py train-dengue       # Train dengue model only  
  python main.py api                # Start API server
  python main.py evaluate           # Evaluate all models
  python main.py health-check       # System health check
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Training commands
    subparsers.add_parser('train-dengue', help='Train dengue prediction model')
    subparsers.add_parser('train-kidney', help='Train kidney disease prediction model')
    subparsers.add_parser('train-mental', help='Train mental health assessment model')
    subparsers.add_parser('train-all', help='Train all models')
    
    # API command
    subparsers.add_parser('api', help='Start Flask API server')
    
    # Evaluation command
    eval_parser = subparsers.add_parser('evaluate', help='Evaluate trained models')
    eval_parser.add_argument('--model', choices=['dengue', 'kidney', 'mental'], 
                            help='Specific model to evaluate')
    
    # Health check command
    subparsers.add_parser('health-check', help='Check system health and dependencies')
    
    args = parser.parse_args()
    
    # Ensure directories exist
    ensure_directories()
    
    try:
        if args.command == 'train-dengue':
            train_dengue_model()
        elif args.command == 'train-kidney':
            train_kidney_model()
        elif args.command == 'train-mental':
            train_mental_health_model()
        elif args.command == 'train-all':
            train_all_models()
        elif args.command == 'api':
            start_api_server()
        elif args.command == 'evaluate':
            evaluate_models(args.model)
        elif args.command == 'health-check':
            issues = check_system_health()
            if issues:
                print("SYSTEM HEALTH ISSUES FOUND:")
                for issue in issues:
                    print(f"   - {issue}")
            else:
                print("SYSTEM HEALTH CHECK PASSED!")
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        print("\n\nPROCESS STOPPED BY USER")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"ERROR: Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    print("\n" + "="*60)
    print("MEDICAL AI PREDICTION SYSTEM")
    print("="*60)
    main()