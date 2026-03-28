import streamlit as st
import pandas as pd
import random
import plotly.express as px
from datetime import datetime, timedelta

# ==========================================
# 1. UI Setup & Branding
# ==========================================
st.set_page_config(page_title="Konecranes OTD Optimizer", layout="wide")
st.markdown("<div style='text-align: center; color: #FFD700; font-size: 18px; font-weight: bold; font-family: monospace; letter-spacing: 3px;'>WAKANDA FOREVER</div>", unsafe_allow_html=True)

st.title("🏗️ Konecranes OTD Simulator（90 day）")
st.write("Dynamic simulation comparing the static **Old System** against the perfect **Wakanda System 2.0**.")

# ==========================================
# 2. Supply Chain Data Definitions
# ==========================================
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

st.sidebar.header("Simulation Params")
orders_per_day = st.sidebar.slider("Daily Average Orders", 10, 30, 15)
learning_rate = st.sidebar.slider("Supplier Learning Rate (%)", 5, 30, 15)
run_btn = st.sidebar.button("Run 90-Day Simulation here")

# ==========================================
# 3. Core Simulation Engine
# ==========================================
if run_btn:
    all_orders = [] # Track every single order for accurate OTD% calculation
    
    start_date = datetime(2024, 1, 1)
    current_probs = {name: info["Base_Prob"] for name, info in supplier_profiles.items()}
    
    for day in range(90):
        current_date = start_date + timedelta(days=day)
        
        for _ in range(orders_per_day):
            sup_name = random.choice(list(supplier_profiles.keys()))
            sup_info = supplier_profiles[sup_name]
            
            # --- Old System Logic (Static, Unfair Penalty) ---
            is_delayed_old = random.random() < sup_info["Base_Prob"]
            old_penalty = 0
            if is_delayed_old:
                days_late_old = random.randint(1, 21)
                # Old system blames everything on the supplier blindly
                old_penalty = days_late_old * sup_info['Base_Fine'] 

            # --- Wakanda System 2.0 Logic (Dynamic, Incoterms, Tiers) ---
            is_delayed_wakanda = random.random() < current_probs[sup_name]
            wakanda_penalty = 0
            action_tier = "On Time"
            accountable = "None"
            issue_cause = "None"
            days_late_wakanda = 0
            
            if is_delayed_wakanda:
                days_late_wakanda = random.randint(1, 21)
                issue = random.choice(root_causes)
                issue_cause = issue['cause']
                accountable = issue['type']
                
                # Incoterms check
                if issue['type'] == 'Logistics':
                    if sup_info['Incoterm'] in ['DAP', 'DDP']:
                        accountable = 'Supplier (Transit Liability)'
                    elif sup_info['Incoterm'] in ['FCA']:
                        accountable = 'Konecranes Freight Forwarder'
                
                # Tiered Penalties & Learning Curve
                if accountable == 'Force Majeure':
                    action_tier = "Exempt (Act of God)"
                elif accountable == 'Konecranes Freight Forwarder':
                    action_tier = "Freight Claim"
                    wakanda_penalty = days_late_wakanda * 200 # Fixed freight penalty
                else: 
                    # Supplier formally at fault
                    if days_late_wakanda <= 3:
                        action_tier = "Tier 1: Warning & 8D"
                    elif days_late_wakanda <= 14:
                        action_tier = "Tier 2: Financial Penalty"
                        wakanda_penalty = days_late_wakanda * sup_info['Base_Fine']
                        current_probs[sup_name] = max(0.05, current_probs[sup_name] * (1 - (learning_rate/100)))
                    else:
                        action_tier = "Tier 3: Termination Review"
                        wakanda_penalty = days_late_wakanda * sup_info['Base_Fine'] * 1.5
                        current_probs[sup_name] = max(0.05, current_probs[sup_name] * 0.5)
            
            # Log the order
            all_orders.append({
                "Date": current_date,
                "Order ID": f"KC-PO-{10000 + day * 100 + _}",
                "Supplier": sup_name,
                "Incoterm": sup_info['Incoterm'],
                "Old_Delayed": 1 if is_delayed_old else 0,
                "Old_Penalty ($)": old_penalty,
                "Wakanda_Delayed": 1 if is_delayed_wakanda else 0,
                "Root Cause": issue_cause,
                "Days Late": days_late_wakanda,
                "Accountable Party": accountable,
                "Enforcement Action": action_tier,
                "Wakanda_Penalty ($)": wakanda_penalty
            })
            
    df_all = pd.DataFrame(all_orders)

    # ==========================================
    # 4. OTD% Trend & Drill-down (Options B & C)
    # ==========================================
    st.header("📈 Supply Chain Performance Dashboard")
    
    st.subheader("System Comparison: OTD% Trend (Old System vs. Wakanda System 2.0)")
    
    # Drill-down selector
    supplier_filter = st.selectbox("Select View (Drill-down Analysis):", ["All Suppliers"] + list(supplier_profiles.keys()))
    
    # Filter data based on selection
    if supplier_filter == "All Suppliers":
        df_trend = df_all.copy()
    else:
        df_trend = df_all[df_all['Supplier'] == supplier_filter].copy()
        
    # Calculate daily OTD %
    daily_stats = df_trend.groupby('Date').agg(
        Total_Orders=('Order ID', 'count'),
        Old_Delays=('Old_Delayed', 'sum'),
        Wakanda_Delays=('Wakanda_Delayed', 'sum')
    ).reset_index()
    
    daily_stats['Old System OTD%'] = ((daily_stats['Total_Orders'] - daily_stats['Old_Delays']) / daily_stats['Total_Orders']) * 100
    daily_stats['Wakanda System 2.0 OTD%'] = ((daily_stats['Total_Orders'] - daily_stats['Wakanda_Delays']) / daily_stats['Total_Orders']) * 100
    
    # 7-Day Moving Average for smooth curves
    daily_stats['Old System OTD% (7-Day Avg)'] = daily_stats['Old System OTD%'].rolling(7).mean()
    daily_stats['Wakanda System 2.0 OTD% (7-Day Avg)'] = daily_stats['Wakanda System 2.0 OTD%'].rolling(7).mean()

    fig_otd = px.line(daily_stats, x='Date', y=['Old System OTD% (7-Day Avg)', 'Wakanda System 2.0 OTD% (7-Day Avg)'], 
                       labels={'value': 'On-Time Delivery (OTD) %', 'variable': 'Framework'},
                       color_discrete_map={"Old System OTD% (7-Day Avg)": "#ef553b", "Wakanda System 2.0 OTD% (7-Day Avg)": "#00cc96"})
    
    fig_otd.update_traces(fill='tozeroy', fillcolor='rgba(0, 204, 150, 0.1)', selector=dict(name='Wakanda System 2.0 OTD% (7-Day Avg)'))
    st.plotly_chart(fig_otd, use_container_width=True)

    st.markdown("---")

    # ==========================================
    # 5. Financial Impact & Accountability (Side-by-Side)
    # ==========================================
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Financial Penalty Breakdown")
        st.markdown("*Old System unfairly billed suppliers. Wakanda 2.0 redistributes blame to forwarders/exceptions.*")
        
        # Aggregate financial data
        fin_impact = df_all.groupby('Supplier').agg(
            Old_System_Penalty=('Old_Penalty ($)', 'sum'),
            Wakanda_Supplier_Penalty=('Wakanda_Penalty ($)', lambda x: df_all.loc[x.index][df_all['Accountable Party'].str.contains('Supplier')]['Wakanda_Penalty ($)'].sum())
        ).reset_index()
        
        fin_melt = fin_impact.melt(id_vars='Supplier', var_name='System', value_name='Penalty ($)')
        fig_bar = px.bar(fin_melt, x='Supplier', y='Penalty ($)', color='System', barmode='group',
                         color_discrete_map={'Old_System_Penalty': '#ef553b', 'Wakanda_Supplier_Penalty': '#00cc96'})
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.subheader("Wakanda 2.0: True Accountability")
        df_delayed_wakanda = df_all[df_all['Wakanda_Delayed'] == 1]
        fig_pie = px.pie(df_delayed_wakanda, names='Accountable Party', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    # ==========================================
    # 6. Automated Risk Detection (Structured Cards)
    # ==========================================
    st.markdown("---")
    st.subheader("Automated Risk Detection")
    st.markdown("based on **Wakanda System 2.0** 90-day performance data.")
    
    col_cards = st.columns(len(supplier_profiles))
    
    for idx, (sup, info) in enumerate(supplier_profiles.items()):
        sup_data = df_delayed_wakanda[df_delayed_wakanda['Supplier'] == sup]
        total_delays = len(sup_data)
        tier3_count = len(sup_data[sup_data['Enforcement Action'] == 'Tier 3: Termination Review'])
        
        top_cause = sup_data['Root Cause'].mode()[0] if not sup_data.empty else "N/A"
        
        with col_cards[idx]:
            if tier3_count > 4 or total_delays > 30:
                st.error(f"🚨 **Critical Alert: {sup}**\n"
                         f"- **Total Delays:** {total_delays}\n"
                         f"- **Tier 3 Breaches:** {tier3_count}\n"
                         f"- **Primary Cause:** {top_cause}\n\n"
                         f"**Actionable Recommendation:**\n"
                         f"Increase SAP Lead Time immediately. Initiate Dual-Sourcing protocol.")
            elif total_delays > 15:
                st.warning(f"⚠️ **Warning: {sup}**\n"
                         f"- **Total Delays:** {total_delays}\n"
                         f"- **Tier 3 Breaches:** {tier3_count}\n"
                         f"- **Primary Cause:** {top_cause}\n\n"
                         f"**Actionable Recommendation:**\n"
                         f"Schedule capacity audit. Review {info['Incoterm']} suitability.")
            else:
                st.success(f"✅ **Stable: {sup}**\n"
                         f"- **Total Delays:** {total_delays}\n"
                         f"- **Tier 3 Breaches:** {tier3_count}\n"
                         f"- **Primary Cause:** {top_cause}\n\n"
                         f"**Status:**\n"
                         f"Performing within acceptable OTD tolerances.")

    # ==========================================
    # 7. Interactive Enforcement Audit Log (Wakanda 2.0)
    # ==========================================
    st.markdown("---")
    st.subheader("📋 Enforcement Audit Log (Wakanda System 2.0)")
    st.markdown("This verified ledger is generated exclusively by the **Wakanda System 2.0** accountability framework.")
    
    # Interactive Filters
    log_c1, log_c2 = st.columns(2)
    filter_sup = log_c1.selectbox("Filter by Supplier:", ["All"] + list(supplier_profiles.keys()))
    filter_action = log_c2.selectbox("Filter by Enforcement Action:", ["All", "Tier 1: Warning & 8D", "Tier 2: Financial Penalty", "Tier 3: Termination Review", "Freight Claim", "Exempt (Act of God)"])
    
    df_log = df_delayed_wakanda[['Date', 'Order ID', 'Supplier', 'Incoterm', 'Root Cause', 'Days Late', 'Accountable Party', 'Enforcement Action', 'Wakanda_Penalty ($)']].copy()
    
    if filter_sup != "All":
        df_log = df_log[df_log['Supplier'] == filter_sup]
    if filter_action != "All":
        df_log = df_log[df_log['Enforcement Action'] == filter_action]
    
    # Pandas Styler for Color-Coding
    def color_tiers(val):
        color = ''
        if val == 'Tier 3: Termination Review':
            color = 'background-color: #ff4b4b; color: white' # Red
        elif val == 'Tier 2: Financial Penalty':
            color = 'background-color: #ffad15; color: black' # Orange
        elif val == 'Tier 1: Warning & 8D':
            color = 'background-color: #fce83a; color: black' # Yellow
        return color
    
    styled_log = df_log.sort_values('Date', ascending=False).style.applymap(color_tiers, subset=['Enforcement Action'])
    
    # Display the styled dataframe
    st.dataframe(styled_log, use_container_width=True)
    
    # Export to CSV Feature
    csv = df_log.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Audit Log (CSV)",
        data=csv,
        file_name='wakanda_system_audit_log.csv',
        mime='text/csv',
    )
else:
    st.info(" Set the parameters and click 'Run 90-Day Simulation'.")
