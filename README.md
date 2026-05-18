# COS720: AI-Powered Insider Threat Detection System

## Project Overview

This project implements an AI-powered insider threat detection system using machine learning to identify potentially dangerous employee behavior patterns. The system uses a Random Forest classifier trained on the Insider Threat dataset to classify employees as either normal or threatening based on 20 behavioral and demographic features.

The project includes:
- **train_model.py**: Model training and evaluation script
- **app.py**: Interactive Streamlit web application for predictions
- **Data**: Clean insider threat dataset for training
- **Models**: Pre-trained model and performance metrics
- **Test Files**: Sample CSV files for testing predictions

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Clone the Repository

1. Clone the project:
   ```bash
   git clone https://github.com/p4ntomath/AI-Powered-Insider-Threat-Detection-System.git
   ```

2. Navigate to the project directory:
   ```bash
   cd AI-Powered-Insider-Threat-Detection-System
   ```

### Install Dependencies

Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

The main dependencies include:
- `scikit-learn` - Machine learning algorithms
- `pandas` & `numpy` - Data processing
- `streamlit` - Web application framework
- `joblib` - Model serialization
- `matplotlib` & `plotly` - Data visualization

## How to Train the Model

Run the training script to train the Random Forest classifier:

```bash
python train_model.py
```

This script will:
1. Load and inspect the insider threat dataset (`data/insider_threat_clean_dataset.csv`)
2. Preprocess data and handle missing values
3. Train a Random Forest classifier with optimized parameters
4. Split data into train/test sets (typical 80/20 split)
5. Evaluate model performance on the test set
6. Save the trained model and generate analysis reports

**Output files** will be saved to the `outputs/` directory:
- `best_model_summary.txt` - Model configuration and hyperparameters
- `model_metrics.txt` - Performance metrics (accuracy, precision, recall, F1)
- `confusion_matrix.csv` - Confusion matrix data
- `classification_report.txt` - Detailed classification report
- `feature_importance.csv` - Ranking of most important features
- `sample_predictions.csv` - Example predictions on test samples
- `dataset_summary.txt` - Dataset statistics

## How to Run the App

Launch the interactive Streamlit web application:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

**Features:**
- System overview and project information
- Upload CSV files with employee data for predictions
- Single record input form for individual predictions
- Real-time threat classification
- Model performance metrics and visualizations
- Feature importance analysis

## How to Test the App

### Option 1: Use Sample Test Files

Test CSV files are provided in `test_files/` directory:
- `normal_behavior.csv` - Employees with typical low-risk behavior
- `suspicious_behavior.csv` - Employees exhibiting high-risk indicators
- `mixed_cases.csv` - Mix of normal and suspicious patterns
- `edge_cases.csv` - Boundary test cases with extreme values

In the Streamlit app:
1. Navigate to the prediction section
2. Upload any test CSV file
3. View the model's predictions and confidence scores

### Option 2: Manual Single Record Testing

Use the single record input form in the app to test individual predictions by entering values for each of the 20 required features.

### Required Input Features

All test files must include these 20 columns:
```
employee_department, employee_campus, employee_position, 
employee_seniority_years, is_contractor, employee_classification,
has_foreign_citizenship, has_criminal_record, has_medical_history,
employee_origin_country, total_printed_pages, num_printed_pages_off_hours,
total_files_burned, burned_from_other, is_abroad, trip_day_number,
hostility_country_level, num_entries, num_unique_campus, entry_during_weekend
```

## Model Files Storage

All model artifacts are stored in the `models/` directory:

- **`insider_threat_model.pkl`** - The trained Random Forest model (loaded by app.py for predictions)
- Additional model files and artifacts used during development

**Directory Structure:**
```
models/
├── insider_threat_model.pkl    # Trained model
└── [other model artifacts]
```

The app automatically loads the model from `models/insider_threat_model.pkl` when starting. Ensure the model file exists before running the application.

## Project Structure

```
COS720-Project/
├── app.py                           # Streamlit web application
├── train_model.py                   # Model training script
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── data/
│   └── insider_threat_clean_dataset.csv  # Training data
├── models/
│   └── insider_threat_model.pkl     # Trained model
├── outputs/
│   ├── best_model_summary.txt
│   ├── model_metrics.txt
│   ├── confusion_matrix.csv
│   ├── classification_report.txt
│   ├── feature_importance.csv
│   ├── sample_predictions.csv
│   └── dataset_summary.txt
└── test_files/
    ├── normal_behavior.csv
    ├── suspicious_behavior.csv
    ├── mixed_cases.csv
    └── edge_cases.csv
```

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/p4ntomath/AI-Powered-Insider-Threat-Detection-System.git
cd AI-Powered-Insider-Threat-Detection-System

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the model (optional - regenerates outputs)
python train_model.py

# 4. Run the app
streamlit run app.py

# 5. Open http://localhost:8501 in your browser
# 6. Upload test files or input data to get predictions
```

## Model Performance

See `outputs/model_metrics.txt` for detailed performance metrics including:
- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

## Notes

- The model is trained on balanced inside threat patterns with 20 behavioral/demographic features
- Predictions are binary classifications: Normal (0) or Threat (1)
- The system considers sensitive features including foreign citizenship and criminal records
- All model decisions are logged for audit and transparency

## License

This project is for educational purposes as part of COS720 course.
