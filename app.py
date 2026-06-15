import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- Streamlit Configurations ---
st.set_page_config(
    page_title="FLIGHT IQ // TACTICAL HUD",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Futuristic Space Cockpit styling via Custom CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
    /* General body & app structure with dark cockpit theme */
    .stApp {
        background-color: #0a0f1d;
        color: #e0e6ed;
        font-family: 'Share Tech Mono', 'Courier New', monospace;
    }
    
    /* Neon glow effect for headers */
    h1, h2, h3, h4, h5, h6 {
        color: #00f3ff !important;
        text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
        font-family: 'Share Tech Mono', monospace !important;
        letter-spacing: 2px;
    }
    
    /* Deep dark blue glowing sidebar configuration */
    section[data-testid="stSidebar"] {
        background-color: #0d1527 !important;
        border-right: 2px solid #00f3ff;
        box-shadow: 5px 0 15px rgba(0, 243, 255, 0.15);
    }
    
    /* Customize all metric boxes to look like instrument indicators */
    div[data-testid="stMetricContainer"] {
        background-color: rgba(13, 21, 39, 0.8) !important;
        border: 1px solid #00f3ff !important;
        box-shadow: 0 0 10px rgba(0, 243, 255, 0.2);
        border-radius: 8px;
        padding: 12px;
    }
    
    /* Streamlit interactive input adjustments */
    div[data-baseweb="select"] > div {
        background-color: #0d1527 !important;
        border: 1px solid #00f3ff !important;
        color: #00f3ff !important;
    }
    
    input {
        background-color: #0d1527 !important;
        color: #00f3ff !important;
        border: 1px solid #00f3ff !important;
    }
    
    /* Button custom hover styling for spaceship aesthetic */
    div.stButton > button {
        background-color: #0d1527 !important;
        color: #00f3ff !important;
        border: 2px solid #00f3ff !important;
        box-shadow: 0 0 8px rgba(0, 243, 255, 0.3);
        font-family: 'Share Tech Mono', monospace !important;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div.stButton > button:hover {
        background-color: #00f3ff !important;
        color: #0a0f1d !important;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.7);
    }

    /* Orange neon accents for buttons */
    .orange-accent div.stButton > button {
        border: 2px solid #ff5e00 !important;
        color: #ff5e00 !important;
        box-shadow: 0 0 8px rgba(255, 94, 0, 0.3);
    }
    .orange-accent div.stButton > button:hover {
        background-color: #ff5e00 !important;
        color: #0a0f1d !important;
        box-shadow: 0 0 15px rgba(255, 94, 0, 0.7);
    }
    
    /* Custom container grids */
    .hud-box {
        border: 1px solid #00f3ff;
        background-color: rgba(13, 21, 39, 0.6);
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 0 12px rgba(0, 243, 255, 0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)


# --- Mock Data Generation for Demo ---
def generate_demo_baseline():
    """Generates 10,000+ rows of Flight Baseline CSV to demonstrate scaling capacity."""
    np.random.seed(42)
    rows = 11000
    times = np.linspace(0, 3600, rows)
    return pd.DataFrame({
        'Time_sec': times,
        'Pitch_deg': np.random.normal(1.5, 0.5, rows),
        'Yaw_deg': (np.linspace(0, 180, rows) + np.random.normal(0, 0.2, rows)) % 360,
        'Roll_deg': np.random.normal(0.0, 1.2, rows),
        'Airspeed_knots': np.random.normal(420, 10, rows) + np.sin(times / 100) * 5,
        'Altitude_ft': 35000 + np.sin(times / 300) * 500 + np.random.normal(0, 20, rows)
    })

def generate_demo_recorded():
    """Generates 10,000+ rows of Recorded Flight telemetry with deviations."""
    np.random.seed(101)
    rows = 11000
    times = np.linspace(0, 3600, rows)
    return pd.DataFrame({
        'Time_sec': times,
        'Pitch_deg': np.random.normal(1.8, 0.7, rows),
        'Yaw_deg': (np.linspace(0, 181.5, rows) + np.random.normal(0, 0.4, rows)) % 360,
        'Roll_deg': np.random.normal(0.2, 1.8, rows),
        'Airspeed_knots': np.random.normal(412, 12, rows) + np.sin(times / 95) * 8,
        'Altitude_ft': 34850 + np.sin(times / 280) * 550 + np.random.normal(0, 30, rows)
    })

# --- Mathematical Helper Functions ---
def parse_units(column_name):
    """Programmatically detects logical units of typical aerospace telemetry."""
    col_lower = column_name.lower()
    if 'deg' in col_lower or 'yaw' in col_lower or 'pitch' in col_lower or 'roll' in col_lower or 'angle' in col_lower:
        return "°"
    elif 'speed' in col_lower or 'knot' in col_lower or 'velocity' in col_lower or 'mps' in col_lower:
        return " kts"
    elif 'alt' in col_lower or 'height' in col_lower or 'ft' in col_lower or 'feet' in col_lower:
        return " ft"
    elif 'sec' in col_lower or 'time' in col_lower:
        return " s"
    return ""

def haversine(lat1, lon1, lat2, lon2):
    """Calculates geodesic distance between coordinates using the Haversine formula."""
    R = 6371.0  # Earth's radius in kilometers
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def calculate_initial_bearing(lat1, lon1, lat2, lon2):
    """Computes bearing relative to True North for tracking steering corrections."""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    y = np.sin(dlon) * np.cos(lat2)
    x = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
    bearing = np.degrees(np.arctan2(y, x))
    return (bearing + 360) % 360

def latlon_to_cartesian(lat, lon, alt_meters, R_earth=6371000):
    """Projects lat/lon/altitude coordinates into standard 3D space vectors."""
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    r = R_earth + alt_meters
    x = r * np.cos(lat_rad) * np.cos(lon_rad)
    y = r * np.cos(lat_rad) * np.sin(lon_rad)
    z = r * np.sin(lat_rad)
    return x, y, z

def make_earth_grid(R=6371000):
    """Generates low-density 3D coordinate grids to render a glowing wireframe sphere."""
    lats = np.linspace(-90, 90, 10)
    lons = np.linspace(-180, 180, 18)
    traces = []
    
    # Latitudinal circles
    for lat in lats:
        theta = np.radians(lat)
        phi = np.radians(np.linspace(-180, 180, 50))
        x = R * np.cos(theta) * np.cos(phi)
        y = R * np.cos(theta) * np.sin(phi)
        z = R * np.sin(theta) * np.ones_like(phi)
        traces.append(go.Scatter3d(
            x=x, y=y, z=z, mode='lines',
            line=dict(color='rgba(0, 243, 255, 0.12)', width=1),
            showlegend=False, hoverinfo='none'
        ))
        
    # Longitudinal half-circles
    for lon in lons:
        phi = np.radians(lon)
        theta = np.radians(np.linspace(-90, 90, 50))
        x = R * np.cos(theta) * np.cos(phi)
        y = R * np.cos(theta) * np.sin(phi)
        z = R * np.sin(theta)
        traces.append(go.Scatter3d(
            x=x, y=y, z=z, mode='lines',
            line=dict(color='rgba(0, 243, 255, 0.12)', width=1),
            showlegend=False, hoverinfo='none'
        ))
    return traces


# --- Application Layout ---
st.markdown("<h1 style='text-align: center;'>FLIGHT IQ // SYSTEM TAC-HUD</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00f3ff;'>TACTICAL NAVIGATION & MISSION RECONNAISSANCE SYSTEM</p>", unsafe_allow_html=True)

# Navigation panel tabs
tab1, tab2 = st.tabs(["[ TELEMETRY COMPARISON ANALYZER ]", "[ FLIGHT TRAJECTORY NAVIGATOR ]"])

# ----------------------------------------------------
# TAB 1: FLIGHT OFP DATA ANALYSIS
# ----------------------------------------------------
with tab1:
    st.markdown("<h3>FLIGHT OVERALL FLIGHT PLAN (OFP) RECONNAISSANCE</h3>", unsafe_allow_html=True)
    
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        st.markdown("<div class='hud-box'>", unsafe_allow_html=True)
        st.markdown("<h4>BASELINE STRATEGY INTAKE</h4>", unsafe_allow_html=True)
        baseline_file = st.file_uploader("Upload Standard Baseline CSV", type=["csv"], key="baseline")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_up2:
        st.markdown("<div class='hud-box'>", unsafe_allow_html=True)
        st.markdown("<h4>MISSION FLIGHT DATA TELEMETRY INTAKE</h4>", unsafe_allow_html=True)
        recorded_file = st.file_uploader("Upload Recorded Flight CSV", type=["csv"], key="recorded")
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Standardize baseline/recorded tables
    if baseline_file is not None:
        df_base = pd.read_csv(baseline_file)
    else:
        df_base = generate_demo_baseline()
        st.info("[DEMO BASELINE ACTIVE] Default 11,000 records loaded.")
        
    if recorded_file is not None:
        df_rec = pd.read_csv(recorded_file)
    else:
        df_rec = generate_demo_recorded()
        st.info("[DEMO TELEMETRY ACTIVE] Default 11,000 records loaded.")
        
    # Header Parsing from Recorded CSV
    rec_headers = list(df_rec.columns)
    
    st.markdown("<div class='hud-box'>", unsafe_allow_html=True)
    st.markdown("<h4>SELECT SENSOR PARAMETERS TO INSPECT</h4>", unsafe_allow_html=True)
    selected_cols = st.multiselect(
        "Select variables for comparison",
        options=[col for col in rec_headers if col != "Time_sec"],
        default=[col for col in rec_headers if col in ["Pitch_deg", "Airspeed_knots", "Altitude_ft"]]
    )
    
    st.markdown("<div class='orange-accent'>", unsafe_allow_html=True)
    calc_trigger = st.button("CALCULATE TELEMETRY DIFFERENTIALS")
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    if calc_trigger:
        if not selected_cols:
            st.error("Select at least one metric to compute calculations.")
        else:
            st.markdown("<h3>TELEMETRY COMPARATIVE ENGINE OUTPUT</h3>", unsafe_allow_html=True)
            
            grid_cols = st.columns(len(selected_cols))
            
            for idx, col in enumerate(selected_cols):
                mean_b = df_base[col].mean() if col in df_base.columns else np.nan
                mean_r = df_rec[col].mean()
                
                unit_label = parse_units(col)
                
                with grid_cols[idx]:
                    if np.isnan(mean_b):
                        st.metric(
                            label=f"Avg {col} (Recorded)",
                            value=f"{mean_r:.2f}{unit_label}",
                            delta="No baseline ref"
                        )
                    else:
                        diff = mean_r - mean_b
                        st.metric(
                            label=col,
                            value=f"{mean_r:.2f}{unit_label}",
                            delta=f"Diff: {diff:+.2f}{unit_label}",
                            delta_color="inverse" if "pitch" in col.lower() or "roll" in col.lower() else "normal"
                        )
                        
            # Visualizing the difference trends
            st.markdown("<h4>TACTICAL INSTRUMENTATION DIFFERENCES (SAMPLE TREND)</h4>", unsafe_allow_html=True)
            chart_df_list = []
            
            # Sampling down to 300 data points for speed and smoothness in visualization rendering
            sample_step = max(1, len(df_rec) // 300)
            df_rec_samp = df_rec.iloc[::sample_step]
            df_base_samp = df_base.iloc[::sample_step] if len(df_base) > 0 else None
            
            fig_compare = go.Figure()
            for col in selected_cols:
                # Recorded trajectory
                fig_compare.add_trace(go.Scatter(
                    x=df_rec_samp['Time_sec'] if 'Time_sec' in df_rec_samp.columns else np.arange(len(df_rec_samp)),
                    y=df_rec_samp[col],
                    mode='lines',
                    line=dict(color='#ff5e00', width=2),
                    name=f"{col} (Recorded)"
                ))
                
                # Baseline trajectory
                if df_base_samp is not None and col in df_base_samp.columns:
                    fig_compare.add_trace(go.Scatter(
                        x=df_base_samp['Time_sec'] if 'Time_sec' in df_base_samp.columns else np.arange(len(df_base_samp)),
                        y=df_base_samp[col],
                        mode='lines',
                        line=dict(color='#00f3ff', width=2, dash='dash'),
                        name=f"{col} (Baseline)"
                    ))
                    
            fig_compare.update_layout(
                paper_bgcolor='#0a0f1d',
                plot_bgcolor='#0d1527',
                legend=dict(font=dict(color='#00f3ff')),
                xaxis=dict(gridcolor='rgba(0,243,255,0.1)', tickfont=dict(color='#00f3ff'), title="Time Sequence / Sec"),
                yaxis=dict(gridcolor='rgba(0,243,255,0.1)', tickfont=dict(color='#00f3ff')),
                margin=dict(l=40, r=40, t=40, b=40)
            )
            st.plotly_chart(fig_compare, use_container_width=True)


# ----------------------------------------------------
# TAB 2: FLIGHT PATH NAVIGATOR
# ----------------------------------------------------
with tab2:
    st.markdown("<h3>FLIGHT TRAJECTORY NAVIGATIONAL COMPUTER</h3>", unsafe_allow_html=True)
    
    col_inp1, col_inp2 = st.columns(2)
    with col_inp1:
        st.markdown("<div class='hud-box'>", unsafe_allow_html=True)
        st.markdown("<h4>DEPARTURE FIX COORDINATES</h4>", unsafe_allow_html=True)
        lat_start = st.number_input("Current Latitude", value=34.0522, format="%.4f")
        lon_start = st.number_input("Current Longitude", value=-118.2437, format="%.4f")
        alt_start = st.number_input("Initial Altitude (m)", value=0.0, format="%.1f")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_inp2:
        st.markdown("<div class='hud-box'>", unsafe_allow_html=True)
        st.markdown("<h4>DESTINATION WAYPOINT</h4>", unsafe_allow_html=True)
        lat_end = st.number_input("Destination Latitude", value=37.7749, format="%.4f")
        lon_end = st.number_input("Destination Longitude", value=-122.4194, format="%.4f")
        target_speed = st.number_input("Target Cruise Velocity (m/s)", value=240.0, format="%.1f")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.sidebar.markdown("### Trajectory Simulation Options")
    anim_speed_opt = st.sidebar.selectbox(
        "Animation Profile Speed",
        options=["Slow Motion", "Normal", "Fast Forward"],
        index=1
    )
    
    # Configure speed intervals
    if anim_speed_opt == "Slow Motion":
        frame_delay = 180
    elif anim_speed_opt == "Normal":
        frame_delay = 60
    else:
        frame_delay = 15
        
    # Trajectory Generation Math Algorithm
    dist_total_km = haversine(lat_start, lon_start, lat_end, lon_end)
    bearing_init = calculate_initial_bearing(lat_start, lon_start, lat_end, lon_end)
    
    # Interpolate waypoint checkpoints
    steps = 45
    lats = np.linspace(lat_start, lat_end, steps)
    lons = np.linspace(lon_start, lon_end, steps)
    
    # Generate flight altitude ceiling curve (climb, cruise, descend)
    cruise_ceiling = 11000.0  # Max altitude 11,000 meters (~36,000 ft)
    climb_phase = int(steps * 0.25)
    descent_phase = int(steps * 0.25)
    cruise_phase = steps - climb_phase - descent_phase
    
    alt_profile = []
    # Climb
    alt_profile.extend(np.linspace(alt_start, cruise_ceiling, climb_phase))
    # Cruise
    alt_profile.extend([cruise_ceiling] * cruise_phase)
    # Descent
    alt_profile.extend(np.linspace(cruise_ceiling, 0.0, descent_phase))
    alt_profile = np.array(alt_profile)
    
    # Construct Navigation Table
    nav_points = []
    running_dist = 0.0
    
    for i in range(steps):
        if i == 0:
            yaw = bearing_init
            pitch = 0.0
            vel = 0.0
        else:
            prev_lat, prev_lon = lats[i-1], lons[i-1]
            curr_lat, curr_lon = lats[i], lons[i]
            
            seg_dist = haversine(prev_lat, prev_lon, curr_lat, curr_lon)
            running_dist += seg_dist
            yaw = calculate_initial_bearing(prev_lat, prev_lon, curr_lat, curr_lon)
            
            # Pitch calculation based on altitude differential relative to current distance
            alt_diff = alt_profile[i] - alt_profile[i-1]
            pitch = np.degrees(np.arctan2(alt_diff, seg_dist * 1000.0))
            
            # Velocity transitions
            if i < climb_phase:
                vel = (i / climb_phase) * target_speed
            elif i >= (climb_phase + cruise_phase):
                rem_steps = steps - i
                vel = (rem_steps / descent_phase) * target_speed
            else:
                vel = target_speed
                
        nav_points.append({
            "Checkpoint": i + 1,
            "Latitude": round(lats[i], 4),
            "Longitude": round(lons[i], 4),
            "Altitude (m)": round(alt_profile[i], 1),
            "Pitch (deg)": round(pitch, 2),
            "Yaw/Heading (deg)": round(yaw, 2),
            "Target Speed (m/s)": round(vel, 1),
            "Total Distance (km)": round(running_dist, 2)
        })
        
    nav_df = pd.DataFrame(nav_points)
    
    st.markdown("<h4>MISSION FLIGHT TRACKING DATA (CALCULATED LOGS)</h4>", unsafe_allow_html=True)
    st.dataframe(nav_df.style.format({
        "Latitude": "{:.4f}",
        "Longitude": "{:.4f}",
        "Altitude (m)": "{:.1f}",
        "Pitch (deg)": "{:+.2f}",
        "Yaw/Heading (deg)": "{:.1f}",
        "Target Speed (m/s)": "{:.1f}",
        "Total Distance (km)": "{:.2f}"
    }))
    
    # --- Spherical 3D Plotly Trajectory Mapping ---
    st.markdown("<h4>3D GLOBE TACTICAL TRAJECTORY ENGINE</h4>", unsafe_allow_html=True)
    st.write("Visualizing simulated Earth sphere relative to departure flight curve.")
    
    R_earth = 6371000.0  # Earth's radius in meters
    
    # Convert trajectory to cartesian space
    xyz_coords = [latlon_to_cartesian(p["Latitude"], p["Longitude"], p["Altitude (m)"], R_earth) for p in nav_points]
    xs = np.array([pt[0] for pt in xyz_coords])
    ys = np.array([pt[1] for pt in xyz_coords])
    zs = np.array([pt[2] for pt in xyz_coords])
    
    # Generate the glowing wireframe globe
    wireframe_traces = make_earth_grid(R_earth)
    
    # Draw static flight line trajectory
    flight_line_trace = go.Scatter3d(
        x=xs, y=ys, z=zs,
        mode='lines',
        line=dict(color='#00f3ff', width=5),
        name='Flight Trajectory Vector'
    )
    
    # Use a solid 'circle' marker to render safely in 3D (avoids previous Scatter3d cone bug)
    live_marker_trace = go.Scatter3d(
        x=[xs[0]], y=[ys[0]], z=[zs[0]],
        mode='markers',
        marker=dict(
            symbol='circle',  # Safe 3D scatter symbol
            size=10,
            color='#ff5e00',
            line=dict(color='#00f3ff', width=2)
        ),
        name='Aero Vehicle Indicator'
    )
    
    # Add a genuine standalone 3D go.Cone trace representing the aircraft directional orientation
    u_init = xs[1] - xs[0] if len(xs) > 1 else 0
    v_init = ys[1] - ys[0] if len(ys) > 1 else 0
    w_init = zs[1] - zs[0] if len(zs) > 1 else 0
    
    live_cone_trace = go.Cone(
        x=[xs[0]], y=[ys[0]], z=[zs[0]],
        u=[u_init], v=[v_init], w=[w_init],
        sizemode="absolute",
        sizeref=100000,  # Explicit structural scale relative to Earth radius
        showscale=False,
        colorscale=[[0, '#ff5e00'], [1, '#ff5e00']],
        name='Vectored Heading'
    )
    
    # Structure Animation Frames
    frames = []
    for i in range(steps):
        if i < steps - 1:
            u = xs[i+1] - xs[i]
            v = ys[i+1] - ys[i]
            w = zs[i+1] - zs[i]
        else:
            u = xs[i] - xs[i-1] if i > 0 else 0
            v = ys[i] - ys[i-1] if i > 0 else 0
            w = zs[i] - zs[i-1] if i > 0 else 0
            
        frame_marker = go.Scatter3d(
            x=[xs[i]], y=[ys[i]], z=[zs[i]],
            mode='markers',
            marker=dict(
                symbol='circle',
                size=10,
                color='#ff5e00',
                line=dict(color='#00f3ff', width=2)
            )
        )
        
        frame_cone = go.Cone(
            x=[xs[i]], y=[ys[i]], z=[zs[i]],
            u=[u], v=[v], w=[w],
            sizemode="absolute",
            sizeref=100000,
            showscale=False,
            colorscale=[[0, '#ff5e00'], [1, '#00f3ff']]
        )
        
        frames.append(go.Frame(
            data=wireframe_traces + [flight_line_trace, frame_marker, frame_cone],
            name=f"frame_{i}"
        ))
        
    # Generate the primary figure object
    fig_3d = go.Figure(
        data=wireframe_traces + [flight_line_trace, live_marker_trace, live_cone_trace],
        layout=go.Layout(
            scene=dict(
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="", backgroundcolor="rgba(0,0,0,0)"),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="", backgroundcolor="rgba(0,0,0,0)"),
                zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title="", backgroundcolor="rgba(0,0,0,0)"),
                aspectmode='data',
                camera=dict(
                    eye=dict(x=1.2, y=1.2, z=1.2)  # Configured camera distance to view complete global arc
                )
            ),
            paper_bgcolor='#0a0f1d',
            margin=dict(r=10, l=10, b=10, t=10),
            legend=dict(font=dict(color='#00f3ff'), y=0.9),
            updatemenus=[dict(
                type="buttons",
                showactive=False,
                direction="left",
                x=0.1, y=0.0,
                xanchor="right", yanchor="top",
                buttons=[
                    dict(
                        label="PLAY SIM",
                        method="animate",
                        args=[None, {
                            "frame": {"duration": frame_delay, "redraw": True},
                            "fromcurrent": True,
                            "transition": {"duration": 0}
                        }]
                    ),
                    dict(
                        label="STOP SIM",
                        method="animate",
                        args=[[None], {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0}
                        }]
                    )
                ]
            )]
        ),
        frames=frames
    )
    
    st.plotly_chart(fig_3d, use_container_width=True)