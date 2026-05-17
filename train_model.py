"""
COS720: AI-Powered Insider Threat Detection System
Training Script for the Random Forest Model

This script:
1. Loads and inspects the insider threat dataset
2. Preprocesses data and handles missing values
3. Trains a Random Forest classifier
4. Evaluates model performance on test set
5. Saves the trained model and analysis results
"""

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid GUI issues
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
from sklearn.impute import SimpleImputer

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# Toggle sensitive features (ethical consideration)
USE_SENSITIVE_FEATURES = True

# Random seed for reproducibility
RANDOM_STATE = 42

# ============================================================================
# PATHS AND DIRECTORIES
# ============================================================================

def setupDirectories():
    """Create necessary directories if they don't exist."""
    paths = {
        'models': Path('models'),
        'outputs': Path('outputs'),
    }
    for path in paths.values():
        path.mkdir(exist_ok=True, parents=True)
    return paths


def getDataPath():
    """Return the path to the dataset."""
    return Path('data') / 'insider_threat_clean_dataset.csv'


# ============================================================================
# DATA LOADING AND INSPECTION
# ============================================================================

def loadDataset(dataPath):
    """
    Load the insider threat dataset.
    
    Args:
        dataPath: Path to the CSV file
        
    Returns:
        DataFrame with the loaded data
    """
    if not dataPath.exists():
        raise FileNotFoundError(
            f"Dataset not found at {dataPath}. "
            "Please ensure the dataset exists in the data/ directory."
        )
    
    print(f"Loading dataset from {dataPath}...")
    df = pd.read_csv(dataPath)
    print(f"✓ Dataset loaded successfully!")
    return df


