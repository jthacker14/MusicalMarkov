# The Multiverse Algorithmic Studio

## Overview
The Multiverse Algorithmic Studio is an interactive, web-based application that explores the intersection of probability theory and the creative arts.[cite: 1] By bridging mathematics and music via a Hierarchical Markov Engine, the application composes multi-track MIDI music in real-time.[cite: 1] It solves the historical struggle of algorithmic composition by operating in the optimal zone of "guided randomness," avoiding both purely chaotic noise and rigidly mechanical sequences.[cite: 1]

## Core Architecture
The system eschews black-box deep learning models in favor of mathematically transparent stochastic processes.[cite: 1] 

### 1. Hierarchical Markov Engine
To prevent structural myopia, the generative workload is divided into independent stochastic processes:[cite: 1]
*   **The Macro-Chain (Harmonic Structure):** Executes once per musical bar to determine the overarching chord progression.[cite: 1] It acts as a boundary constraint, mathematically dictating the exact pool of active pitches permitted during that measure.[cite: 1]
*   **The Micro-Chain (Melody and Dynamics):** Operates at a high frequency within the established bar to generate primary lead melodies, rhythm, and MIDI velocity.[cite: 1] 

### 2. Thermodynamic Interpolation (Temperature)
The application utilizes the concept of Temperature from statistical mechanics to control the informational entropy of the generated output.[cite: 1] By applying softmax temperature scaling to the transition probabilities:[cite: 1]
*   **Low Temperature ($0 < T < 1$):** Amplifies the highest raw frequencies, producing conservative, deterministic, and highly predictable musical sequences.[cite: 1]
*   **Standard Temperature ($T = 1.0$):** Samples directly from the raw empirical distribution of the training corpus.[cite: 1]
*   **High Temperature ($T > 1.0$):** Flattens the probability distribution, injecting massive entropy to generate unpredictable, avant-garde improvisational choices.[cite: 1]

### 3. Mathematical Foundations
The engine leverages Discrete-Time Markov Chains (DTMC).[cite: 1] Adhering to the Markov property (memorylessness), the conditional probability of transitioning to a future state depends exclusively on the current state:[cite: 1]

$$P(X_{n+1} = x \mid X_1 = x_1, X_2 = x_2, \dots, X_n = x_n) = P(X_{n+1} = x \mid X_n = x_n)$$[cite: 1]

The probabilistic rules are encoded in right-stochastic Transition Probability Matrices (TPMs), utilizing distinct multidimensional state spaces for harmony, rhythm, and dynamic velocity.[cite: 1]

## Supported Genres
The system features highly specialized, hard-coded data corpora capable of generating music across 11 distinct genres, including:[cite: 1]
*   **Afrobeats:** Features polyrhythmic percussion and the "Tresillo" bounce.[cite: 1]
*   **Neo-Soul:** Utilizes complex jazz ii-V-I cadences, extended voicings, and soft dynamic phrasing.[cite: 1]
*   **UK Drill:** Generates cinematic dread through minor chords and aggressive, rapid staccato melodies.[cite: 1]
*   **Lofi Jazz:** Employs resolving jazz progressions with constrained rhythmic densities to maintain an ambient aesthetic.[cite: 1]

## Interactive Visual Analytics
Beyond music generation, the application serves as a transparent pedagogical tool using the Streamlit framework:[cite: 1]
*   **Transition Probability Matrices:** Real-time dataframes proving the thermodynamic entropy manipulation occurring in the backend.[cite: 1]
*   **Adjacency Graphs:** Network topology graphs rendered via NetworkX and Plotly that map the temporal transitions of the overarching harmonic macro-structure.[cite: 1]
*   **Pitch Heatmaps:** Visualizes the frequency of melodic interval transitions to instantly analyze the melodic contour.[cite: 1]

## Audio Rendering
The software utilizes the `MIDIUtil` Python library to construct multi-track MIDI files natively.[cite: 1] The frontend integrates in-browser playback using Magenta.js, Tone.js, and html-midi-player components for real-time synthesis and visual piano roll tracking without requiring an external DAW.[cite: 1]

## Documentation
For an in-depth exploration of the mathematics, algorithms, and musicology powering this engine, please refer to the included document: `Copy of Algorithmic Music Studio Report.docx`.