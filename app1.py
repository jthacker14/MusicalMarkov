import streamlit as st
import random
import ast
import collections
import base64
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import streamlit.components.v1 as components
from midiutil import MIDIFile

st.set_page_config(page_title="Musical Markov", layout="wide")

# --- CUSTOM CSS: GLOSSY MULTIVERSE THEME & MONTSERRAT FONT ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap');

/* Apply Montserrat Font */
html, body, [class*="css"], .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
    font-family: 'Montserrat', sans-serif !important;
}

/* Multiverse Deep Space Background */
.stApp {
    background: radial-gradient(circle at 15% 50%, #16002a, #000000 60%, #001233);
    color: #e0e0e0;
}

/* Glossy Glassmorphism Sidebar */
[data-testid="stSidebar"] {
    background: rgba(15, 0, 30, 0.4) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}
/* 1. FIXING THE HEADING (Composition Controls) */
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2 {
    color: white !important;
    -webkit-text-fill-color: white !important;
    background: none !important;
    font-weight: 800 !important;
}

/* 2. FIXING THE LABELS & TEXT */
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] p {
    color: white !important;
    font-weight: 500 !important;
}

/* 3. FIXING THE NUMBER INPUT BUTTONS (+ and -) */
[data-testid="stSidebar"] button[kind="secondary"] {
    color: white !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
}

/* 4. TARGETING THE INPUT BOX TEXT COLOR */
[data-testid="stSidebar"] input {
    color: #16002a !important; /* Keeping the number dark since background is white */
}