def inspectDataset(df, outputPath):
    """
    Inspect and print dataset information.
    
    Args:
        df: DataFrame to inspect
        outputPath: Path to save the summary
        
    Returns:
        Summary string
    """
    summary = []
    summary.append("=" * 80)
    summary.append("DATASET INSPECTION SUMMARY")
    summary.append("=" * 80)
    
    # Shape
    summary.append(f"\nDataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Column names and types
    summary.append("\nColumn Names and Data Types:")
    summary.append("-" * 80)
    for col in df.columns:
        summary.append(f"  {col:<40} {str(df[col].dtype):<20}")
    
    # Missing values
    summary.append("\nMissing Values:")
    summary.append("-" * 80)
    missing = df.isnull().sum()
    if missing.sum() == 0:
        summary.append("  No missing values detected.")
    else:
        for col in missing[missing > 0].index:
            summary.append(f"  {col:<40} {missing[col]:<10} ({missing[col]/len(df)*100:.2f}%)")
    
    # Class distribution
    if 'is_malicious' in df.columns:
        summary.append("\nClass Distribution (is_malicious):")
        summary.append("-" * 80)
        class_dist = df['is_malicious'].value_counts()
        for label, count in class_dist.items():
            label_name = "Malicious" if label == 1 else "Normal"
            summary.append(f"  {label_name:<40} {count:<10} ({count/len(df)*100:.2f}%)")
    
    summary.append("\n" + "=" * 80)
    
    # Print and save
    summary_str = "\n".join(summary)
    print(summary_str)
    
    with open(outputPath, 'w') as f:
        f.write(summary_str)
    
    print(f"\n✓ Dataset summary saved to {outputPath}")
    return summary_str


# ============================================================================
# DATA PREPROCESSING
# ============================================================================

def preprocessData(df, useSensitiveFeatures=True):
    """
    Preprocess the dataset: drop irrelevant/sensitive columns and split X, y.
    
    Args:
        df: DataFrame to preprocess
        useSensitiveFeatures: Whether to include sensitive features
        
    Returns:
        Tuple of (X, y, dropped_columns)
    """
    print("\n" + "=" * 80)
    print("DATA PREPROCESSING")
    print("=" * 80)
    
    # Check if target column exists
    if 'is_malicious' not in df.columns:
        raise ValueError("Target column 'is_malicious' not found in dataset.")
    
    df = df.copy()
    
    # Drop late_exit_flag (has only one value, no predictive value)
    print("\n1. Dropping late_exit_flag (no predictive value)...")
    if 'late_exit_flag' in df.columns:
        df.drop('late_exit_flag', axis=1, inplace=True)
        print("   ✓ late_exit_flag dropped")
    else:
        print("   ⚠ late_exit_flag not found in dataset")
    
    # Drop sensitive features if configured
    droppedSensitive = []
    if not useSensitiveFeatures:
        print("\n2. Dropping sensitive features (USE_SENSITIVE_FEATURES = False)...")
        sensitiveCols = [
            'has_foreign_citizenship',
            'has_criminal_record',
            'has_medical_history',
            'employee_origin_country'
        ]
        for col in sensitiveCols:
            if col in df.columns:
                df.drop(col, axis=1, inplace=True)
                droppedSensitive.append(col)
        print(f"   ✓ Dropped {len(droppedSensitive)} sensitive features: {droppedSensitive}")
    else:
        print("\n2. Sensitive features retained (USE_SENSITIVE_FEATURES = True)")
    
    # Split features and target
    print("\n3. Splitting features and target...")
    y = df['is_malicious']
    X = df.drop('is_malicious', axis=1)
    print(f"   ✓ X shape: {X.shape}")
    print(f"   ✓ y shape: {y.shape}")
    
    droppedColumns = ['late_exit_flag'] + droppedSensitive
    
    return X, y, droppedColumns


def createPreprocessor(X_train):
    """
    Create a ColumnTransformer for preprocessing.
    
    Args:
        X_train: Training features (to identify column types)
        
    Returns:
        ColumnTransformer pipeline
    """
    print("\n4. Creating preprocessing pipeline...")
    
    # Identify numeric and categorical columns
    numericCols = X_train.select_dtypes(
        include=['int64', 'float64']
    ).columns.tolist()
    categoricalCols = X_train.select_dtypes(
        include=['object']
    ).columns.tolist()
    
    print(f"   Numeric columns: {len(numericCols)}")
    print(f"   Categorical columns: {len(categoricalCols)}")
    
    # Numeric transformer: median imputation
    numericTransformer = Pipeline(
        steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler()),
        ]
    )
    
    # Categorical transformer: most frequent imputation + one-hot encoding
    # Handle sklearn version compatibility for OneHotEncoder
    try:
        # Try sparse_output parameter (sklearn >= 1.2)
        categoricalTransformer = Pipeline(
            steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
            ]
        )
    except TypeError:
        # Fallback to sparse parameter (sklearn < 1.2)
        categoricalTransformer = Pipeline(
            steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False)),
            ]
        )
    
    # Combine transformers
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numericTransformer, numericCols),
            ('cat', categoricalTransformer, categoricalCols),
        ]
    )
    
    print("   ✓ Preprocessing pipeline created")
    return preprocessor, numericCols, categoricalCols


# ============================================================================
# MODEL TRAINING
# ============================================================================

def trainModels(X_train, y_train, preprocessor):
    """
    Train the Random Forest model using a pipeline.
    
    Args:
        X_train: Training features
        y_train: Training target
        preprocessor: ColumnTransformer for preprocessing
        
    Returns:
        Trained pipeline
    """
  
    print("MODEL TRAINING")
 
    
    modelName = 'Random Forest'
    print(f"\nTraining {modelName}...")
    
    model = Pipeline(
        steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(
                n_estimators=100,
                random_state=RANDOM_STATE,
                class_weight='balanced',
                n_jobs=-1
            ))
        ]
    )
    
    model.fit(X_train, y_train)
    print(f"✓ {modelName} trained successfully")
    
    return model


# ============================================================================
# MODEL EVALUATION
# ============================================================================

def evaluateModel(model, X_test, y_test):
    """
    Evaluate a model on test data.
    
    Args:
        model: Trained model/pipeline
        X_test: Test features
        y_test: Test target
        
    Returns:
        Dictionary with evaluation metrics and predictions
    """
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred, zero_division=0),
        'Recall': recall_score(y_test, y_pred, zero_division=0),
        'F1-Score': f1_score(y_test, y_pred, zero_division=0),
    }
    
    return metrics, y_pred, y_pred_proba


