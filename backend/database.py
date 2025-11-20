from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from datetime import datetime
import json
import os

db = SQLAlchemy()

class DenguePrediction(db.Model):
    """Dengue prediction records"""
    __tablename__ = 'dengue_predictions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), default='anonymous')
    age = Column(Integer)
    temperature = Column(Float)
    prediction = Column(Integer)  # 0 or 1
    probability = Column(Float)
    confidence = Column(Float)
    risk_level = Column(String(50))
    risk_category = Column(String(50))  # Added to match API
    recommendations = Column(JSON)  # Changed from Text to JSON for arrays
    input_data = Column(JSON)  # Changed from Text to JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'age': self.age,
            'temperature': self.temperature,
            'prediction': self.prediction,
            'probability': round(self.probability, 4),
            'confidence': round(self.confidence, 4),
            'risk_level': self.risk_level,
            'risk_category': self.risk_category,
            'recommendations': self.recommendations,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class KidneyDiseasePrediction(db.Model):
    """Kidney disease prediction records"""
    __tablename__ = 'kidney_predictions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), default='anonymous')
    age = Column(Integer)
    creatinine = Column(Float)
    prediction = Column(Integer)
    probability = Column(Float)
    confidence = Column(Float)
    ckd_stage = Column(String(50))
    disease_status = Column(String(100))
    gfr_range = Column(String(50))  # Added to match API
    clinical_significance = Column(Text)  # Added to match API
    recommendations = Column(JSON)  # Changed from Text to JSON
    input_data = Column(JSON)  # Changed from Text to JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'age': self.age,
            'creatinine': self.creatinine,
            'prediction': self.prediction,
            'probability': round(self.probability, 4),
            'confidence': round(self.confidence, 4),
            'ckd_stage': self.ckd_stage,
            'disease_status': self.disease_status,
            'gfr_range': self.gfr_range,
            'clinical_significance': self.clinical_significance,
            'recommendations': self.recommendations,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class MentalHealthAssessment(db.Model):
    """Mental health assessment records"""
    __tablename__ = 'mental_health_assessments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), default='anonymous')
    assessment_score = Column(Float)
    predicted_class = Column(Integer)  # Added to match API
    severity_level = Column(String(50))
    risk_category = Column(String(100))
    recommendations = Column(JSON)  # Changed from Text to JSON
    professional_help_needed = Column(Boolean, default=False)
    follow_up_frequency = Column(String(50))  # Added to match API
    input_data = Column(JSON)  # Changed from Text to JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'assessment_score': round(self.assessment_score, 4),
            'predicted_class': self.predicted_class,
            'severity_level': self.severity_level,
            'risk_category': self.risk_category,
            'recommendations': self.recommendations,
            'professional_help_needed': self.professional_help_needed,
            'follow_up_frequency': self.follow_up_frequency,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class MentalHealthTherapyPlan(db.Model):
    """Mental health therapy plan records"""
    __tablename__ = 'mental_health_therapy_plans'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), default='anonymous')
    assessment_score = Column(Float)
    severity_level = Column(String(50))
    therapy_plan = Column(JSON)  # Store entire therapy plan as JSON
    follow_up_frequency = Column(String(50))
    professional_referral = Column(Boolean, default=False)
    input_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'assessment_score': round(self.assessment_score, 4),
            'severity_level': self.severity_level,
            'therapy_plan': self.therapy_plan,
            'follow_up_frequency': self.follow_up_frequency,
            'professional_referral': self.professional_referral,
            'created_at': self.created_at.isoformat()
        }


class MentalHealthChat(db.Model):
    """Mental health chat conversations"""
    __tablename__ = 'mental_health_chats'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), default='anonymous')
    user_message = Column(Text)
    ai_response = Column(Text)
    empathy_score = Column(Float)
    conversation_depth = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_message': self.user_message,
            'ai_response': self.ai_response,
            'empathy_score': round(self.empathy_score, 4),
            'conversation_depth': self.conversation_depth,
            'created_at': self.created_at.isoformat()
        }


class RiskAssessment(db.Model):
    """Generic risk assessment records"""
    __tablename__ = 'risk_assessments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), default='anonymous')
    disease_type = Column(String(50))  # 'dengue', 'kidney', etc.
    risk_probability = Column(Float)
    risk_category = Column(String(50))
    recommended_action = Column(Text)
    preventive_measures = Column(JSON)
    recommended_tests = Column(JSON)
    lifestyle_recommendations = Column(JSON)
    input_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'disease_type': self.disease_type,
            'risk_probability': round(self.risk_probability, 4),
            'risk_category': self.risk_category,
            'recommended_action': self.recommended_action,
            'preventive_measures': self.preventive_measures,
            'recommended_tests': self.recommended_tests,
            'lifestyle_recommendations': self.lifestyle_recommendations,
            'created_at': self.created_at.isoformat()
        }


