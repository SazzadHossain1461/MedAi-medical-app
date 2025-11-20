import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import logging
import os

logger = logging.getLogger(__name__)

class Config:
    """Configuration class for file paths"""
    MODELS_DIR = "models"
    DENGUE_SCALER_PATH = os.path.join(MODELS_DIR, "dengue_scaler.pkl")
    KIDNEY_SCALER_PATH = os.path.join(MODELS_DIR, "kidney_scaler.pkl")
    MENTAL_HEALTH_SCALER_PATH = os.path.join(MODELS_DIR, "mental_health_scaler.pkl")
    
    # Create models directory if it doesn't exist
    os.makedirs(MODELS_DIR, exist_ok=True)

class DataPreprocessor:
    """Handle data preprocessing for medical datasets with consistent 13 features"""
    
    def __init__(self, dataset_type='dengue'):
        self.dataset_type = dataset_type
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = None
        self.target_column = None
        self.num_features = 13  # Fixed to 13 features for all models
        
    def load_data(self, filepath):
        """Load CSV data"""
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Data loaded successfully. Shape: {df.shape}")
            print(f"✓ Data loaded successfully. Shape: {df.shape}")
            print(f"✓ Columns: {df.columns.tolist()}")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            print(f"✗ Error loading data: {str(e)}")
            return None
    
    def handle_missing_values(self, df, strategy='mean'):
        """Handle missing values in dataset"""
        if df.empty:
            return df
            
        print(f"✓ Handling missing values using {strategy} strategy...")
        
        # Handle numerical columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        if not numeric_columns.empty:
            if strategy == 'mean':
                df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
            elif strategy == 'median':
                df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
            elif strategy == 'drop':
                df = df.dropna()
        
        # Handle categorical columns
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if col in df.columns and df[col].isna().any():
                df[col] = df[col].fillna('Unknown')
                
        return df
    
    def encode_categorical_features(self, df):
        """Encode categorical variables"""
        if df.empty:
            return df
            
        categorical_columns = df.select_dtypes(include=['object']).columns
        
        print("✓ Encoding categorical features...")
        for col in categorical_columns:
            if col in df.columns and col != self.target_column:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
                print(f"  - Encoded '{col}' with {len(le.classes_)} categories")
        
        return df
    
    def normalize_features(self, X_train, X_test=None):
        """Normalize features using StandardScaler"""
        if len(X_train) == 0:
            return X_train, X_test if X_test is not None else X_train
            
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        if X_test is not None and len(X_test) > 0:
            X_test_scaled = self.scaler.transform(X_test)
            return X_train_scaled, X_test_scaled
        
        return X_train_scaled
    
    def _select_top_features(self, df, target_column, n_features=13):
        """Select top n features using correlation or importance"""
        if len(df.columns) <= n_features + 1:  # +1 for target
            return df
        
        # Calculate correlation with target for numerical features
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        numerical_cols = [col for col in numerical_cols if col != target_column]
        
        if len(numerical_cols) > 0:
            correlations = df[numerical_cols + [target_column]].corr()[target_column].abs()
            correlations = correlations.drop(target_column).sort_values(ascending=False)
            
            # Select top correlated numerical features
            top_numerical = correlations.head(min(n_features, len(correlations))).index.tolist()
        else:
            top_numerical = []
        
        # Add categorical features if needed
        categorical_cols = df.select_dtypes(include=['object']).columns
        categorical_cols = [col for col in categorical_cols if col != target_column]
        
        # If we don't have enough numerical features, add categorical ones
        remaining_slots = n_features - len(top_numerical)
        if remaining_slots > 0 and len(categorical_cols) > 0:
            top_categorical = categorical_cols[:remaining_slots]
        else:
            top_categorical = []
        
        selected_features = top_numerical + top_categorical
        
        # If still not enough, add remaining columns
        if len(selected_features) < n_features:
            all_features = [col for col in df.columns if col != target_column]
            remaining_features = [col for col in all_features if col not in selected_features]
            selected_features.extend(remaining_features[:n_features - len(selected_features)])
        
        return df[selected_features + [target_column]]
    
    def _prepare_features_target(self, df, target_column):
        """Prepare features and target variables with exactly 13 features"""
        if target_column not in df.columns:
            available_columns = ", ".join(df.columns.tolist())
            raise ValueError(f"Target column '{target_column}' not found. Available: {available_columns}")
        
        # Select exactly 13 features
        df_selected = self._select_top_features(df, target_column, self.num_features)
        
        X = df_selected.drop(columns=[target_column])
        y = df_selected[target_column]
        
        self.feature_names = X.columns.tolist()
        
        print(f"✓ Selected {len(self.feature_names)} features: {self.feature_names}")
        
        return X, y
    
    def _save_scaler(self, scaler_path):
        """Save scaler to file"""
        try:
            joblib.dump(self.scaler, scaler_path)
            logger.info(f"Scaler saved to {scaler_path}")
            print(f"✓ Scaler saved to {scaler_path}")
        except Exception as e:
            logger.error(f"Error saving scaler: {str(e)}")
            print(f"✗ Error saving scaler: {str(e)}")
    
    def preprocess_dengue_data(self, filepath):
        """Preprocess dengue dataset with 13 features"""
        print("\n=== PREPROCESSING DENGUE DATA (13 FEATURES) ===")
        self.target_column = 'Outcome'
        
        df = self.load_data(filepath)
        if df is None:
            return None, None, None, None
        
        df = self.handle_missing_values(df, strategy='mean')
        df = self.encode_categorical_features(df)
        
        try:
            X, y = self._prepare_features_target(df, self.target_column)
        except ValueError as e:
            logger.error(f"Error preparing features: {str(e)}")
            print(f"✗ Error preparing features: {str(e)}")
            return None, None, None, None
        
        print(f"✓ Final feature count: {X.shape[1]}")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        X_train_scaled, X_test_scaled = self.normalize_features(X_train, X_test)
        
        self._save_scaler(Config.DENGUE_SCALER_PATH)
        
        print(f"✅ Dengue preprocessing completed. Training shape: {X_train_scaled.shape}")
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def preprocess_kidney_data(self, filepath):
        """Preprocess kidney disease dataset with 13 features"""
        print("\n=== PREPROCESSING KIDNEY DATA (13 FEATURES) ===")
        self.target_column = 'Target'
        
        df = self.load_data(filepath)
        if df is None:
            return None, None, None, None
        
        # Map column names to standardized names
        column_mapping = {
            'Age of the patient': 'age',
            'Blood pressure (mm/Hg)': 'bp',
            'Specific gravity of urine': 'sg',
            'Albumin in urine': 'al',
            'Sugar in urine': 'su',
            'Red blood cells in urine': 'rbc',
            'Pus cells in urine': 'pc',
            'Pus cell clumps in urine': 'pcc',
            'Bacteria in urine': 'ba',
            'Random blood glucose level (mg/dl)': 'bgr',
            'Blood urea (mg/dl)': 'bu',
            'Serum creatinine (mg/dl)': 'sc',
            'Sodium level (mEq/L)': 'sod',
            'Potassium level (mEq/L)': 'pot',
            'Hemoglobin level (gms)': 'hemo',
            'Packed cell volume (%)': 'pcv',
            'White blood cell count (cells/cumm)': 'wc',
            'Red blood cell count (millions/cumm)': 'rc',
            'Hypertension (yes/no)': 'htn',
            'Diabetes mellitus (yes/no)': 'dm',
            'Coronary artery disease (yes/no)': 'cad',
            'Appetite (good/poor)': 'appet',
            'Pedal edema (yes/no)': 'pe',
            'Anemia (yes/no)': 'ane',
            'Target': 'ckd'
        }
        
        # Rename columns that exist in the dataframe
        existing_columns = {k: v for k, v in column_mapping.items() if k in df.columns}
        df = df.rename(columns=existing_columns)
        self.target_column = 'ckd'
        
        df = self.handle_missing_values(df, strategy='mean')
        df = self.encode_categorical_features(df)
        
        try:
            X, y = self._prepare_features_target(df, self.target_column)
        except ValueError as e:
            logger.error(f"Error preparing features: {str(e)}")
            print(f"✗ Error preparing features: {str(e)}")
            return None, None, None, None
        
        print(f"✓ Final feature count: {X.shape[1]}")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        X_train_scaled, X_test_scaled = self.normalize_features(X_train, X_test)
        
        self._save_scaler(Config.KIDNEY_SCALER_PATH)
        
        print(f"✅ Kidney preprocessing completed. Training shape: {X_train_scaled.shape}")
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def preprocess_mental_health_data(self, filepath):
        """Preprocess mental health dataset with 13 features"""
        print("\n=== PREPROCESSING MENTAL HEALTH DATA (13 FEATURES) ===")
        self.target_column = 'mental_health_risk'
        
        df = self.load_data(filepath)
        if df is None:
            return None, None, None, None
        
        # Map to standardized names
        column_mapping = {
            'age': 'age',
            'gender': 'gender',
            'employment_status': 'employment',
            'work_environment': 'work_env',
            'mental_health_history': 'mh_history',
            'seeks_treatment': 'treatment',
            'stress_level': 'stress',
            'sleep_hours': 'sleep',
            'physical_activity_days': 'activity',
            'depression_score': 'depression',
            'anxiety_score': 'anxiety',
            'social_support_score': 'support',
            'productivity_score': 'productivity',
            'mental_health_risk': 'mh_risk'
        }
        
        # Rename columns that exist
        existing_columns = {k: v for k, v in column_mapping.items() if k in df.columns}
        df = df.rename(columns=existing_columns)
        self.target_column = 'mh_risk'
        
        df = self.handle_missing_values(df, strategy='mean')
        df = self.encode_categorical_features(df)
        
        try:
            X, y = self._prepare_features_target(df, self.target_column)
        except ValueError as e:
            logger.error(f"Error preparing features: {str(e)}")
            print(f"✗ Error preparing features: {str(e)}")
            return None, None, None, None
        
        print(f"✓ Final feature count: {X.shape[1]}")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        X_train_scaled, X_test_scaled = self.normalize_features(X_train, X_test)
        
        self._save_scaler(Config.MENTAL_HEALTH_SCALER_PATH)
        
        print(f"✅ Mental health preprocessing completed. Training shape: {X_train_scaled.shape}")
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def inverse_transform(self, X_scaled):
        """Inverse transform scaled features"""
        if hasattr(self.scaler, 'inverse_transform'):
            return self.scaler.inverse_transform(X_scaled)
        return X_scaled
    
    def preprocess_prediction_input(self, input_dict, scaler_path):
        """Preprocess input for prediction"""
        try:
            if not os.path.exists(scaler_path):
                logger.error(f"Scaler file not found: {scaler_path}")
                return None
                
            scaler = joblib.load(scaler_path)
            input_array = np.array([list(input_dict.values())]).reshape(1, -1)
            return scaler.transform(input_array)
        except Exception as e:
            logger.error(f"Error preprocessing input: {str(e)}")
            return None
    
    def get_feature_names(self):
        """Get feature names"""
        return self.feature_names
    
    def get_label_encoders(self):
        """Get label encoders"""
        return self.label_encoders
    
    def get_feature_count(self):
        """Get number of features - always 13"""
        return self.num_features


