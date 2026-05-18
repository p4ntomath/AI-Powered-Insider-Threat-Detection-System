"""
Model Performance Testing Script
Tests the trained insider threat detection model on various test files
"""

import pandas as pd
import joblib
from pathlib import Path
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


# ============================================================================
# CONFIGURATION
# ============================================================================

EXPECTED_FEATURES = [
    "employee_department",
    "employee_campus",
    "employee_position",
    "employee_seniority_years",
    "is_contractor",
    "employee_classification",
    "has_foreign_citizenship",
    "has_criminal_record",
    "has_medical_history",
    "employee_origin_country",
    "total_printed_pages",
    "num_printed_pages_off_hours",
    "total_files_burned",
    "burned_from_other",
    "is_abroad",
    "trip_day_number",
    "hostility_country_level",
    "num_entries",
    "num_unique_campus",
    "entry_during_weekend",
]

TEST_FILES = {
    "normal_behavior.csv": "Normal behavior (low-risk employees)",
    "suspicious_behavior.csv": "Suspicious behavior (high-risk indicators)",
    "mixed_cases.csv": "Mixed patterns (normal + suspicious)",
    "edge_cases.csv": "Edge cases (extreme values)",
    "missing_fields.csv": "Missing values (data imputation testing)",
    "missing_total_files_burned.csv": "Missing total_files_burned feature",
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_model():
    """Load the trained model."""
    try:
        model_path = Path('models') / 'insider_threat_model.pkl'
        model = joblib.load(model_path)
        print(f"✓ Model loaded from {model_path}")
        return model
    except FileNotFoundError:
        print(f"✗ Model not found at {model_path}")
        print("  Run 'python train_model.py' first to train the model")
        return None


def load_test_file(filename):
    """Load a test CSV file."""
    filepath = Path('test_files') / filename
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"✗ Test file not found: {filepath}")
        return None


def validate_features(df):
    """Validate that all required features are present."""
    missing_features = set(EXPECTED_FEATURES) - set(df.columns)
    if missing_features:
        print(f"  ⚠ Missing features: {missing_features}")
        return False
    return True


def test_file(model, filename, description):
    """Test the model on a single file."""
    print(f"\n{'='*70}")
    print(f"Testing: {filename}")
    print(f"Description: {description}")
    print(f"{'='*70}")
    
    # Load test file
    df = load_test_file(filename)
    if df is None:
        return
    
    print(f"Loaded {len(df)} records")
    
    # Validate features
    if not validate_features(df):
        print("Cannot proceed - missing required features")
        return
    
    # Select only expected features
    X_test = df[EXPECTED_FEATURES].copy()
    
    # Make predictions
    try:
        print("\nMaking predictions...")
        predictions = model.predict(X_test)
        probabilities = model.predict_proba(X_test)
        
        # Display results
        print(f"\nPredictions Summary:")
        print(f"  Total records: {len(predictions)}")
        print(f"  Normal (0): {sum(predictions == 0)}")
        print(f"  Threat (1): {sum(predictions == 1)}")
        
        # Show threat rate
        threat_rate = (sum(predictions == 1) / len(predictions)) * 100
        print(f"  Threat rate: {threat_rate:.1f}%")
        
        # Show individual predictions
        print(f"\nDetailed Predictions:")
        print("-" * 70)
        for idx, (pred, prob) in enumerate(zip(predictions, probabilities)):
            threat_label = "THREAT" if pred == 1 else "NORMAL"
            confidence = max(prob) * 100
            print(f"  Record {idx+1}: {threat_label:6s} (confidence: {confidence:.1f}%)")
        
        # Statistics
        print(f"\nConfidence Statistics:")
        print(f"  Mean confidence: {np.mean(np.max(probabilities, axis=1)) * 100:.1f}%")
        print(f"  Min confidence:  {np.min(np.max(probabilities, axis=1)) * 100:.1f}%")
        print(f"  Max confidence:  {np.max(np.max(probabilities, axis=1)) * 100:.1f}%")
        
    except Exception as e:
        print(f"✗ Error during prediction: {e}")
        return


def test_single_record():
    """Test a single record by user input."""
    print(f"\n{'='*70}")
    print("Interactive Single Record Test")
    print(f"{'='*70}")
    print("Enter values for each feature (or press Enter to skip):")
    
    model = load_model()
    if model is None:
        return
    
    record = {}
    for feature in EXPECTED_FEATURES:
        value = input(f"  {feature}: ").strip()
        if value:
            # Try to convert to numeric if possible
            try:
                record[feature] = float(value)
            except ValueError:
                record[feature] = value
        else:
            record[feature] = None
    
    # Create dataframe
    df = pd.DataFrame([record])
    
    try:
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0]
        
        threat_label = "THREAT" if prediction == 1 else "NORMAL"
        confidence = max(probability) * 100
        
        print(f"\nResult: {threat_label}")
        print(f"Confidence: {confidence:.1f}%")
        print(f"  Normal probability: {probability[0]*100:.1f}%")
        print(f"  Threat probability: {probability[1]*100:.1f}%")
        
    except Exception as e:
        print(f"✗ Error during prediction: {e}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("INSIDER THREAT DETECTION MODEL - PERFORMANCE TEST")
    print("="*70)
    
    # Load model
    model = load_model()
    if model is None:
        return
    
    print(f"\nTesting on {len(TEST_FILES)} test files...\n")
    
    # Test all files
    for filename, description in TEST_FILES.items():
        test_file(model, filename, description)
    
    # Interactive test option
    print(f"\n{'='*70}")
    interactive = input("\nDo you want to test a single record? (y/n): ").strip().lower()
    if interactive == 'y':
        test_single_record()
    
    print(f"\n{'='*70}")
    print("Testing Complete!")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