class BatchPrediction(db.Model):
    """Batch prediction records"""
    __tablename__ = 'batch_predictions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), default='anonymous')
    disease_type = Column(String(50))
    total_records = Column(Integer)
    processed_records = Column(Integer)
    results = Column(JSON)  # Store all batch results as JSON
    input_data = Column(JSON)  # Store input data samples
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'disease_type': self.disease_type,
            'total_records': self.total_records,
            'processed_records': self.processed_records,
            'results': self.results,
            'created_at': self.created_at.isoformat()
        }


class User(db.Model):
    """User profiles"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    medical_history = Column(Text)
    emergency_contact = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'age': self.age,
            'gender': self.gender,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class ModelPerformance(db.Model):
    """Track model performance metrics"""
    __tablename__ = 'model_performance'
    
    id = Column(Integer, primary_key=True)
    model_name = Column(String(100))
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    roc_auc = Column(Float)
    evaluation_date = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'model_name': self.model_name,
            'accuracy': round(self.accuracy, 4),
            'precision': round(self.precision, 4),
            'recall': round(self.recall, 4),
            'f1_score': round(self.f1_score, 4),
            'roc_auc': round(self.roc_auc, 4) if self.roc_auc else None,
            'evaluation_date': self.evaluation_date.isoformat()
        }


class PredictionHistory(db.Model):
    """General prediction history"""
    __tablename__ = 'prediction_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), default='anonymous')
    disease_type = Column(String(100))
    prediction_result = Column(Integer)
    probability = Column(Float)
    confidence = Column(Float)
    actual_diagnosis = Column(String(100), nullable=True)  # For validation
    feedback = Column(String(500), nullable=True)
    model_version = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'disease_type': self.disease_type,
            'prediction_result': self.prediction_result,
            'probability': round(self.probability, 4),
            'confidence': round(self.confidence, 4),
            'model_version': self.model_version,
            'created_at': self.created_at.isoformat()
        }


def init_db(app):
    """Initialize database with proper configuration"""
    # Configure database URI if not already set
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        # Create instance directory if it doesn't exist
        instance_path = os.path.join(os.path.dirname(__file__), 'instance')
        os.makedirs(instance_path, exist_ok=True)
        
        # Set SQLite database path
        database_path = os.path.join(instance_path, 'medai.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
    
    # Essential configuration
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the database with the app
    db.init_app(app)
    
    # Create all tables
    with app.app_context():
        db.create_all()
        print(f"✅ Database initialized successfully at: {app.config['SQLALCHEMY_DATABASE_URI']}")


def get_dengue_predictions(user_id=None, limit=10):
    """Get dengue predictions"""
    query = DenguePrediction.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    return query.order_by(DenguePrediction.created_at.desc()).limit(limit).all()


def get_kidney_predictions(user_id=None, limit=10):
    """Get kidney disease predictions"""
    query = KidneyDiseasePrediction.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    return query.order_by(KidneyDiseasePrediction.created_at.desc()).limit(limit).all()


def get_mental_health_assessments(user_id=None, limit=10):
    """Get mental health assessments"""
    query = MentalHealthAssessment.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    return query.order_by(MentalHealthAssessment.created_at.desc()).limit(limit).all()


def get_mental_health_therapy_plans(user_id=None, limit=10):
    """Get mental health therapy plans"""
    query = MentalHealthTherapyPlan.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    return query.order_by(MentalHealthTherapyPlan.created_at.desc()).limit(limit).all()


def get_risk_assessments(disease_type=None, user_id=None, limit=10):
    """Get risk assessments"""
    query = RiskAssessment.query
    if disease_type:
        query = query.filter_by(disease_type=disease_type)
    if user_id:
        query = query.filter_by(user_id=user_id)
    return query.order_by(RiskAssessment.created_at.desc()).limit(limit).all()


def add_dengue_prediction(user_id, age, temperature, prediction, probability, 
                          confidence, risk_level, risk_category, recommendations, input_data):
    """Add dengue prediction to database"""
    record = DenguePrediction(
        user_id=user_id,
        age=age,
        temperature=temperature,
        prediction=prediction,
        probability=probability,
        confidence=confidence,
        risk_level=risk_level,
        risk_category=risk_category,
        recommendations=recommendations,
        input_data=input_data
    )
    db.session.add(record)
    db.session.commit()
    return record


def add_kidney_prediction(user_id, age, creatinine, prediction, probability,
                         confidence, ckd_stage, disease_status, gfr_range, 
                         clinical_significance, recommendations, input_data):
    """Add kidney disease prediction to database"""
    record = KidneyDiseasePrediction(
        user_id=user_id,
        age=age,
        creatinine=creatinine,
        prediction=prediction,
        probability=probability,
        confidence=confidence,
        ckd_stage=ckd_stage,
        disease_status=disease_status,
        gfr_range=gfr_range,
        clinical_significance=clinical_significance,
        recommendations=recommendations,
        input_data=input_data
    )
    db.session.add(record)
    db.session.commit()
    return record


def add_mental_health_assessment(user_id, assessment_score, predicted_class,
                                 severity_level, risk_category, recommendations,
                                 professional_help_needed, follow_up_frequency, input_data):
    """Add mental health assessment to database"""
    record = MentalHealthAssessment(
        user_id=user_id,
        assessment_score=assessment_score,
        predicted_class=predicted_class,
        severity_level=severity_level,
        risk_category=risk_category,
        recommendations=recommendations,
        professional_help_needed=professional_help_needed,
        follow_up_frequency=follow_up_frequency,
        input_data=input_data
    )
    db.session.add(record)
    db.session.commit()
    return record


def add_mental_health_therapy_plan(user_id, assessment_score, severity_level,
                                   therapy_plan, follow_up_frequency, professional_referral, input_data):
    """Add mental health therapy plan to database"""
    record = MentalHealthTherapyPlan(
        user_id=user_id,
        assessment_score=assessment_score,
        severity_level=severity_level,
        therapy_plan=therapy_plan,
        follow_up_frequency=follow_up_frequency,
        professional_referral=professional_referral,
        input_data=input_data
    )
    db.session.add(record)
    db.session.commit()
    return record


def add_mental_health_chat(user_id, user_message, ai_response, empathy_score, conversation_depth):
    """Add mental health chat to database"""
    record = MentalHealthChat(
        user_id=user_id,
        user_message=user_message,
        ai_response=ai_response,
        empathy_score=empathy_score,
        conversation_depth=conversation_depth
    )
    db.session.add(record)
    db.session.commit()
    return record


def add_risk_assessment(user_id, disease_type, risk_probability, risk_category,
                       recommended_action, preventive_measures, recommended_tests,
                       lifestyle_recommendations, input_data):
    """Add risk assessment to database"""
    record = RiskAssessment(
        user_id=user_id,
        disease_type=disease_type,
        risk_probability=risk_probability,
        risk_category=risk_category,
        recommended_action=recommended_action,
        preventive_measures=preventive_measures,
        recommended_tests=recommended_tests,
        lifestyle_recommendations=lifestyle_recommendations,
        input_data=input_data
    )
    db.session.add(record)
    db.session.commit()
    return record


def add_batch_prediction(user_id, disease_type, total_records, processed_records, results, input_data):
    """Add batch prediction to database"""
    record = BatchPrediction(
        user_id=user_id,
        disease_type=disease_type,
        total_records=total_records,
        processed_records=processed_records,
        results=results,
        input_data=input_data
    )
    db.session.add(record)
    db.session.commit()
    return record


def add_model_performance(model_name, accuracy, precision, recall, f1_score, roc_auc=None):
    """Add model performance metrics"""
    record = ModelPerformance(
        model_name=model_name,
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1_score=f1_score,
        roc_auc=roc_auc
    )
    db.session.add(record)
    db.session.commit()
    return record


def create_user(username, email, age=None, gender=None):
    """Create new user"""
    user = User(
        username=username,
        email=email,
        age=age,
        gender=gender
    )
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_id(user_id):
    """Get user by ID"""
    return User.query.get(user_id)


def get_user_by_username(username):
    """Get user by username"""
    return User.query.filter_by(username=username).first()


def get_user_predictions(user_id, disease_type=None, limit=20):
    """Get all predictions for a user"""
    predictions = []
    
    # Get dengue predictions
    dengue_preds = get_dengue_predictions(user_id, limit)
    predictions.extend([{'type': 'dengue', 'data': pred.to_dict()} for pred in dengue_preds])
    
    # Get kidney predictions
    kidney_preds = get_kidney_predictions(user_id, limit)
    predictions.extend([{'type': 'kidney', 'data': pred.to_dict()} for pred in kidney_preds])
    
    # Get mental health assessments
    mh_assessments = get_mental_health_assessments(user_id, limit)
    predictions.extend([{'type': 'mental_health', 'data': pred.to_dict()} for pred in mh_assessments])
    
    # Sort by creation date and limit
    predictions.sort(key=lambda x: x['data']['created_at'], reverse=True)
    return predictions[:limit]