# Test function
def test_all_datasets():
    """Test preprocessing for all datasets"""
    print("🧪 TESTING ALL DATASETS WITH 13 FEATURES")
    
    datasets = [
        ('dengue', 'dengue_data.csv'),
        ('kidney', 'kidney_disease.csv'),
        ('mental_health', 'mental_health_data.csv')
    ]
    
    for dataset_type, filepath in datasets:
        if os.path.exists(filepath):
            print(f"\n{'='*50}")
            print(f"Testing {dataset_type} dataset...")
            preprocessor = DataPreprocessor(dataset_type)
            
            if dataset_type == 'dengue':
                X_train, X_test, y_train, y_test = preprocessor.preprocess_dengue_data(filepath)
            elif dataset_type == 'kidney':
                X_train, X_test, y_train, y_test = preprocessor.preprocess_kidney_data(filepath)
            else:
                X_train, X_test, y_train, y_test = preprocessor.preprocess_mental_health_data(filepath)
            
            if X_train is not None:
                print(f"✅ {dataset_type}: SUCCESS - Shape: {X_train.shape}")
            else:
                print(f"❌ {dataset_type}: FAILED")
        else:
            print(f"⚠️  {dataset_type}: File not found - {filepath}")


if __name__ == "__main__":
    test_all_datasets()