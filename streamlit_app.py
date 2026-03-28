import streamlit as st
import pandas as pd
import random
import plotly.express as px
from datetime import datetime, timedelta

# 1. Page Configuration & Enlarged Easter Egg
st.set_page_config(page_title="Konecranes OTD Optimizer", layout="wide")
st.markdown("<div style='text-align: center; color: #FFD700; font-size: 18px; font-weight: bold; font-family: monospace; letter-spacing: 3px;'>WAKANDA FOREVER！</div>", unsafe_allow_html=True)

st.title("🏗️ Konecranes OTD Simulator(90 DAYS)")
st.write("Dynamic simulation comparing Legacy static models vs. the New Tiered-Penalty & Learning framework.")

# 2. Supplier Profiles & Initial Parameters
supplier_profiles = {
    "Nordic Steel Works": {"Commodity": "Steel Structures", "Incoterm": "FCA", "Base_Prob": 0.15, "Base_Fine": 600},
    "Siemens Drives": {"Commodity": "Heavy Motors", "Incoterm": "DAP", "Base_Prob": 0.20, "Base_Fine": 800},
    "Taiwan Semi": {"Commodity": "Microchips", "Incoterm": "FCA", "Base_Prob": 0.35, "Base_Fine": 400},
    "Global Hydraulics": {"Commodity": "Hydraulic Pumps", "Incoterm": "DDP", "Base_Prob": 0.25, "Base_Fine": 500}
}

root_causes = [
    {"cause": "Production Capacity Issue", "type": "Supplier"},
    {"cause": "Quality QA/QC Failure", "type": "Supplier"},
    {"cause": "Raw Material Shortage", "type": "Supplier"},
    {"cause": "Port Congestion / Vessel Delay", "type": "Logistics"},
    {"cause": "Customs Clearance Hold", "type": "Logistics"},
    {"cause": "Extreme Weather / Typhoon", "type": "Force Majeure"}
]

st.sidebar.header("⚙️ Simulation Params")
orders_per_day = st.sidebar.slider("Daily Average Orders", 10, 30, 15)
learning_rate = st.sidebar.slider("Supplier Learning Rate (%)", 5, 30, 15)
run_btn = st.sidebar.button("🚀 Run 90-Day Simulation")

