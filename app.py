import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
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

st.set_page_config(
    page_title="SENTINEL INTELLIGENCE | COS720 Insider Threat Prototype",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load trained model ────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    """Load the trained model and feature names."""
    try:
        model_path = Path('models') / 'insider_threat_model.pkl'
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None

model = load_model()


# ── Aggressive CSS reset – force light theme everywhere ──────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

/* ── Force light background on EVERY Streamlit container ── */
html, body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="block-container"],
.main, .main > div,
section[data-testid="stSidebar"],
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
[class*="css"] {
    background-color: #f7f9fb !important;
    color: #191c1e !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Streamlit column wrappers ── */
[data-testid="column"] {
    background-color: #f7f9fb !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background-color: #ffffff !important;
    border: 2px dashed #c6c6cd !important;
    border-radius: 12px !important;
    padding: 8px !important;
}
[data-testid="stFileUploader"] * {
    background-color: transparent !important;
    color: #191c1e !important;
}
[data-testid="stFileUploaderDropzone"] {
    background-color: #ffffff !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] {
    visibility: hidden !important;
    height: 0 !important;
}
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
}

/* ── Block container sizing ── */
.block-container,
[data-testid="stMainBlockContainer"] {
    padding-top: 1rem !important;
    padding-bottom: 4rem !important;
    margin: 0 auto !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f7f9fb; }