def evaluateModelPerformance(model, X_test, y_test):
    """
    Evaluate the model on test data.
    
    Args:
        model: Trained model/pipeline
        X_test: Test features
        y_test: Test target
        
    Returns:
        Tuple of (metrics dict, predictions, probabilities)
    """
 
    print("MODEL EVALUATION")
  
    
    print(f"\nEvaluating Random Forest...")
    metrics, y_pred, y_pred_proba = evaluateModel(model, X_test, y_test)
    
    print(f"  Accuracy:  {metrics['Accuracy']:.4f}")
    print(f"  Precision: {metrics['Precision']:.4f}")
    print(f"  Recall:    {metrics['Recall']:.4f}")
    print(f"  F1-Score:  {metrics['F1-Score']:.4f}")
    
    return metrics, y_pred, y_pred_proba


# ============================================================================
# SAVING RESULTS
# ============================================================================

def saveModelMetrics(metrics, outputPath):
    """Save model evaluation metrics to a summary file."""
    summary = []
    summary.append("=" * 80)
    summary.append("RANDOM FOREST MODEL - EVALUATION METRICS")
    summary.append("=" * 80)
    summary.append(f"\nAccuracy:  {metrics['Accuracy']:.4f}")
    summary.append(f"Precision: {metrics['Precision']:.4f}")
    summary.append(f"Recall:    {metrics['Recall']:.4f}")
    summary.append(f"F1-Score:  {metrics['F1-Score']:.4f}")
    summary.append("\n" + "=" * 80)
    
    summaryStr = "\n".join(summary)
    
    with open(outputPath, 'w') as f:
        f.write(summaryStr)
    
    print(f"\n✓ Model metrics saved to {outputPath}")


def savePipeline(pipeline, modelPath):
    """Save the trained pipeline to a joblib file."""
    joblib.dump(pipeline, modelPath)
    print(f"✓ Best model saved to {modelPath}")


def saveFeatureNames(X_train, featureNamesPath):
    """Save the feature names to a joblib file."""
    featureNames = X_train.columns.tolist()
    joblib.dump(featureNames, featureNamesPath)
    print(f"✓ Feature names saved to {featureNamesPath}")


def saveClassificationReport(bestModel, X_test, y_test, outputPath):
    """Save the classification report to a text file."""
    y_pred = bestModel.predict(X_test)
    report = classification_report(
        y_test, y_pred,
        target_names=['Normal/Benign', 'Malicious Insider Activity']
    )
    
    with open(outputPath, 'w') as f:
        f.write(report)
    
    print(f"✓ Classification report saved to {outputPath}")


