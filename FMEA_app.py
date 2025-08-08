import streamlit as st
import pandas as pd
import numpy as np
import os
import json

# Define CPP–CQA map as per ICH/FDA guidelines
cpp_cqa_map = {
    "Wet Granulation": {
        "CPP": ["Binder Addition Rate", "Mixing Time", "Granulation Time", "Inlet Temperature", "Impeller Speed", "Drying Time"],
        "CQA": ["Granule Size", "Moisture Content", "Tablet Hardness", "Content Uniformity", "Dissolution"]
    },
    "Dry Granulation (Roller Compaction)": {
        "CPP": ["Roll Pressure", "Feed Screw Speed", "Roll Speed", "Milling Speed"],
        "CQA": ["Ribbon Density", "Granule Size", "Tablet Friability", "Tablet Hardness", "Content Uniformity"]
    },
    "Direct Compression": {
        "CPP": ["Blending Time", "Lubrication Time", "Mixing Speed"],
        "CQA": ["Content Uniformity", "Tablet Weight Variation", "Dissolution", "Tablet Hardness"]
    }
}

# RPN color level
def get_risk_level_color(rpn):
    if rpn >= 120:
        return "🔴 High"
    elif rpn >= 60:
        return "🟠 Medium"
    else:
        return "🟢 Low"

st.title("🧪 AI-Powered CPP–CQA Risk Assessment Tool")
st.caption("ICH Q8(R2), Q9, FDA QbD & ANDA Compliance")

# Select granulation type
granulation_type = st.selectbox("📂 Select Granulation Type", list(cpp_cqa_map.keys()))

cpps = cpp_cqa_map[granulation_type]["CPP"]
cqas = cpp_cqa_map[granulation_type]["CQA"]

# Optional: manual overrides
st.subheader("⚙️ Optional: Override AI Risk Scoring")

use_manual = st.checkbox("Use manual inputs for risk scoring", value=False)

risk_data = []

for cpp in cpps:
    for cqa in cqas:
        if use_manual:
            severity = st.slider(f"🔹 Severity of '{cpp}' on '{cqa}'", 1, 10, 5)
            occurrence = st.slider(f"🔹 Occurrence for '{cpp}'", 1, 10, 5)
            detectability = st.slider(f"🔹 Detectability of failure for '{cpp}'", 1, 10, 5)
        else:
            # AI-style logic (can be replaced by LLM or ML backend)
            severity = 9 if "content" in cqa.lower() or "dissolution" in cqa.lower() else 6
            occurrence = 7 if "Mixing" in cpp or "Roll" in cpp else 4
            detectability = 4 if "Granule Size" in cqa or "Tablet Hardness" in cqa else 5

        rpn = severity * occurrence * detectability
        level = get_risk_level_color(rpn)

        risk_data.append({
            "CPP": cpp,
            "CQA": cqa,
            "Severity": severity,
            "Occurrence": occurrence,
            "Detectability": detectability,
            "RPN": rpn,
            "Risk Level": level
        })

# Convert to DataFrame
risk_df = pd.DataFrame(risk_data)

st.subheader("📋 FMEA Risk Table")
st.dataframe(risk_df, use_container_width=True)

# Save/load session
st.subheader("💾 Session Management")
save_name = st.text_input("Filename to save/load", value="risk_session.json")

col1, col2 = st.columns(2)

with col1:
    if st.button("💾 Save Session"):
        with open(save_name, "w") as f:
            json.dump(risk_data, f)
        st.success("Session saved!")

with col2:
    if st.button("📂 Load Session"):
        if os.path.exists(save_name):
            with open(save_name, "r") as f:
                loaded_data = json.load(f)
                risk_df = pd.DataFrame(loaded_data)
                st.dataframe(risk_df, use_container_width=True)
        else:
            st.error("File not found!")



