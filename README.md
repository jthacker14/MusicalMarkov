# The Multiverse Algorithmic Studio

## Overview
The Multiverse Algorithmic Studio is an interactive, web-based application that explores the intersection of probability theory and the creative arts. By bridging mathematics and music via a Hierarchical Markov Engine, the application composes multi-track MIDI music in real-time. It solves the historical struggle of algorithmic composition by operating in the optimal zone of "guided randomness," avoiding both purely chaotic noise and rigidly mechanical sequences.

## Core Architecture
The system eschews black-box deep learning models in favor of mathematically transparent stochastic processes. 

### 1. Hierarchical Markov Engine
To prevent structural myopia, the generative workload is divided into independent stochastic processes:
*   **The Macro-Chain (Harmonic Structure):** Executes once per musical bar to determine the overarching chord progression. It acts as a boundary constraint, mathematically dictating the exact pool of active pitches permitted during that measure.
*   **The Micro-Chain (Melody and Dynamics):** Operates at a high frequency within the established bar to generate primary lead melodies, rhythm, and MIDI velocity. 

### 2. Thermodynamic Interpolation (Temperature)
The application utilizes the concept of Temperature from statistical mechanics to control the informational entropy of the generated output. By applying softmax temperature scaling to the transition probabilities:
*   **Low Temperature ($0 < T < 1$):** Amplifies the highest raw frequencies, producing conservative, deterministic, and highly predictable musical sequences.
*   **Standard Temperature ($T = 1.0$):** Samples directly from the raw empirical distribution of the training corpus.
*   **High Temperature ($T > 1.0$):** Flattens the probability distribution, injecting massive entropy to generate unpredictable, avant-garde improvisational choices.

### 3. Mathematical Foundations
The engine leverages Discrete-Time Markov Chains (DTMC). Adhering to the Markov property (memorylessness), the conditional probability of transitioning to a future state depends exclusively on the current state:

$$P(X_{n+1} = x \mid X_1 = x_1, X_2 = x_2, \dots, X_n = x_n) = P(X_{n+1} = x \mid X_n = x_n)$$

The probabilistic rules are encoded in right-stochastic Transition Probability Matrices (TPMs), utilizing distinct multidimensional state spaces for harmony, rhythm, and dynamic velocity.

## Supported Genres
The system features highly specialized, hard-coded data corpora capable of generating music across 11 distinct genres, including:
*   **Afrobeats:** Features polyrhythmic percussion and the "Tresillo" bounce.
*   **Neo-Soul:** Utilizes complex jazz ii-V-I cadences, extended voicings, and soft dynamic phrasing.
*   **UK Drill:** Generates cinematic dread through minor chords and aggressive, rapid staccato melodies.
*   **Lofi Jazz:** Employs resolving jazz progressions with constrained rhythmic densities to maintain an ambient aesthetic.

## Interactive Visual Analytics
Beyond music generation, the application serves as a transparent pedagogical tool using the Streamlit framework:
*   **Transition Probability Matrices:** Real-time dataframes proving the thermodynamic entropy manipulation occurring in the backend.
*   **Adjacency Graphs:** Network topology graphs rendered via NetworkX and Plotly that map the temporal transitions of the overarching harmonic macro-structure.
*   **Pitch Heatmaps:** Visualizes the frequency of melodic interval transitions to instantly analyze the melodic contour.

## Audio Rendering
The software utilizes the `MIDIUtil` Python library to construct multi-track MIDI files natively. The frontend integrates in-browser playback using Magenta.js, Tone.js, and html-midi-player components for real-time synthesis and visual piano roll tracking without requiring an external DAW.

## Documentation
For an in-depth exploration of the mathematics, algorithms, and musicology powering this engine, please refer to the included document: `Copy of Algorithmic Music Studio Report.docx`.
