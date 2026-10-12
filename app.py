import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from recommendation import get_recommendation
from datetime import datetime


st.set_page_config(
    page_title="",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

.stApp{
    background-color:#F4F7FA;
    color:#111827;
}

section[data-testid="stSidebar"]{
    background:#172033;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}


div[data-testid="metric-container"]{
    background:white;
    border:1px solid #D9E2EC;
    border-radius:12px;
    padding:18px;
    box-shadow:0 2px 8px rgba(0,0,0,0.08);
}

/* Metric Label */

div[data-testid="metric-container"] label{
    color:#6B7280 !important;
}

/* Metric Value */

div[data-testid="stMetricValue"]{
    color:#111827 !important;
    font-weight:700;
}


h1,h2,h3,h4,h5,h6{
    color:#111827 !important;
}

p{
    color:#4B5563 !important;
}

label{
    color:#111827 !important;
}


.stButton>button{
    width:100%;
    height:45px;
    border:none;
    border-radius:8px;
    background:#005EB8;
    color:white;
    font-weight:600;
}

hr{
    border:1px solid #E5E7EB;
}

</style>
""", unsafe_allow_html=True)


model = joblib.load("model/paper_model.pkl")

df = pd.read_csv("Honeywell_Synthetic_Historical_Dataset_10000.csv")


st.markdown("""
<div style="
background:#FFFFFF;
padding:25px;
border-radius:12px;
border-left:6px solid #005EB8;
box-shadow:0 2px 10px rgba(0,0,0,0.08);
margin-bottom:20px;
">

<h1 style="
color:#111827;
font-size:42px;
font-weight:700;
margin:0;
">
AI-Based Decision Support System for Paper Grade Transition Optimization
</h1>

<p style="
color:#4B5563;
font-size:18px;
margin-top:10px;
margin-bottom:0;
">
Predictive Decision Support System for Paper Grade Transition Optimization
</p>

</div>
""", unsafe_allow_html=True)


st.sidebar.header("Process Parameters")

st.sidebar.markdown("### Grade Selection")

current_grade = st.sidebar.selectbox(
    "Current Grade",
    ["A","B","C"]
)

target_grade = st.sidebar.selectbox(
    "Target Grade",
    ["A","B","C"]
)

grade_setpoint = {
    "A":90,
    "B":100,
    "C":110
}

st.sidebar.markdown("---")
st.sidebar.markdown("### Process Variables")

stock_flow = st.sidebar.slider(
    "Stock Flow (L/min)",
    float(df["Stock Flow (L/min)"].min()),
    float(df["Stock Flow (L/min)"].max()),
    float(df["Stock Flow (L/min)"].mean())
)

filler_flow = st.sidebar.slider(
    "Filler Flow (kg/min)",
    float(df["Filler Flow (kg/min)"].min()),
    float(df["Filler Flow (kg/min)"].max()),
    float(df["Filler Flow (kg/min)"].mean())
)

steam_pressure = st.sidebar.slider(
    "Steam Pressure (bar)",
    float(df["Steam Pressure (bar)"].min()),
    float(df["Steam Pressure (bar)"].max()),
    float(df["Steam Pressure (bar)"].mean())
)

machine_speed = st.sidebar.slider(
    "Machine Speed (m/min)",
    float(df["Machine Speed (m/min)"].min()),
    float(df["Machine Speed (m/min)"].max()),
    float(df["Machine Speed (m/min)"].mean())
)

moisture = st.sidebar.slider(
    "Moisture (%)",
    float(df["Moisture (%)"].min()),
    float(df["Moisture (%)"].max()),
    float(df["Moisture (%)"].mean())
)

ash = st.sidebar.slider(
    "Ash (%)",
    float(df["Ash (%)"].min()),
    float(df["Ash (%)"].max()),
    float(df["Ash (%)"].mean())
)

caliper = st.sidebar.slider(
    "Caliper (mm)",
    float(df["Caliper (mm)"].min()),
    float(df["Caliper (mm)"].max()),
    float(df["Caliper (mm)"].mean())
)


input_data = pd.DataFrame({

    "Stock Flow (L/min)":[stock_flow],
    "Filler Flow (kg/min)":[filler_flow],
    "Steam Pressure (bar)":[steam_pressure],
    "Machine Speed (m/min)":[machine_speed],
    "Moisture (%)":[moisture],
    "Ash (%)":[ash],
    "Caliper (mm)":[caliper]

})


prediction = model.predict(input_data)[0]
probability = model.predict_proba(input_data)[0]

transition = current_grade != target_grade

target_bw = grade_setpoint[target_grade]

estimated_bw = (
    95
    + 1.15 * (stock_flow - 120)
    - 0.08 * (machine_speed - 700)
)

deviation = abs(estimated_bw - target_bw)

limit = target_bw * 0.025

risk = "Low"

if transition:

    if deviation > limit:

        risk = "High"

    elif deviation > (limit * 0.5):

        risk = "Medium"

st.subheader("Production Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Current Grade",
        current_grade
    )

with col2:
    st.metric(
        "Target Grade",
        target_grade
    )

with col3:

    if transition:

        st.metric(
            "Transition Risk",
            risk
        )

    else:

        st.metric(
            "Production Status",
            "Off-Spec" if prediction == 1 else "Within Spec"
        )

with col4:
    st.metric(
        "Prediction Confidence",
        f"{max(probability) * 100:.2f}%"
    )

with col5:
    st.metric(
        "Target Basis Weight",
        f"{target_bw:.1f} gsm"
    )

st.markdown("---")

left, right = st.columns([1.3, 1])

with left:

    st.subheader("Transition Assessment")

    if transition:

        if risk == "High":

            st.error("""
Transition Status : High Risk

The estimated basis weight is outside the acceptable transition tolerance.

Controlled parameter adjustment is recommended before continuing production.
""")

        elif risk == "Medium":

            st.warning("""
Transition Status : Moderate Risk

The estimated basis weight is approaching the allowable transition tolerance.

Continue the transition while closely monitoring process variables.
""")

        else:

            st.success("""
Transition Status : Stable

The estimated basis weight is within the acceptable transition tolerance.

Production can proceed with monitored adjustments.
""")

    else:

        if prediction == 1:

            st.error("""
Production Status : Off-Spec Predicted

The current operating conditions indicate an increased probability of off-spec production.
""")

        else:

            st.success("""
Production Status : Within Specification

Current operating conditions are stable.

Continue normal production.

No corrective action is required.
""")

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Target Basis Weight",
            f"{target_bw:.1f} gsm"
        )

    with col2:
        st.metric(
            "Estimated Basis Weight",
            f"{estimated_bw:.2f} gsm"
        )

    with col3:
        st.metric(
            "Deviation",
            f"{deviation:.2f} gsm"
        )

st.subheader("AI Decision")

if transition and risk == "High":

    decision = "High Risk Transition"
    decision_color = "#dc3545"

elif transition and risk == "Medium":

    decision = "Moderate Risk Transition"
    decision_color = "#ffc107"

elif prediction == 1:

    decision = "Potential Off-Spec"
    decision_color = "#fd7e14"

else:

    decision = "Process Stable"
    decision_color = "#198754"

st.markdown(
    f"""
<div style="
background:white;
padding:20px;
border-left:6px solid {decision_color};
border-radius:10px;
box-shadow:0 2px 8px rgba(0,0,0,0.08);
">

<h3>Current Decision</h3>

<h4>{decision}</h4>

<b>Confidence</b><br>
{max(probability)*100:.2f}%<br><br>

<b>Current Grade</b><br>
{current_grade}<br><br>

<b>Target Grade</b><br>
{target_grade}

</div>
""",
    unsafe_allow_html=True
)

st.subheader("AI Recommendations")

recommendations = []

if transition:

    if risk == "High":

        st.error("""
A HIGH-RISK grade transition has been detected.

Immediate engineering intervention is recommended before continuing production.
""")

        if estimated_bw < target_bw:

            recommendations = [
                {
                    "Recommendation": "Increase Stock Flow by 3-5%",
                    "Reason": f"Estimated Basis Weight ({estimated_bw:.2f} gsm) is BELOW the Target ({target_bw} gsm). Increasing stock flow increases fibre deposition and raises basis weight.",
                    "Source": "Engineering Rule Base"
                },
                {
                    "Recommendation": "Reduce Machine Speed by 2-5%",
                    "Reason": "Lower machine speed increases fibre retention per unit area, helping achieve the target basis weight.",
                    "Source": "Honeywell Best Practices"
                },
                {
                    "Recommendation": "Maintain Steam Pressure",
                    "Reason": "Stable drying conditions prevent further quality variation during the transition.",
                    "Source": "Engineering Rule Base"
                }
            ]

        else:

            recommendations = [
                {
                    "Recommendation": "Reduce Stock Flow by 3-5%",
                    "Reason": f"Estimated Basis Weight ({estimated_bw:.2f} gsm) is ABOVE the Target ({target_bw} gsm). Reducing stock flow lowers basis weight.",
                    "Source": "Engineering Rule Base"
                },
                {
                    "Recommendation": "Increase Machine Speed by 2-5%",
                    "Reason": "Higher machine speed reduces fibre deposition and helps lower basis weight.",
                    "Source": "Honeywell Best Practices"
                },
                {
                    "Recommendation": "Maintain Steam Pressure",
                    "Reason": "Stable drying conditions help maintain sheet quality during adjustment.",
                    "Source": "Engineering Rule Base"
                }
            ]

    elif risk == "Medium":

        st.warning("""
A MODERATE-RISK transition is in progress.

Corrective adjustments are recommended while closely monitoring process variables.
""")

        if estimated_bw < target_bw:

            recommendations = [
                {
                    "Recommendation": "Increase Stock Flow Slightly",
                    "Reason": f"Estimated Basis Weight ({estimated_bw:.2f} gsm) is slightly below the Target ({target_bw} gsm).",
                    "Source": "Engineering Rule Base"
                },
                {
                    "Recommendation": "Reduce Machine Speed Slightly",
                    "Reason": "Small speed reductions can improve basis weight without disturbing production.",
                    "Source": "Honeywell Best Practices"
                },
                {
                    "Recommendation": "Monitor Basis Weight Every 5 Minutes",
                    "Reason": "Confirm that the process moves toward the target grade.",
                    "Source": "Engineering Rule Base"
                }
            ]

        else:

            recommendations = [
                {
                    "Recommendation": "Reduce Stock Flow Slightly",
                    "Reason": f"Estimated Basis Weight ({estimated_bw:.2f} gsm) is slightly above the Target ({target_bw} gsm).",
                    "Source": "Engineering Rule Base"
                },
                {
                    "Recommendation": "Increase Machine Speed Slightly",
                    "Reason": "Small speed increases help reduce basis weight gradually.",
                    "Source": "Honeywell Best Practices"
                },
                {
                    "Recommendation": "Monitor Basis Weight Every 5 Minutes",
                    "Reason": "Ensure the transition remains within tolerance.",
                    "Source": "Engineering Rule Base"
                }
            ]

    else:

        st.success("""
The grade transition is stable.

No corrective action is required. Continue monitoring until the target grade is achieved.
""")

        recommendations = [
            {
                "Recommendation": "Continue Current Operating Conditions",
                "Reason": "Estimated Basis Weight is within the allowable transition tolerance.",
                "Source": "Engineering Rule Base"
            }
        ]

else:

    recommendations = get_recommendation(
        stock_flow,
        filler_flow,
        steam_pressure,
        machine_speed,
        moisture,
        ash,
        caliper
    )

if len(recommendations) == 0:

    st.success("No corrective action is required.")

else:

    for rec in recommendations:

        st.markdown(f"""
<div style="
background:white;
border-left:5px solid #005EB8;
padding:15px;
margin-bottom:12px;
border-radius:8px;
box-shadow:0 2px 6px rgba(0,0,0,0.08);
">

<b>{rec['Recommendation']}</b><br><br>

<b>Reason</b><br>
{rec['Reason']}<br><br>

<b>Reference</b><br>
{rec['Source']}

</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(
    [
        "Feature Importance",
        "Correlation Analysis",
        "Engineering Insights"
    ]
)


with tab1:

    st.subheader("Feature Importance")

    importance = pd.DataFrame({

        "Feature": input_data.columns,

        "Importance": model.feature_importances_

    })

    importance = importance.sort_values(
        by="Importance",
        ascending=True
    )

    fig, ax = plt.subplots(figsize=(8,5))

    ax.barh(
        importance["Feature"],
        importance["Importance"],
        color="#005EB8"
    )

    ax.set_xlabel("Importance Score")

    ax.set_ylabel("")

    ax.set_title("Model Feature Importance")

    st.pyplot(fig)

    st.info(
        """
The chart shows the contribution of each process variable to the AI prediction.
Higher importance indicates a stronger influence on Off-Spec prediction.
        """
    )
with tab2:

    st.subheader("Correlation Matrix")

    corr = df[
        [
            "Stock Flow (L/min)",
            "Filler Flow (kg/min)",
            "Steam Pressure (bar)",
            "Machine Speed (m/min)",
            "Moisture (%)",
            "Ash (%)",
            "Caliper (mm)",
            "Basis Weight (gsm)"
        ]
    ].corr()

    fig2, ax2 = plt.subplots(figsize=(9,7))

    heatmap = ax2.imshow(
        corr,
        cmap="coolwarm",
        vmin=-1,
        vmax=1
    )

    ax2.set_xticks(range(len(corr.columns)))
    ax2.set_xticklabels(
        corr.columns,
        rotation=45,
        ha="right"
    )

    ax2.set_yticks(range(len(corr.columns)))
    ax2.set_yticklabels(corr.columns)

    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):

            ax2.text(
                j,
                i,
                f"{corr.iloc[i,j]:.2f}",
                ha="center",
                va="center",
                fontsize=8
            )

    plt.colorbar(heatmap)

    st.pyplot(fig2)

    st.info(
        """
Correlation values close to +1 indicate strong positive relationships,
while values close to -1 indicate strong negative relationships.
        """
    )

with tab3:

    st.subheader("Engineering Insights")

    st.markdown("### Process Relationships")

    insight_data = [

        (
            "Stock Flow",
            "Basis Weight",
            "High",
            "Increasing stock flow generally increases basis weight."
        ),

        (
            "Steam Pressure",
            "Moisture",
            "High",
            "Steam pressure directly influences paper drying."
        ),

        (
            "Machine Speed",
            "Caliper",
            "Medium",
            "Higher speed generally reduces paper thickness."
        ),

        (
            "Filler Flow",
            "Ash",
            "High",
            "Stable filler addition improves ash consistency."
        )

    ]

    insight_df = pd.DataFrame(
        insight_data,
        columns=[
            "Parameter",
            "Influenced Variable",
            "Impact",
            "Engineering Interpretation"
        ]
    )

    st.dataframe(
        insight_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.subheader("Key Findings")

    st.markdown("""

**Primary Process Drivers**

- Stock Flow has the highest influence on Basis Weight.
- Steam Pressure controls drying performance.
- Machine Speed affects sheet thickness.
- Filler Flow determines Ash consistency.

**Operational Recommendations**

- Stabilize Stock Flow before changing production rate.
- Avoid rapid Machine Speed changes during grade transitions.
- Maintain Steam Pressure throughout stabilization.
- Monitor Basis Weight continuously until the target grade is achieved.

""")

st.markdown("---")

tab4, tab5 = st.tabs(
    [
        "Historical Trends",
        "AI Summary"
    ]
)

with tab4:

    st.subheader("Historical Process Trends")

    col1, col2 = st.columns(2)

    with col1:

        history_range = st.selectbox(
            "History Range",
            [
                "Last 100 Records",
                "Last 500 Records",
                "Entire Dataset"
            ]
        )

    with col2:

        selected = st.selectbox(
            "Process Variable",
            [
                "Stock Flow (L/min)",
                "Filler Flow (kg/min)",
                "Steam Pressure (bar)",
                "Machine Speed (m/min)",
                "Moisture (%)",
                "Ash (%)",
                "Caliper (mm)",
                "Basis Weight (gsm)"
            ]
        )

    if history_range == "Last 100 Records":
        trend = df.tail(100)

    elif history_range == "Last 500 Records":
        trend = df.tail(500)

    else:
        trend = df

    fig, ax = plt.subplots(figsize=(12,5))

    ax.plot(
        trend["Timestamp"],
        trend[selected],
        linewidth=2,
        color="#005EB8"
    )

    ax.set_title(selected)

    ax.set_xlabel("Timestamp")

    ax.set_ylabel(selected)

    plt.xticks(rotation=45)

    plt.tight_layout()

    st.pyplot(fig)

    mean = trend[selected].mean()
    minimum = trend[selected].min()
    maximum = trend[selected].max()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Average",
            f"{mean:.2f}"
        )

    with c2:
        st.metric(
            "Minimum",
            f"{minimum:.2f}"
        )

    with c3:
        st.metric(
            "Maximum",
            f"{maximum:.2f}"
        )


with tab5:

    st.subheader("AI Decision Summary")

    summary = []

    if transition:
        summary.append(
            "Grade transition is currently in progress."
        )

    else:
        summary.append(
            "Machine is operating at steady state."
        )

    if prediction == 1:

        summary.append(
            "AI predicts a potential Off-Spec condition."
        )

    else:

        summary.append(
            "AI predicts production within specification."
        )

    if deviation > limit:

        summary.append(
            "Estimated Basis Weight deviation exceeds allowable tolerance."
        )

    else:

        summary.append(
            "Estimated Basis Weight is within acceptable tolerance."
        )

    st.markdown("### Executive Summary")

    for item in summary:

        st.markdown(f"- {item}")

    st.markdown("---")

    st.subheader("Recommended Operator Actions")

    recommendations = get_recommendation(
        stock_flow,
        filler_flow,
        steam_pressure,
        machine_speed,
        moisture,
        ash,
        caliper
    )

    if len(recommendations) == 0:

        st.success(
            "No corrective action is required."
        )

    else:

        for rec in recommendations:

            st.markdown(
                f"""
<div style="
background:white;
padding:18px;
border-radius:10px;
border-left:5px solid #005EB8;
margin-bottom:10px;
">

<b>{rec['Recommendation']}</b>

<br><br>

<b>Reason</b><br>

{rec['Reason']}

<br><br>

<b>Reference</b><br>

{rec['Source']}

</div>
""",
                unsafe_allow_html=True
            )

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Prediction",
            "Off-Spec" if prediction else "Within Spec"
        )

    with c2:
        st.metric(
            "Confidence",
            f"{max(probability)*100:.2f}%"
        )

    with c3:
        st.metric(
            "Deviation",
            f"{deviation:.2f} gsm"
        )