/* Main Page Gradient Titles */
h1:not([data-testid="stSidebar"] h1) {
    background: -webkit-linear-gradient(45deg, #00d2ff, #9b51e0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
}

/* Glossy Neon Buttons */
.stButton>button {
    background: linear-gradient(135deg, #ff00cc, #3333ff) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 15px rgba(255, 0, 204, 0.3) !important;
    transition: all 0.3s ease !important;
    font-weight: 600 !important;
    letter-spacing: 1px;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(51, 51, 255, 0.6) !important;
}

/* Gradient Titles */
h1 {
    background: -webkit-linear-gradient(45deg, #00d2ff, #9b51e0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
}

/* Inputs / Selectboxes (Glassy) */
.stSelectbox div[data-baseweb="select"], .stMultiSelect div[data-baseweb="select"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    color: white !important;
}

/* Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    background-color: transparent;
}
.stTabs [aria-selected="true"] {
    color: #ff00cc !important;
    border-bottom: 2px solid #ff00cc !important;
}

/* Dataframe Styling */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
# -----------------------------------------------------------

st.title("**Musical Markov: let the algorithm compose your next beat!**")
st.markdown("**Music generation by using markov chain**")

# --- 1. DATA CORPORA (11 Genres) ---
GENRES = {
    "Afrobeats": {
        "chords": {"F_Minor_7": ["E_Flat_Major", "D_Flat_Major"], "E_Flat_Major": ["D_Flat_Major", "F_Minor_7"], "D_Flat_Major": ["C_Minor_7", "F_Minor_7"], "C_Minor_7": ["F_Minor_7"]},
        "notes": {"F_Minor_7": [53, 56, 60, 63], "E_Flat_Major": [51, 55, 58, 63], "D_Flat_Major": [49, 53, 56, 60], "C_Minor_7": [48, 51, 55, 58]},
        "rhythm": {str([0.75, 0.25]): [0.5, 0.5], str([0.5, 0.5]): [0.25, 0.75], str([0.25, 0.75]): [0.75, 0.25]},
        "velocity": {"85": [60, 40], "60": [85], "40": [60, 85]}
    },
    "UK Drill": {
        "chords": {"D_Minor": ["A_Minor", "A_Sharp_Major"], "A_Minor": ["D_Minor"], "A_Sharp_Major": ["A_Minor"]},
        "notes": {"D_Minor": [50, 53, 57], "A_Minor": [45, 48, 52], "A_Sharp_Major": [46, 50, 53]},
        "rhythm": {str([0.5, 0.25]): [0.25, 0.75], str([0.25, 0.75]): [0.25, 0.5], str([0.25, 0.25]): [0.5]},
        "velocity": {"127": [85, 60], "85": [127], "60": [127, 85]}
    },
    "Neo-Soul": {
        "chords": {"E_Minor_9": ["A_13"], "A_13": ["D_Major_9"], "D_Major_9": ["B_7_alt"], "B_7_alt": ["E_Minor_9"]},
        "notes": {"E_Minor_9": [52, 59, 62, 66], "A_13": [45, 55, 61, 66], "D_Major_9": [50, 57, 61, 64], "B_7_alt": [47, 51, 58, 61]},
        "rhythm": {str([1.0, 0.5]): [0.5, 0.25], str([0.5, 0.25]): [0.75], str([0.75, 0.5]): [0.5]},
        "velocity": {"85": [60, 40], "60": [85], "40": [60, 85]}
    },
    "Lofi Jazz": {
        "chords": {"D_Minor_7": ["G_7", "C_Major_7"], "G_7": ["C_Major_7"], "C_Major_7": ["A_Minor_7"], "A_Minor_7": ["D_Minor_7"]},
        "notes": {"D_Minor_7": [50, 53, 57, 60], "G_7": [43, 47, 50, 53], "C_Major_7": [48, 52, 55, 59], "A_Minor_7": [45, 48, 52, 55]},
        "rhythm": {str([1.0, 1.0]): [0.5, 1.0], str([1.0, 0.5]): [0.5, 1.0], str([0.5, 0.5]): [1.0, 0.5]},
        "velocity": {"60": [60, 85], "85": [60, 40], "40": [60]}
    },
    "Cinematic Orchestral": {
        "chords": {"C_Minor": ["A_Sharp_Major", "G_Sharp_Major"], "G_Sharp_Major": ["F_Minor"], "A_Sharp_Major": ["C_Minor"], "F_Minor": ["C_Minor"]},
        "notes": {"C_Minor": [36, 43, 60], "G_Sharp_Major": [32, 39, 56], "A_Sharp_Major": [34, 41, 58], "F_Minor": [41, 48, 65]},
        "rhythm": {str([2.0, 2.0]): [4.0, 2.0], str([4.0, 2.0]): [2.0], str([2.0, 4.0]): [2.0]},
        "velocity": {"60": [60, 85], "85": [85, 110], "110": [127, 85], "127": [110]}
    },
    "Synthwave (80s Pop)": {
        "chords": {"A_Minor": ["F_Major", "G_Major"], "F_Major": ["D_Minor", "G_Major"], "G_Major": ["A_Minor"], "D_Minor": ["A_Minor"]},
        "notes": {"A_Minor": [45, 48, 52], "F_Major": [41, 45, 48], "G_Major": [43, 47, 50], "D_Minor": [50, 53, 57]},
        "rhythm": {str([0.25, 0.25]): [0.25, 0.5], str([0.25, 0.5]): [0.25], str([0.5, 0.25]): [0.25]},
        "velocity": {"110": [110], "127": [110]}
    },
    "EDM / House": {
        "chords": {"E_Minor": ["C_Major", "D_Major"], "C_Major": ["D_Major"], "D_Major": ["E_Minor"]},
        "notes": {"E_Minor": [52, 55, 59], "C_Major": [48, 52, 55], "D_Major": [50, 54, 57]},
        "rhythm": {str([0.25, 0.25]): [0.25], str([0.5, 0.25]): [0.25]},
        "velocity": {"127": [110, 127], "110": [127]}
    }
}

# --- 2. INSTRUMENTS & BEATS DICTIONARIES ---
# FIXED: Removed trailing spaces from keys
INSTRUMENTS = {
    "Acoustic Grand Piano": 0, "Piano": 1,
    "Marimba": 12, "Harmonium": 20, 
    "Acoustic Guitar": 24, "Electric Guitar": 27,
    "Acoustic Bass": 32, "Slap Bass": 36, "Synth Bass": 38,
    "Violin": 40, "String Ensemble": 48, "Choir Aahs": 52, "Brass Section": 61,
    "Soprano Saxophone": 64, "Flute": 73,
    "Synth Lead": 80, "Synth Pad": 88, 
    "Sitar": 104, "Kalimba": 108, "Shanai": 111
}

BEATS = {
    "None": [],
    "Afrobeats": [
        (36, 0.0), (42, 0.25), (42, 0.5), (37, 0.75),
        (42, 1.0), (42, 1.25), (36, 1.5), (37, 1.75),
        (36, 2.0), (42, 2.25), (42, 2.5), (37, 2.75),
        (42, 3.0), (42, 3.25), (36, 3.5), (37, 3.75)
    ],
    "Trap / DHH": [
        (36, 0.0), (42, 0.0), (42, 0.5), (38, 1.0), (42, 1.0), (42, 1.5),
        (36, 2.0), (42, 2.0), (36, 2.5), (42, 2.5), (38, 3.0), (42, 3.0), (42, 3.5)
    ],
    "Boom Bap": [
        (36, 0.0), (42, 0.0), (42, 0.5), (38, 1.0), (42, 1.0), (42, 1.5),
        (36, 2.5), (42, 2.0), (42, 2.5), (38, 3.0), (42, 3.0), (42, 3.5)
    ],
    "EDM / House": [
        (36, 0.0), (42, 0.5), (36, 1.0), (39, 1.0), (46, 1.5),
        (36, 2.0), (42, 2.5), (36, 3.0), (39, 3.0), (46, 3.5)
    ],
    "Tabla": [
        (64, 0.0), (60, 0.5), (64, 1.0), (60, 1.5),
        (64, 2.0), (60, 2.5), (63, 3.0), (60, 3.5)
    ]
}

# --- 3. CORE LOGIC FUNCTIONS ---
def apply_temperature(transitions, temp):
    """Applies entropy (randomness) to a transition probability matrix."""
    counts = collections.Counter(transitions)
    states = list(counts.keys())
    freqs = np.array(list(counts.values()))
    if temp == 0: return states[np.argmax(freqs)]
    probs = freqs ** (1.0 / temp)
    probs = probs / np.sum(probs)
    return np.random.choice(states, p=probs)

def setup_midi_environment(chord_insts, melody_insts, tempo):
    """Calculates track allocations and configures the MIDI object cleanly."""
    total_tracks = len(chord_insts) + len(melody_insts) + 1 # +1 for drums
    midi = MIDIFile(total_tracks)
    
    for i in range(total_tracks):
        midi.addTempo(i, 0, tempo)
        
    available_channels = [ch for ch in range(16) if ch != 9] # Reserve 9 for drums
    channel_idx = 0
    track_mapping = {'chords': [], 'melody': [], 'drums': (total_tracks - 1, 9)}
    
    # Map Chords
    for i, inst_name in enumerate(chord_insts):
        channel = available_channels[channel_idx % len(available_channels)]
        midi.addProgramChange(i, channel, 0, INSTRUMENTS[inst_name])
        track_mapping['chords'].append((i, channel))
        channel_idx += 1
        
    # Map Melody
    for i, inst_name in enumerate(melody_insts):
        track_num = len(chord_insts) + i
        channel = available_channels[channel_idx % len(available_channels)]
        midi.addProgramChange(track_num, channel, 0, INSTRUMENTS[inst_name])
        track_mapping['melody'].append((track_num, channel))
        channel_idx += 1

    return midi, track_mapping

def generate_musical_sequence(midi, track_mapping, corpus, beat_pattern, num_bars, randomness, chord_octave, melody_octave):
    """Executes the hierarchical Markov chain to compose the track."""
    current_chord = list(corpus["chords"].keys())[0]
    current_rhythm = list(ast.literal_eval(list(corpus["rhythm"].keys())[0]))
    current_velocity = list(corpus["velocity"].keys())[0]
    
    absolute_time = 0.0
    chord_log, melody_log = [], []

    for bar in range(num_bars):
        # 1. Macro-Chain: Determine Harmony
        next_chord = apply_temperature(corpus["chords"][current_chord], randomness)
        chord_log.append({"From": current_chord, "To": next_chord, "Time": absolute_time})
        current_chord = next_chord
        
        active_pitches = [p + (chord_octave * 12) for p in corpus["notes"][current_chord]]
        for pitch in active_pitches:
            for track, channel in track_mapping['chords']:
                midi.addNote(track, channel, pitch, absolute_time, 4.0, 75)

        # 2. Micro-Chain: Determine Melody
        bar_time = 0.0
        while bar_time < 4.0:
            r_str = str(current_rhythm)
            next_dur = apply_temperature(corpus["rhythm"][r_str], randomness) if r_str in corpus["rhythm"] else 0.5
            if bar_time + next_dur > 4.0: next_dur = 4.0 - bar_time
            
            next_vel = int(apply_temperature(corpus["velocity"][current_velocity], randomness)) if current_velocity in corpus["velocity"] else 85
            
            melody_pitch = random.choice(active_pitches) + (melody_octave * 12)
            
            for track, channel in track_mapping['melody']:
                midi.addNote(track, channel, melody_pitch, absolute_time + bar_time, next_dur, next_vel)
                
            melody_log.append({"Pitch": melody_pitch, "Duration": next_dur, "Time": absolute_time + bar_time})
            
            current_rhythm = [current_rhythm[1], next_dur]
            current_velocity = str(next_vel)
            bar_time += next_dur
            
        # 3. Static Pattern: Percussion
        for drum_pitch, hit_time_offset in beat_pattern:
            track, channel = track_mapping['drums']
            midi.addNote(track, channel, drum_pitch, absolute_time + hit_time_offset, 0.25, 100)
            
        absolute_time += 4.0
        
    return midi, chord_log, melody_log

# FIXED: Cleaned up the downloaded file name
def create_download_link(file_path):
    with open(file_path, "rb") as f: data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<br><a href="data:audio/midi;base64,{b64}" download="masterpiece.mid" style="background:#ff00cc;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;font-weight:bold;">⬇️ Download Full Multi-Track MIDI</a><br><br>'

# --- 4. SIDEBAR UI ---
st.sidebar.header("Composition Controls")
selected_genre = st.sidebar.selectbox("Genre Algorithm", list(GENRES.keys()))
selected_beat = st.sidebar.selectbox("Drum Beat Style", list(BEATS.keys()))
num_bars = st.sidebar.number_input("Duration (Bars)", min_value=4, max_value=64, value=8, step=4)
tempo = st.sidebar.slider("Pace (Tempo BPM)", 60, 180, 100)
randomness = st.sidebar.slider("Randomness (Entropy)", 0.1, 2.0, 1.0, 0.1)

st.sidebar.markdown("---")
st.sidebar.markdown("**Track 1: Harmony (Chords)**")
# FIXED: Changed default value to match keys actually present in the INSTRUMENTS dictionary
chord_insts = st.sidebar.multiselect("Harmony Instruments", list(INSTRUMENTS.keys()), default=["Piano", "Marimba"])
chord_octave = st.sidebar.slider("Chord Octave Shift", -2, 2, 0)

st.sidebar.markdown("**Track 2: Melody (Lead)**")
melody_insts = st.sidebar.multiselect("Melody Instruments", list(INSTRUMENTS.keys()), default=["Kalimba", "Soprano Saxophone"])
melody_octave = st.sidebar.slider("Melody Octave Shift", -1, 3, 1)

generate_btn = st.sidebar.button("GENERATE TRACK", type="primary", use_container_width=True)

# --- TABS SETUP ---
tab1, tab2 = st.tabs(["Web Studio Player", "Stochastic Analytics"])

if "chord_log" not in st.session_state: st.session_state.chord_log = []
if "melody_log" not in st.session_state: st.session_state.melody_log = []
if "out_file" not in st.session_state: st.session_state.out_file = None

# --- 5. MAIN EXECUTION ---
if generate_btn:
    if not chord_insts or not melody_insts:
        st.error("Please select at least one Harmony and one Melody instrument!")
    else:
        with st.spinner('Calculating Matrices & Layering Instruments...'):
            corpus = GENRES[selected_genre]
            beat_pattern = BEATS[selected_beat]
            
            # Use modularized functions
            midi, track_map = setup_midi_environment(chord_insts, melody_insts, tempo)
            midi, chord_log, melody_log = generate_musical_sequence(
                midi, track_map, corpus, beat_pattern, num_bars, randomness, chord_octave, melody_octave
            )

            # Save Output Data
            # FIXED: Cleaned up the file name
            st.session_state.out_file = "masterpiece.mid"
            with open(st.session_state.out_file, "wb") as f: 
                midi.writeFile(f)
            st.session_state.chord_log = chord_log
            st.session_state.melody_log = melody_log

# --- 6. TAB 1: COMPOSER TAB ---
with tab1:
    st.subheader("Piano Roll & Playback")
    
    if st.session_state.out_file:
        st.success("Track generated! ⚠️ **WAIT 5 SECONDS before pressing play** to allow your browser to download the virtual instrument sounds.")
        st.markdown(create_download_link(st.session_state.out_file), unsafe_allow_html=True)
        
        with open(st.session_state.out_file, "rb") as f:
            b64_midi = base64.b64encode(f.read()).decode()
            
        player_id = random.randint(10000, 99999)
            
        midi_player_html = f"""
        <script src="https://cdn.jsdelivr.net/combine/npm/tone@14.7.58,npm/@magenta/music@1.23.1/es6/core.js,npm/focus-visible@5,npm/html-midi-player@1.5.0"></script>
        <midi-player id="midi-player-{player_id}" src="data:audio/midi;base64,{b64_midi}" sound-font="https://storage.googleapis.com/magentadata/js/soundfonts/sgm_plus" visualizer="#viz-{player_id}"></midi-player>
        <midi-visualizer type="piano-roll" id="viz-{player_id}"></midi-visualizer>
        <style>
          midi-player {{ display: block; margin-bottom: 20px; width: 100%; }}
          midi-visualizer {{ background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 10px; height: 300px; display: block; }}
        </style>
        """
        components.html(midi_player_html, height=450)
    else:
        st.info("Adjust your parameters on the left and click 'GENERATE TRACK'.")

# --- 7. TAB 2: TECHNICAL TAB (Analytics) ---
with tab2:
    st.subheader("Stochastic Process Analytics")
    
    if st.session_state.chord_log:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Melody Pitch TPM (Heatmap)")
            df_mel = pd.DataFrame(st.session_state.melody_log)
            df_mel["Next Pitch"] = df_mel["Pitch"].shift(-1)
            df_mel = df_mel.dropna()
            
            tpm_counts = pd.crosstab(df_mel['Pitch'], df_mel['Next Pitch'])
            
            # Adjusted for dark theme
            fig_heat = px.imshow(tpm_counts, labels=dict(x="To Pitch", y="From Pitch", color="Freq"), color_continuous_scale="Purpor", template="plotly_dark")
            fig_heat.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_heat, use_container_width=True)
            
        with col2:
            st.markdown("### Chord Progression (Adjacency Graph)")
            G = nx.DiGraph()
            for row in st.session_state.chord_log: G.add_edge(row["From"], row["To"])
                
            pos = nx.spring_layout(G)
            edge_x, edge_y = [], []
            for edge in G.edges():
                x0, y0 = pos[edge[0]][0], pos[edge[0]][1]
                x1, y1 = pos[edge[1]][0], pos[edge[1]][1]
                edge_x.extend([x0, x1, None]); edge_y.extend([y0, y1, None])

            # Adjusted line color for dark theme
            edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1.5, color='rgba(255, 255, 255, 0.4)'), hoverinfo='none', mode='lines')
            
            node_x, node_y, node_text = [], [], []
            for node in G.nodes():
                x, y = pos[node][0], pos[node][1]
                node_x.append(x); node_y.append(y); node_text.append(node)

            # Vibrant node colors
            node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text', text=node_text, textposition="top center",
                                    marker=dict(size=40, color='#00d2ff', line_width=2, line_color="#ff00cc"), textfont=dict(color="white"))

            fig_graph = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False, hovermode='closest', margin=dict(b=0,l=0,r=0,t=0),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
            st.plotly_chart(fig_graph, use_container_width=True)

        st.markdown("---")
        st.markdown("### Markov Chain Transition Probability Matrix (Chords)")
        
        df_chords = pd.DataFrame(st.session_state.chord_log)
        if not df_chords.empty and len(df_chords) > 1:
            tpm_chords = pd.crosstab(df_chords['From'], df_chords['To'], normalize='index')
            st.dataframe(
                tpm_chords.style.format("{:.1%}") \
                                .background_gradient(cmap='Purples', axis=1),
                use_container_width=True
            )
            st.caption("*How to read this:* Look at the row for your current chord. The percentages show the Markov probability of the engine picking the next chord in the columns.")