::-webkit-scrollbar-thumb { background: #c6c6cd; border-radius: 3px; }

/* ── Material Symbols font ── */
.material-symbols-outlined {
    font-family: 'Material Symbols Outlined' !important;
    font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
    vertical-align: middle;
    display: inline-block;
}

/* ══════════════════════════════════════
   Typography
══════════════════════════════════════ */
.display-lg {
    font-family: 'Hanken Grotesk', sans-serif !important;
    font-size: 48px; line-height: 56px; font-weight: 700;
    letter-spacing: -0.02em; color: #191c1e;
    margin: 0 0 16px 0;
}
.headline-lg {
    font-family: 'Hanken Grotesk', sans-serif !important;
    font-size: 32px; line-height: 40px; font-weight: 600;
    letter-spacing: -0.01em; color: #191c1e; margin: 0;
}
.title-md {
    font-family: 'Hanken Grotesk', sans-serif !important;
    font-size: 20px; line-height: 28px; font-weight: 600; color: #191c1e;
}
.label-caps {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px; line-height: 16px; letter-spacing: 0.05em; font-weight: 500;
}
.code-sm { font-family: 'JetBrains Mono', monospace !important; font-size: 13px; line-height: 18px; }
.body-lg  { font-size: 16px; line-height: 24px; }
.body-md  { font-size: 14px; line-height: 20px; }
.body-sm  { font-size: 14px; line-height: 20px; }
.text-secondary { color: #515f74 !important; }
.text-error     { color: #ba1a1a !important; }
.text-primary   { color: #000000 !important; }

/* ══════════════════════════════════════
   Components
══════════════════════════════════════ */
.card {
    background: #ffffff !important;
    border: 1px solid #c6c6cd;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin-bottom: 10px;
}
.glass-panel {
    background: rgba(255,255,255,0.92) !important;
    border: 1px solid rgba(185,199,224,0.5);
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 20px rgba(186,26,26,0.08);
}
.metric-card {
    background: #ffffff !important;
    border: 1px solid #c6c6cd;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    height: 100%;
}
.badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 0.05em; font-weight: 600;
    padding: 2px 8px; border-radius: 4px; text-transform: uppercase;
}
.badge-error   { background: rgba(186,26,26,0.08); color: #ba1a1a; border: 1px solid rgba(186,26,26,0.25); }
.badge-success { background: rgba(81,95,116,0.08); color: #515f74; border: 1px solid #c6c6cd; }
.badge-neutral { background: #eceef0; color: #515f74; border: 1px solid #c6c6cd; }
.section-divider { border: none; border-top: 1px solid #c6c6cd; margin: 40px 0; }
.progress-bar-bg   { background: #eceef0; height: 8px; border-radius: 999px; overflow: hidden; margin-top: 4px; }
.progress-bar-fill { background: #ba1a1a; height: 100%; border-radius: 999px; }
.info-box {
    background: #ffffff !important;
    border: 1px solid #c6c6cd;
    border-radius: 12px; padding: 24px;
}
.ethics-box {
    background: #f2f4f6 !important;
    border: 1px solid #c6c6cd;
    border-radius: 12px; padding: 32px;
}
.indicator-card {
    background: #ffffff !important;
    border: 1px solid #c6c6cd;
    border-radius: 12px; padding: 16px; text-align: center;
    margin-bottom: 8px;
}
.pipeline-circle {
    width: 48px; height: 48px;
    background: #000; color: #fff;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 16px;
    margin: 0 auto 12px auto;
    font-family: 'Hanken Grotesk', sans-serif;
}

/* ── Confusion table ── */
table.confusion { width: 100%; border-collapse: collapse; }
table.confusion th, table.confusion td {
    padding: 14px 16px; border-bottom: 1px solid #c6c6cd; font-size: 13px;
}
table.confusion thead {
    background: #e6e8ea;
    font-family: 'JetBrains Mono', monospace; font-size: 10px;
    text-transform: uppercase; letter-spacing: 0.05em; color: #515f74;
}
table.confusion tr:nth-child(even) td { background: rgba(0,0,0,0.015); }
table.confusion .row-header {
    background: #f2f4f6; color: #515f74;
    font-family: 'JetBrains Mono', monospace; font-size: 10px;
    text-transform: uppercase; letter-spacing: 0.05em;
    border-right: 1px solid #c6c6cd;
}

/* ── Fixed top nav ── */
.topnav {
    position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
    background: #ffffff !important;
    border-bottom: 1px solid #c6c6cd;
    height: 64px;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 32px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.topnav a {
    font-weight: 500; text-decoration: none;
    color: #515f74 !important;
    margin: 0 12px; line-height: 64px; font-size: 15px;
    font-family: 'Inter', sans-serif;
}
.topnav a.active {
    font-weight: 700; color: #000 !important;
    border-bottom: 2px solid #000;
    padding-bottom: 2px;
}
.topnav-brand {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; font-weight: 700; letter-spacing: 0.05em; color: #191c1e;
}
</style>
""", unsafe_allow_html=True)

# ── Top Nav ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="topnav">
  <div>
    <a class="active" href="#">System Overview</a>
    <a href="#">Metrics</a>
    <a href="#">Evaluation</a>
  </div>
  <span class="topnav-brand">COS720 Prototype</span>
</div>
<div style="height:72px;"></div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1 — Hero & Upload
# ═══════════════════════════════════════════════════════════════════════════

# Button styling
st.markdown("""
<style>
div[data-testid="stDownloadButton"] {
    margin-top: 4px !important;
}

div[data-testid="stDownloadButton"] button,
div[data-testid="stButton"] button {
    background-color: white !important;
    color: black !important;
    border: 1px solid #c6c6cd !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}

div[data-testid="stDownloadButton"] button:hover,
div[data-testid="stButton"] button:hover {
    background-color: #f2f4f6 !important;
    color: black !important;
    border-color: black !important;
}
</style>
""", unsafe_allow_html=True)


def get_record_explanation(row, pred, conf):
    """Generate simple dataset-aligned explanation and key indicators."""
    indicators = []

    if row.get("total_files_burned", 0) > 0:
        indicators.append("File burning activity")
    if row.get("num_printed_pages_off_hours", 0) > 0:
        indicators.append("Off-hours printing")
    if row.get("total_printed_pages", 0) > 100:
        indicators.append("High printing volume")
    if row.get("burned_from_other", 0) > 0:
        indicators.append("Files burned from another source")
    if row.get("entry_during_weekend", 0) == 1:
        indicators.append("Weekend facility entry")
    if row.get("is_abroad", 0) == 1:
        indicators.append("Activity while abroad")
    if row.get("hostility_country_level", 0) > 0:
        indicators.append("Hostility country indicator")
    if row.get("num_entries", 0) > 5:
        indicators.append("High facility entry count")
    if row.get("num_unique_campus", 0) > 1:
        indicators.append("Multiple campus access")
    if row.get("is_contractor", 0) == 1:
        indicators.append("Contractor status")

    if pred == 1:
        if indicators:
            explanation = (
                "This activity was flagged because the record shows "
                + ", ".join(indicators)
                + "."
            )
        else:
            explanation = (
                "This activity was flagged because the overall behavioural pattern "
                "matched potential malicious insider activity."
            )
    else:
        if indicators:
            explanation = (
                "This activity was classified as normal, although some indicators "
                "were present: "
                + ", ".join(indicators)
                + ". The overall pattern did not match malicious activity."
            )
        else:
            explanation = (
                "This activity appears normal because the behavioural indicators do "
                "not show strong signs of unusual printing, file burning, weekend access, "
                "or travel-related risk."
            )

    key_indicators = "; ".join(indicators) if indicators else "None"
    return explanation, key_indicators


col_hero, col_result = st.columns([1, 1], gap="medium")

with col_hero:
    st.markdown("""
    <h1 class="display-lg">AI-Powered Insider Threat Detection System</h1>
    <p class="body-lg text-secondary" style="margin-bottom:24px; line-height:1.6;">
        Deploying advanced behavioral analytics to identify high-risk internal activity before data breaches occur.
        Upload employee records for immediate predictive analysis.
    </p>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload employee behavioural records",
        type=["csv"],
        label_visibility="visible",
    )


with col_result:
    if uploaded_file and model:
        try:
            # Read uploaded file
            df = pd.read_csv(uploaded_file)

            # Drop columns that should not be used for prediction
            df_model = df.copy()
            for col in ["is_malicious", "late_exit_flag"]:
                if col in df_model.columns:
                    df_model = df_model.drop(columns=[col])

            # If you already have EXPECTED_FEATURES defined globally, this validates input
            missing_cols = [col for col in EXPECTED_FEATURES if col not in df_model.columns]
            if missing_cols:
                raise ValueError("Missing required columns: " + ", ".join(missing_cols))

            df_model = df_model[EXPECTED_FEATURES]

            # Make predictions
            predictions = model.predict(df_model)
            probabilities = model.predict_proba(df_model)[:, 1]

            table_rows_html = ""
            export_rows = []

            for i in range(len(predictions)):
                pred = predictions[i]
                prob = probabilities[i]
                conf = prob if pred == 1 else (1 - prob)

                short_pred_label = "Malicious" if pred == 1 else "Normal"
                full_pred_label = (
                    "Malicious Insider Activity"
                    if pred == 1
                    else "Normal / Benign Behaviour"
                )

                risk_label = "HIGH RISK" if pred == 1 else "LOW RISK"
                risk_color = "#ba1a1a" if pred == 1 else "#2d7d3d"

                bg_r = 255 if pred == 1 else 45
                bg_g = 26 if pred == 1 else 125
                bg_b = 26 if pred == 1 else 61

                explanation, key_indicators = get_record_explanation(
                    df_model.iloc[i], pred, conf
                )

                short_explanation = key_indicators
                if short_explanation == "None":
                    short_explanation = "Normal operations within baseline"

                # HTML table preview row - single line to avoid rendering issues
                table_rows_html += f"<tr><td style='padding:12px 16px; border-bottom:1px solid #c6c6cd; font-family:\"JetBrains Mono\",monospace; font-size:12px; white-space:nowrap;'>#{i+1}</td><td style='padding:12px 16px; border-bottom:1px solid #c6c6cd; font-weight:500; color:#191c1e; white-space:nowrap;'>{short_pred_label}</td><td style='padding:12px 16px; border-bottom:1px solid #c6c6cd; font-weight:700; color:#191c1e; white-space:nowrap;'>{conf*100:.1f}%</td><td style='padding:12px 16px; border-bottom:1px solid #c6c6cd; white-space:nowrap;'><span style='display:inline-block; background:rgba({bg_r},{bg_g},{bg_b},0.12); color:{risk_color}; border:1px solid rgba({bg_r},{bg_g},{bg_b},0.3); padding:4px 8px; border-radius:4px; font-size:11px; font-weight:600;'>{risk_label}</span></td><td style='padding:12px 16px; border-bottom:1px solid #c6c6cd; font-size:12px; color:#515f74;'>{short_explanation}</td></tr>"

                # Download / expanded table row
                export_row = {
                    "Record": i + 1,
                    "Prediction": full_pred_label,
                    "Prediction_Value": int(pred),
                    "Confidence": f"{conf*100:.1f}%",
                    "Risk_Level": risk_label,
                    "Explanation": explanation,
                    "Key_Indicators": key_indicators,
                    "Employee_Department": df_model.iloc[i].get("employee_department", ""),
                    "Employee_Position": df_model.iloc[i].get("employee_position", ""),
                    "Employee_Classification": df_model.iloc[i].get("employee_classification", ""),
                    "Contractor_Status": df_model.iloc[i].get("is_contractor", ""),
                    "total_printed_pages": df_model.iloc[i].get("total_printed_pages", ""),
                    "num_printed_pages_off_hours": df_model.iloc[i].get("num_printed_pages_off_hours", ""),
                    "total_files_burned": df_model.iloc[i].get("total_files_burned", ""),
                    "burned_from_other": df_model.iloc[i].get("burned_from_other", ""),
                    "entry_during_weekend": df_model.iloc[i].get("entry_during_weekend", ""),
                    "is_abroad": df_model.iloc[i].get("is_abroad", ""),
                    "num_entries": df_model.iloc[i].get("num_entries", ""),
                    "num_unique_campus": df_model.iloc[i].get("num_unique_campus", ""),
                }

                export_rows.append(export_row)

            results_df = pd.DataFrame(export_rows)
            csv_data = results_df.to_csv(index=False)

            # Store for expanded table outside the columns
            st.session_state["prediction_results_df"] = results_df

            if "show_full_table" not in st.session_state:
                st.session_state["show_full_table"] = False

            avg_confidence = np.mean(
                np.where(predictions == 1, probabilities, 1 - probabilities)
            ) * 100

            malicious_count = int(sum(predictions))

            # Preview table panel
            st.markdown(f"""
            <div class="glass-panel">
              <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px;">
                <div>
                  <p class="title-md" style="margin:0 0 8px 0;">Prediction Results</p>
                  <p class="body-sm text-secondary" style="margin:0;">Total Records: {len(df_model)}</p>
                </div>
                <div style="text-align:right;">
                  <p class="code-sm" style="font-weight:700; color:#000; margin:0;">AVG CONFIDENCE: {avg_confidence:.1f}%</p>
                  <p class="code-sm text-secondary" style="margin:4px 0 0 0;">MALICIOUS DETECTED: {malicious_count}</p>
                </div>
              </div>

              <div style="overflow-x:auto; overflow-y:auto; max-height:300px; border:1px solid #c6c6cd; border-radius:8px; margin-bottom:16px;">
                <table class="confusion" style="width:100%;">
                  <thead style="background:#e6e8ea; position:sticky; top:0;">
                    <tr>
                      <th style="text-align:left; padding:12px 16px;">RECORD</th>
                      <th style="text-align:left; padding:12px 16px;">PREDICTION</th>
                      <th style="text-align:left; padding:12px 16px;">CONFIDENCE</th>
                      <th style="text-align:left; padding:12px 16px;">RISK LEVEL</th>
                      <th style="text-align:left; padding:12px 16px;">EXPLANATION</th>
                    </tr>
                  </thead>
                  <tbody>
                    {table_rows_html}
                  </tbody>
                </table>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Download + expanded table toggle buttons
            btn_col1, btn_col2 = st.columns([3, 1])

            with btn_col1:
                st.markdown("<div style='margin-top: 0px;'></div>", unsafe_allow_html=True)
                st.download_button(
                    label="Download Results (CSV)",
                    data=csv_data,
                    file_name="threat_predictions.csv",
                    mime="text/csv",
                    help="Download prediction results for all records",
                    type="secondary",
                    use_container_width=True,
                )

            with btn_col2:
                st.markdown("<div style='margin-top: 1px;'></div>", unsafe_allow_html=True)
                if st.button("⛶", help="Show / hide full table", use_container_width=True):
                    st.session_state["show_full_table"] = not st.session_state["show_full_table"]

        except Exception as e:
            st.markdown(f"""
            <div style="background:#ffd6d6; border:1px solid #ffb3b3; border-radius:8px; padding:12px 16px; margin:12px 0;">
              <p style="color:#000000; margin:0; font-size:14px; font-weight:500;">Error processing file: {str(e)}</p>
            </div>
            """, unsafe_allow_html=True)

    else:
        if not model:
            st.warning("Model not loaded. Please ensure the trained model exists in the models/ directory.")
        else:
            # Show example table before upload
            st.markdown("""
            <div class="glass-panel">
              <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px;">
                <div>
                  <p class="title-md" style="margin:0 0 0 0;">Example Prediction Results</p>
                  <p class="body-sm text-secondary" style="margin:0;">Total Records: 2</p>
                </div>
                <div style="text-align:right;">
                  <p class="code-sm" style="font-weight:700; color:#000; margin:0;">AVG CONFIDENCE: 92.9%</p>
                  <p class="code-sm text-secondary" style="margin:4px 0 0 0;">MALICIOUS DETECTED: 1</p>
                </div>
              </div>

              <div style="overflow-x:auto; overflow-y:auto; max-height:300px; border:1px solid #c6c6cd; border-radius:8px; margin-bottom:16px;">
                <table class="confusion" style="width:100%;">
                  <thead style="background:#e6e8ea; position:sticky; top:0;">
                    <tr>
                      <th style="text-align:left; padding:12px 16px;">RECORD</th>
                      <th style="text-align:left; padding:12px 16px;">PREDICTION</th>
                      <th style="text-align:left; padding:12px 16px;">CONFIDENCE</th>
                      <th style="text-align:left; padding:12px 16px;">RISK LEVEL</th>
                      <th style="text-align:left; padding:12px 16px;">EXPLANATION</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td style="padding:12px 16px; border-bottom:1px solid #c6c6cd; font-family:'JetBrains Mono',monospace; font-size:12px; white-space:nowrap;">#1</td>
                      <td style="padding:12px 16px; border-bottom:1px solid #c6c6cd; font-weight:500; color:#191c1e; white-space:nowrap;">Malicious</td>
                      <td style="padding:12px 16px; border-bottom:1px solid #c6c6cd; font-weight:700; color:#191c1e; white-space:nowrap;">94.2%</td>
                      <td style="padding:12px 16px; border-bottom:1px solid #c6c6cd; white-space:nowrap;">
                        <span style="display:inline-block; background:rgba(255,26,26,0.12); color:#ba1a1a; border:1px solid rgba(255,26,26,0.3); padding:4px 8px; border-radius:4px; font-size:11px; font-weight:600;">HIGH RISK</span>
                      </td>
                      <td style="padding:12px 16px; border-bottom:1px solid #c6c6cd; font-size:12px; color:#515f74;">File burning activity + Off-hours printing</td>
                    </tr>
                    <tr>
                      <td style="padding:12px 16px; font-family:'JetBrains Mono',monospace; font-size:12px; white-space:nowrap;">#2</td>
                      <td style="padding:12px 16px; font-weight:500; color:#191c1e; white-space:nowrap;">Normal</td>
                      <td style="padding:12px 16px; font-weight:700; color:#191c1e; white-space:nowrap;">91.5%</td>
                      <td style="padding:12px 16px; white-space:nowrap;">
                        <span style="display:inline-block; background:rgba(45,125,61,0.12); color:#2d7d3d; border:1px solid rgba(45,125,61,0.3); padding:4px 8px; border-radius:4px; font-size:11px; font-weight:600;">LOW RISK</span>
                      </td>
                      <td style="padding:12px 16px; font-size:12px; color:#515f74;">Normal operations within baseline</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# FULL-WIDTH EXPANDED TABLE — OUTSIDE THE COLUMNS
# ═══════════════════════════════════════════════════════════════════════════
if (
    st.session_state.get("show_full_table", False)
    and "prediction_results_df" in st.session_state
):
    st.markdown("""
    <div style="margin-top:8px; margin-bottom:8px; padding:8px; border:1px solid #c6c6cd; border-radius:12px; background:#ffffff;">
        <p class="title-md" style="margin:0 ;">Full Prediction Results Table</p>
        <p class="body-sm text-secondary" style="margin:0 0 12px 0;">
            Expanded view of all prediction results.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        st.session_state["prediction_results_df"],
        use_container_width=True,
        height=600,
        hide_index=True,
    )

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2 — Model Summary
# ═══════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("""
<div style="display:flex; align-items:center; gap:12px; border-bottom:1px solid #c6c6cd; padding-bottom:16px; margin-bottom:24px;">
  <span class="material-symbols-outlined text-primary" style="font-size:28px;">analytics</span>
  <h2 class="headline-lg">Model Architecture: Random Forest Classifier</h2>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4, gap="small")
metrics = [
    ("ACCURACY",  "97.10%", "Overall correctly identified records across all classes."),
    ("PRECISION", "74.10%", "The ratio of true malicious detections to all predicted threats."),
    ("RECALL",    "71.03%", "The system's ability to find all actual malicious activities."),
    ("F1-SCORE",  "72.53%", "Harmonic mean of precision and recall for balanced evaluation."),
]
for col, (label, value, desc) in zip([m1, m2, m3, m4], metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <p class="label-caps text-secondary" style="margin:0 0 4px 0;">{label}</p>
          <p style="font-size:30px; font-weight:700; color:#000; margin:0; font-family:'Hanken Grotesk',sans-serif;">{value}</p>
          <p class="body-sm text-secondary" style="font-size:12px; margin:8px 0 0 0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3 — Inference Pipeline
# ═══════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<h2 class="headline-lg" style="text-align:center; margin-bottom:36px;">Inference Pipeline</h2>', unsafe_allow_html=True)

p1, p2, p3, p4 = st.columns(4, gap="small")
steps = [
    ("1", "Upload CSV",        "Import batch behavioral logs into the secure buffer."),
    ("2", "Validate Data",     "Automatic cleaning and structural integrity verification."),
    ("3", "Predict Behaviour", "Random Forest scoring and classification engine."),
    ("4", "Explain Result",    "XAI output generation for human review."),
]
for col, (num, title, desc) in zip([p1, p2, p3, p4], steps):
    with col:
        st.markdown(f"""
        <div style="text-align:center; padding:0 8px;">
          <div class="pipeline-circle">{num}</div>
          <p style="font-weight:700; color:#191c1e; margin:0 0 4px 0; font-family:'Hanken Grotesk',sans-serif;">{title}</p>
          <p class="body-sm text-secondary" style="font-size:12px; margin:0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 4 — Key Behavioural Indicators
# ═══════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<h2 class="headline-lg" style="margin-bottom:24px;">Key Behavioural Indicators</h2>', unsafe_allow_html=True)

indicators = [
    ("print",                 "Off-hours Printing"),
    ("description",           "Total Printed Pages"),
    ("local_fire_department", "File Burning Activity"),
    ("folder_zip",            "Files Burned From Other Source"),
    ("event",                 "Weekend Facility Entry"),
    ("login",                 "Number of Facility Entries"),
    ("corporate_fare",        "Campus Access"),
    ("apartment",             "Number of Unique Campuses Accessed"),
    ("public",                "Activity While Abroad"),
    ("calendar_today",        "Trip Day Number"),
    ("warning",               "Hostility Country Level"),
    ("badge",                 "Contractor Status"),
    ("groups",                "Employee Classification"),
]

rows = [indicators[i:i+5] for i in range(0, len(indicators), 5)]
for row in rows:
    cols = st.columns(5, gap="small")
    for i, col in enumerate(cols):
        if i < len(row):
            icon, label = row[i]
            with col:
                st.markdown(f"""
                <div class="indicator-card">
                  <span class="material-symbols-outlined text-secondary" style="font-size:28px;">{icon}</span>
                  <p class="label-caps text-secondary" style="font-size:10px; margin:8px 0 0 0;">{label}</p>
                </div>
                """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 5 — Testing Examples
# ═══════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<h2 class="headline-lg" style="margin-bottom:24px;">Testing Examples</h2>', unsafe_allow_html=True)

ex1, ex2 = st.columns(2, gap="medium")

with ex1:
    st.markdown("""
    <div class="card">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <span class="badge badge-error">TRUE POSITIVE</span>
        <span class="code-sm text-secondary">Confidence: 98%</span>
      </div>
      <p class="body-md" style="color:#191c1e; margin:0;">Successful detection of actual malicious activity. High-severity alert triggered.</p>
    </div>
    <div class="card">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <span class="badge badge-neutral">FALSE POSITIVE</span>
        <span class="code-sm text-secondary">RISK: 0.61</span>
      </div>
      <p class="body-md" style="color:#191c1e; margin:0;">Benign activity misclassified as threat. Typical in high-sensitivity settings.</p>
    </div>
    """, unsafe_allow_html=True)

with ex2:
    st.markdown("""
    <div class="card">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <span class="badge badge-success">TRUE NEGATIVE</span>
        <span class="code-sm text-secondary">Confidence: 98%</span>
      </div>
      <p class="body-md" style="color:#191c1e; margin:0;">Correctly identified standard, non-malicious business operations.</p>
    </div>
    <div class="card" style="border-color:#ffdad6;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <span class="badge badge-error">FALSE NEGATIVE</span>
        <span class="code-sm text-secondary">RISK: 0.14</span>
      </div>
      <p class="body-md" style="color:#191c1e; margin:0;">Failure to detect actual threat. Critical area for model optimization.</p>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 6 — Confusion Matrix
# ═══════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

cm_col, why_col = st.columns([2, 1], gap="large")

with cm_col:
    st.markdown('<h2 class="headline-lg" style="margin-bottom:20px;">Confusion Matrix Analysis</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div style="overflow-x:auto; border:1px solid #c6c6cd; border-radius:12px; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
      <table class="confusion">
        <thead>
          <tr>
            <th style="text-align:left;">Actual / Predicted</th>
            <th style="text-align:left;">Predicted Normal</th>
            <th style="text-align:left;">Predicted Malicious</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="row-header">Actual Normal</td>
            <td style="font-weight:700; color:#191c1e; font-family:'JetBrains Mono',monospace;">22,129 (TN)</td>
            <td style="color:#515f74; font-family:'JetBrains Mono',monospace;">317 (FP)</td>
          </tr>
          <tr>
            <td class="row-header">Actual Malicious</td>
            <td style="color:#515f74; font-family:'JetBrains Mono',monospace;">370 (FN)</td>
            <td style="font-weight:700; color:#ba1a1a; font-family:'JetBrains Mono',monospace;">907 (TP)</td>
          </tr>
        </tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)

with why_col:
    st.markdown("""
    <div class="info-box" style="margin-top:52px;">
      <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
        <span class="material-symbols-outlined" style="font-size:22px; color:#000;">info</span>
        <span class="title-md">Why Recall and F1-Score Matter</span>
      </div>
      <p class="body-md text-secondary" style="line-height:1.7; margin:0 0 12px 0;">
        In insider threat detection, recall is important because a false negative means malicious
        behaviour was missed. However, precision is also important because false positives may lead
        to unnecessary investigation. The F1-score balances precision and recall, especially
        important for imbalanced insider threat data.
      </p>
      <ul style="margin:0; padding:0; list-style:none; font-family:'JetBrains Mono',monospace; font-size:12px; color:#000;">
        <li style="margin-bottom:6px;">• Minimizes Unobserved Threats</li>
        <li style="margin-bottom:6px;">• Optimizes Security Response</li>
        <li>• Validates Detection Sensitivity</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 7 — Explainability Framework
# ═══════════════════════════════════════════════════════════════════════════

FEATURE_IMPORTANCE_PATH = "outputs/feature_importance.csv"

FEATURE_LABELS = {
    "total_printed_pages": "Total Printed Pages",
    "num_printed_pages_off_hours": "Off-hours Printing",
    "total_files_burned": "File Burning Activity",
    "burned_from_other": "Files Burned From Other Source",
    "is_abroad": "Activity While Abroad",
    "trip_day_number": "Trip Day Number",
    "hostility_country_level": "Hostility Country Level",
    "num_entries": "Number of Facility Entries",
    "num_unique_campus": "Number of Unique Campuses Accessed",
    "entry_during_weekend": "Weekend Facility Entry",
    "is_contractor": "Contractor Status",
    "employee_classification": "Employee Classification",
    "employee_seniority_years": "Employee Seniority Years",
    "employee_department": "Employee Department",
    "employee_campus": "Employee Campus",
    "employee_position": "Employee Position",
    "employee_origin_country": "Employee Origin Country",
    "has_foreign_citizenship": "Foreign Citizenship",
    "has_criminal_record": "Criminal Record Indicator",
    "has_medical_history": "Medical History Indicator",
}


def clean_feature_name(feature_name):
    """Clean transformed feature names from the preprocessing pipeline."""
    feature_name = str(feature_name)

    # Remove sklearn ColumnTransformer prefixes
    feature_name = feature_name.replace("num__", "").replace("cat__", "")

    # For one-hot encoded categorical variables, keep readable form
    for base_feature in [
        "employee_department",
        "employee_campus",
        "employee_position",
        "employee_origin_country",
    ]:
        if feature_name.startswith(base_feature + "_"):
            category = feature_name.replace(base_feature + "_", "")
            readable_base = FEATURE_LABELS.get(base_feature, base_feature.replace("_", " ").title())
            return f"{readable_base}: {category}"

    return FEATURE_LABELS.get(feature_name, feature_name.replace("_", " ").title())


def load_feature_importance(path):
    """Load real feature importance values from the model output CSV."""
    try:
        fi_df = pd.read_csv(path)

        # Support both possible column formats: Feature/Importance or feature/importance
        fi_df.columns = [col.strip().lower() for col in fi_df.columns]

        if "feature" not in fi_df.columns or "importance" not in fi_df.columns:
            return pd.DataFrame(columns=["Label", "Importance", "Relative_Impact"])

        fi_df["Label"] = fi_df["feature"].apply(clean_feature_name)
        fi_df["Importance"] = fi_df["importance"].astype(float)

        fi_df = fi_df.sort_values("Importance", ascending=False).head(5)

        max_importance = fi_df["Importance"].max()
        fi_df["Relative_Impact"] = (fi_df["Importance"] / max_importance * 100).round(1)

        return fi_df

    except Exception:
        return pd.DataFrame(columns=["Label", "Importance", "Relative_Impact"])


feature_importance_df = load_feature_importance(FEATURE_IMPORTANCE_PATH)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; margin-bottom:32px;">
  <h2 class="headline-lg">Explainability Framework</h2>
  <p class="body-md text-secondary" style="margin-top:8px;">
    Transparency in algorithmic decision-making for security compliance.
  </p>
</div>
""", unsafe_allow_html=True)

xai_left, xai_right = st.columns(2, gap="large")

with xai_left:
    st.markdown("""
    <h3 class="headline-lg" style="font-size:24px; margin-bottom:10px;">Model Interpretability</h3>
    <p class="body-md text-secondary" style="margin-bottom:24px; line-height:1.65;">
        The system uses the Random Forest model's feature importance values and behavioural
        indicators to explain predictions in human-readable form.
    </p>
    """, unsafe_allow_html=True)

    if feature_importance_df.empty:
        st.warning("Feature importance file not found. Run train_model.py first.")
    else:
        for _, row in feature_importance_df.iterrows():
            name = row["Label"]
            importance = row["Importance"]
            relative_pct = row["Relative_Impact"]

            st.markdown(f"""
            <div style="margin-bottom:16px;">
              <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span class="label-caps text-secondary" style="font-size:10px; text-transform:uppercase; font-weight:700;">
                    {name}
                </span>
                <span class="label-caps text-error" style="font-size:10px; font-weight:700;">
                    {importance:.4f}
                </span>
              </div>
              <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width:{relative_pct}%;"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.caption(
            "The bar length is normalised relative to the most important feature. "
            "The number shown is the actual Random Forest feature importance score."
        )

with xai_right:
    if not feature_importance_df.empty:
        chart_df = feature_importance_df[["Label", "Importance"]].sort_values(
            "Importance", ascending=True
        )

        st.bar_chart(
            chart_df.set_index("Label"),
            use_container_width=True
        )
    else:
        st.markdown("""
        <div style="background:#f2f4f6; border:1px solid #c6c6cd; border-radius:12px; padding:32px; text-align:center;">
            <p class="title-md" style="margin:0 0 8px 0;">Feature Importance Visualisation</p>
            <p class="body-md text-secondary" style="margin:0;">
                Run the training script to generate feature_importance.csv.
            </p>
        </div>
        """, unsafe_allow_html=True)
# ═══════════════════════════════════════════════════════════════════════════
# SECTION 8 — Ethics & Limitations
# ═══════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="ethics-box">
  <div style="display:flex; align-items:center; gap:12px; margin-bottom:24px;">
    <span class="material-symbols-outlined text-error" style="font-size:28px;">gavel</span>
    <h2 class="headline-lg">Ethics &amp; Protocol Limitations</h2>
  </div>
  <div style="display:grid; grid-template-columns:1fr 1fr; gap:32px;">
    <div>
      <p class="body-lg" style="font-weight:700; color:#191c1e; margin:0 0 12px 0;">Prototype Disclaimer</p>
      <p class="body-md text-secondary" style="line-height:1.7; margin:0;">
        This system is an academic prototype. Predictions should support further human investigation
        and should not be treated as proof of malicious intent.
      </p>
    </div>
    <div>
      <p class="body-lg" style="font-weight:700; color:#191c1e; margin:0 0 12px 0;">Human-in-the-Loop Requirement</p>
      <ul style="list-style:none; padding:0; margin:0;">
        <li style="display:flex; gap:10px; margin-bottom:12px; align-items:flex-start;">
          <span class="material-symbols-outlined" style="font-size:18px; color:#000; margin-top:2px; flex-shrink:0;">check_circle</span>
          <span class="body-md text-secondary">All high-risk alerts must be reviewed by a human analyst before any action is taken.</span>
        </li>
        <li style="display:flex; gap:10px; margin-bottom:12px; align-items:flex-start;">
          <span class="material-symbols-outlined" style="font-size:18px; color:#000; margin-top:2px; flex-shrink:0;">check_circle</span>
          <span class="body-md text-secondary">Data ingestion must comply with GDPR and local labor privacy laws.</span>
        </li>
        <li style="display:flex; gap:10px; align-items:flex-start;">
          <span class="material-symbols-outlined" style="font-size:18px; color:#000; margin-top:2px; flex-shrink:0;">check_circle</span>
          <span class="body-md text-secondary">Model bias audits should be conducted quarterly on demographic data.</span>
        </li>
      </ul>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Footer ───────────────────────────────────────────────────────────────
st.markdown("""
<hr style="border:none; border-top:1px solid #c6c6cd; margin-top:64px;">
<p class="label-caps text-secondary" style="text-align:center; font-size:10px; letter-spacing:0.12em; text-transform:uppercase; padding:24px 0; margin:0;">
  COS720 Insider Threat Detection Prototype • Academic Demonstration System
</p>
""", unsafe_allow_html=True)