st.markdown("---")


st.subheader("Operator Feedback")

st.write(
    "Record whether the AI recommendation was accepted or rejected. "
    "This feedback can be used to evaluate AI performance over time."
)

col1, col2 = st.columns(2)

with col1:

    if st.button("Accept Recommendation", use_container_width=True):

        feedback = pd.DataFrame({

            "Timestamp":[datetime.now()],

            "Prediction":[
                "Off-Spec" if prediction else "Within Spec"
            ],

            "Confidence":[
                round(max(probability)*100,2)
            ],

            "Current Grade":[current_grade],

            "Target Grade":[target_grade],

            "Response":["Accepted"]

        })

        try:

            history = pd.read_csv("feedback.csv")

            feedback = pd.concat(
                [history, feedback],
                ignore_index=True
            )

        except FileNotFoundError:

            pass

        feedback.to_csv(
            "feedback.csv",
            index=False
        )

        st.success("Feedback saved successfully.")

with col2:

    if st.button("Reject Recommendation", use_container_width=True):

        feedback = pd.DataFrame({

            "Timestamp":[datetime.now()],

            "Prediction":[
                "Off-Spec" if prediction else "Within Spec"
            ],

            "Confidence":[
                round(max(probability)*100,2)
            ],

            "Current Grade":[current_grade],

            "Target Grade":[target_grade],

            "Response":["Rejected"]

        })

        try:

            history = pd.read_csv("feedback.csv")

            feedback = pd.concat(
                [history, feedback],
                ignore_index=True
            )

        except FileNotFoundError:

            pass

        feedback.to_csv(
            "feedback.csv",
            index=False
        )

        st.success("Feedback saved successfully.")

st.markdown("---")

st.subheader("Recent Feedback History")

try:

    history = pd.read_csv("feedback.csv")

    if len(history) > 0:

        st.dataframe(

            history.tail(10),

            use_container_width=True,

            hide_index=True

        )

    else:

        st.info("No feedback records available.")

except FileNotFoundError:

    st.info("No feedback has been recorded yet.")

st.markdown("---")

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Model Status",
        "Online"
    )

with c2:

    st.metric(
        "Recommendation Engine",
        "Active"
    )

with c3:

    st.metric(
        "Dataset Records",
        f"{len(df):,}"
    )


st.markdown("---")

st.markdown(
"""
<div style="
text-align:center;
padding:20px;
color:#6B7280;
font-size:14px;
">

<b>Honeywell AI Grade Change Intelligence</b><br>

Predictive Decision Support for Paper Manufacturing<br>

Random Forest Prediction • Engineering Rule Engine •
Historical Trend Analysis • Process Analytics

</div>
""",
unsafe_allow_html=True
)