if run_btn:
    data = []
    trend_data = [] # Data array for the Before vs After trend chart
    tier2_tracker = {sup: 0 for sup in supplier_profiles} # Tracker for AI insights popup
    
    start_date = datetime(2024, 1, 1)
    
    # current_probs updates dynamically (New Framework), base_probs remains static (Legacy System)
    current_probs = {name: info["Base_Prob"] for name, info in supplier_profiles.items()}
    
    # 3. Core 90-Day Time-Series Simulation
    for day in range(90):
        current_date = start_date + timedelta(days=day)
        daily_legacy_delays = 0
        daily_new_delays = 0
        
        for _ in range(orders_per_day):
            sup_name = random.choice(list(supplier_profiles.keys()))
            sup_info = supplier_profiles[sup_name]
            
            # --- Parallel Universe 1: Legacy System (Static probability, no learning) ---
            if random.random() < sup_info["Base_Prob"]:
                daily_legacy_delays += 1

            # --- Parallel Universe 2: New Framework (Dynamic learning & tiered penalties) ---
            is_delayed_new = random.random() < current_probs[sup_name]
            
            if is_delayed_new:
                daily_new_delays += 1
                days_late = random.randint(1, 21)
                issue = random.choice(root_causes)
                
                # Incoterms Logic Execution
                accountable = issue['type']
                if issue['type'] == 'Logistics':
                    if sup_info['Incoterm'] in ['DAP', 'DDP']:
                        accountable = 'Supplier (Transit Liability)'
                    elif sup_info['Incoterm'] in ['FCA']:
                        accountable = 'Konecranes Freight Forwarder Claim'
                
                # Tiered Penalty & Learning Curve Implementation
                penalty = 0
                action_tier = "Tier 1: Warning"
                
                if accountable == 'Force Majeure':
                    action_tier = "Exempt (Act of God)"
                elif accountable == 'Konecranes Freight Forwarder Claim':
                    action_tier = "Freight Claim"
                    penalty = days_late * 200
                else: # Supplier is formally at fault
                    if days_late <= 3:
                        action_tier = "Tier 1: Warning & 8D Report"
                    elif days_late <= 14:
                        action_tier = "Tier 2: Financial Penalty"
                        penalty = days_late * sup_info['Base_Fine']
                        tier2_tracker[sup_name] += 1 # Track recurring offenses
                        
                        # KEY LOGIC: Probability drops after a financial penalty (Learning effect)
                        current_probs[sup_name] = max(0.05, current_probs[sup_name] * (1 - (learning_rate/100)))
                    else:
                        action_tier = "Tier 3: Termination Review"
                        penalty = days_late * sup_info['Base_Fine'] * 1.5
                        
                        # KEY LOGIC: Drastic improvement mandated after critical review
                        current_probs[sup_name] = max(0.05, current_probs[sup_name] * 0.5)
                
                data.append({
                    "Date": current_date,
                    "Order ID": f"KC-PO-{10000 + day * 100 + _}",
                    "Supplier": sup_name,
                    "Incoterm": sup_info['Incoterm'],
                    "Root Cause": issue['cause'],
                    "Delay Days": days_late,
                    "Final Accountability": accountable,
                    "Enforcement Action": action_tier,
                    "Penalty ($)": penalty
                })
        
        # End of day: Record aggregated data for trend comparison
        trend_data.append({
            "Date": current_date,
            "Legacy System (Static)": daily_legacy_delays,
            "New System (Dynamic Learning)": daily_new_delays
        })
                
    df = pd.DataFrame(data)
    df_trend = pd.DataFrame(trend_data)

    # 4. Visualization & Dashboard
    st.header("📈 Q1 Supply Chain Performance Dashboard")
    
    # --- Feature: Dual-line Comparison Chart (Before vs After) ---
    st.subheader("System Comparison: Legacy vs. New Framework")
    
    # Use 7-Day Moving Average to smooth the trend lines for better readability
    df_trend['Legacy Trend'] = df_trend['Legacy System (Static)'].rolling(7).mean()
    df_trend['New Trend'] = df_trend['New System (Dynamic Learning)'].rolling(7).mean()
    
    fig_line = px.line(df_trend, x='Date', y=['Legacy Trend', 'New Trend'], 
                       labels={'value': '7-Day Moving Average of Delays', 'variable': 'System Type'},
                       color_discrete_map={"Legacy Trend": "#ef553b", "New Trend": "#00cc96"})
    
    # Add fill color to highlight the performance gap (The value saved)
    fig_line.update_traces(fill='tozeroy', fillcolor='rgba(0, 204, 150, 0.1)', selector=dict(name='New Trend'))
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Financial Impact by Supplier")
        fig_bar = px.bar(df, x="Supplier", y="Penalty ($)", color="Enforcement Action", barmode="stack")
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.subheader("Accountability Breakdown (Corrected)")
        fig_pie = px.pie(df, names='Final Accountability', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    # --- Feature: AI Strategic Sourcing Insights Popup ---
    st.markdown("---")
    st.subheader(" Automatic Strategic Sourcing Insights")
    insight_triggered = False
    
    for sup, count in tier2_tracker.items():
        # Trigger critical alert if penalized heavily within 90 days
        if count > 10: 
            insight_triggered = True
            st.error(f"🚨 **CRITICAL RISK DETECTED:** {sup} has consistently triggered Tier 2/3 penalties ({count} times). \n\n**Recommendation:** \n1. Adjust SAP Lead Time from 30 days to 45 days immediately to reflect reality.\n2. Initiate Dual-Sourcing protocol to reduce dependency.")
        # Trigger warning for moderate instability
        elif count > 5:
            insight_triggered = True
            st.warning(f"⚠️ **WARNING:** {sup} shows unstable delivery reliability. \n\n**Recommendation:** Mandate a supplier capacity audit and review current Incoterm ({supplier_profiles[sup]['Incoterm']}) suitability.")
            
    if not insight_triggered:
        st.success("✅ All suppliers are responding positively to the new learning framework. No critical systemic bottlenecks detected.")

    st.subheader("📋 Enforcement Audit Log")
    st.dataframe(df.sort_values('Date', ascending=False), use_container_width=True)
else:
    st.info("👈 Set the parameters and click 'Run 90-Day Simulation'.")