def saveConfusionMatrixPlot(bestModel, X_test, y_test, outputPath):
    """Save confusion matrix plot as PNG."""
    y_pred = bestModel.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix - Best Model')
    plt.colorbar()
    
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, ['Normal/Benign', 'Malicious'])
    plt.yticks(tick_marks, ['Normal/Benign', 'Malicious'])
    
    # Add text annotations
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(
                j, i, format(cm[i, j], 'd'),
                ha="center", va="center",
                color="white" if cm[i, j] > cm.max() / 2 else "black"
            )
    
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(outputPath, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Confusion matrix plot saved to {outputPath}")


def saveConfusionMatrixCsv(bestModel, X_test, y_test, outputPath):
    """Save confusion matrix as CSV file."""
    y_pred = bestModel.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    
    cm_df = pd.DataFrame(
        cm,
        index=['Actual Normal', 'Actual Malicious'],
        columns=['Predicted Normal', 'Predicted Malicious']
    )
    
    cm_df.to_csv(outputPath)
    print(f"✓ Confusion matrix CSV saved to {outputPath}")


def saveBestModelSummary(metrics, outputPath):
    """
    Save the model performance summary to a file.
    
    Args:
        metrics: Dictionary with evaluation metrics
        outputPath: Path to save the summary
    """
    summary = []
    summary.append("=" * 80)
    summary.append("RANDOM FOREST MODEL - SUMMARY")
    summary.append("=" * 80)
    summary.append("\nModel: Random Forest (n_estimators=100)")
    summary.append("Classifier: RandomForestClassifier with balanced class weights")
    summary.append("\nPerformance Metrics:")
    summary.append("-" * 80)
    summary.append(f"  Accuracy:  {metrics['Accuracy']:.4f}")
    summary.append(f"  Precision: {metrics['Precision']:.4f}")
    summary.append(f"  Recall:    {metrics['Recall']:.4f}")
    summary.append(f"  F1-Score:  {metrics['F1-Score']:.4f}")
    summary.append("\n" + "=" * 80)
    
    summaryStr = "\n".join(summary)
    
    with open(outputPath, 'w') as f:
        f.write(summaryStr)
    
    print(f"✓ Model summary saved to {outputPath}")


def saveFeatureImportance(bestModel, outputPath):
    """
    Save feature importance if the model supports it.
    
    Args:
        bestModel: Trained model pipeline
        outputPath: Path to save the feature importance CSV
    """
    # Get the classifier from the pipeline
    classifier = bestModel.named_steps['classifier']
    
    # Check if the classifier has feature_importances_ attribute
    if not hasattr(classifier, 'feature_importances_'):
        print("⚠ Best model does not support feature importance")
        return
    
    # Get preprocessor to extract feature names
    preprocessor = bestModel.named_steps['preprocessor']
    
    # Get feature names after preprocessing using get_feature_names_out()
    try:
        featureNames = preprocessor.get_feature_names_out()
    except AttributeError:
        # Fallback for older sklearn versions
        print("⚠ get_feature_names_out() not available, using manual feature names")
        featureNames = None
    
    # Get feature importances
    importances = classifier.feature_importances_
    
    # Create DataFrame
    if featureNames is not None:
        importanceDF = pd.DataFrame({
            'Feature': featureNames[:len(importances)],
            'Importance': importances,
        }).sort_values('Importance', ascending=False)
    else:
        importanceDF = pd.DataFrame({
            'Feature': [f"Feature_{i}" for i in range(len(importances))],
            'Importance': importances,
        }).sort_values('Importance', ascending=False)
    
    importanceDF.to_csv(outputPath, index=False)
    print(f"✓ Feature importance saved to {outputPath}")


def saveSamplePredictions(bestModel, X_test, y_test, outputPath, nSamples=100):
    """
    Save a sample of predictions to CSV.
    
    Args:
        bestModel: Trained model pipeline
        X_test: Test features
        y_test: Test target
        outputPath: Path to save the predictions
        nSamples: Number of samples to save
    """
    # Get predictions
    y_pred = bestModel.predict(X_test)
    y_pred_proba = bestModel.predict_proba(X_test)
    
    # Take a sample with reproducible random_state
    sampleSize = min(nSamples, len(y_test))
    indices = np.random.RandomState(RANDOM_STATE).choice(
        len(y_test), sampleSize, replace=False
    )
    
    # Calculate confidence score as probability of predicted class
    confidenceScores = np.array([
        y_pred_proba[idx, int(y_pred[idx])] for idx in indices
    ])
    
    # Create results DataFrame
    resultsDF = pd.DataFrame({
        'True_Label': y_test.iloc[indices].values,
        'Predicted_Label': y_pred[indices],
        'Confidence_Score': confidenceScores,
    })
    
    # Add readable labels
    resultsDF['True_Label_Text'] = resultsDF['True_Label'].apply(
        lambda x: 'Malicious Insider Activity' if x == 1 else 'Normal / Benign Behaviour'
    )
    resultsDF['Predicted_Label_Text'] = resultsDF['Predicted_Label'].apply(
        lambda x: 'Malicious Insider Activity' if x == 1 else 'Normal / Benign Behaviour'
    )
    
    # Reorder columns
    resultsDF = resultsDF[[
        'True_Label', 'True_Label_Text',
        'Predicted_Label', 'Predicted_Label_Text',
        'Confidence_Score'
    ]]
    
    resultsDF.to_csv(outputPath, index=False)
    print(f"✓ Sample predictions saved to {outputPath}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    try:
        print("\n" + "=" * 80)
        print("INSIDER THREAT DETECTION - MODEL TRAINING")
        print("=" * 80)
        print(f"Random State: {RANDOM_STATE}")
        print(f"Use Sensitive Features: {USE_SENSITIVE_FEATURES}\n")
        
        # Setup directories
        paths = setupDirectories()
        
        # Load and inspect dataset
        dataPath = getDataPath()
        df = loadDataset(dataPath)
        inspectDataset(df, paths['outputs'] / 'dataset_summary.txt')
        
        # Preprocess data
        X, y, droppedCols = preprocessData(df, useSensitiveFeatures=USE_SENSITIVE_FEATURES)
        print(f"\n✓ Preprocessing complete. Dropped columns: {droppedCols}")
        
        # Train-test split
        print("\n5. Splitting data (80% train, 20% test with stratification)...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.2,
            stratify=y,
            random_state=RANDOM_STATE
        )
        print(f"   ✓ Training set: {X_train.shape}")
        print(f"   ✓ Test set: {X_test.shape}")
        
        # Create preprocessor
        preprocessor, numericCols, categoricalCols = createPreprocessor(X_train)
        
        # Train Random Forest model
        bestModel = trainModels(X_train, y_train, preprocessor)
        
        # Evaluate model
        metrics, y_pred, y_pred_proba = evaluateModelPerformance(bestModel, X_test, y_test)
        
        # Save best model
        savePipeline(bestModel, paths['models'] / 'insider_threat_model.pkl')
        
        # Save feature names
        saveFeatureNames(X_train, paths['models'] / 'feature_names.pkl')
        
        # Save model metrics
        saveModelMetrics(metrics, paths['outputs'] / 'model_metrics.txt')
        
        # Save classification report
        saveClassificationReport(bestModel, X_test, y_test, paths['outputs'] / 'classification_report.txt')
        
        # Save confusion matrix
        saveConfusionMatrixPlot(bestModel, X_test, y_test, paths['outputs'] / 'confusion_matrix.png')
        
        # Save confusion matrix as CSV
        saveConfusionMatrixCsv(bestModel, X_test, y_test, paths['outputs'] / 'confusion_matrix.csv')
        
        # Save feature importance (if available)
        saveFeatureImportance(bestModel, paths['outputs'] / 'feature_importance.csv')
        
        # Save sample predictions
        saveSamplePredictions(bestModel, X_test, y_test, paths['outputs'] / 'sample_predictions.csv')
        
        # Save model summary
        saveBestModelSummary(metrics, paths['outputs'] / 'best_model_summary.txt')
        
        print("\n" + "=" * 80)
        print("✓ TRAINING COMPLETE - ALL RESULTS SAVED")
        print("=" * 80)
        print(f"\nModel: Random Forest")
        print(f"F1-Score: {metrics['F1-Score']:.4f}")
        print("\nOutput Files:")
        print(f"  - {paths['models'] / 'insider_threat_model.pkl'}")
        print(f"  - {paths['models'] / 'feature_names.pkl'}")
        print(f"  - {paths['outputs'] / 'dataset_summary.txt'}")
        print(f"  - {paths['outputs'] / 'model_metrics.txt'}")
        print(f"  - {paths['outputs'] / 'best_model_summary.txt'}")
        print(f"  - {paths['outputs'] / 'classification_report.txt'}")
        print(f"  - {paths['outputs'] / 'confusion_matrix.png'}")
        print(f"  - {paths['outputs'] / 'confusion_matrix.csv'}")
        print(f"  - {paths['outputs'] / 'feature_importance.csv'}")
        print(f"  - {paths['outputs'] / 'sample_predictions.csv'}")
        print()
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        return 1
    except ValueError as e:
        print(f"\n✗ Error: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
