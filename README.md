**VERY IMPORTANT: This script is a technical proof-of-concept and an educational tool for exploring system automation and input control. This is NOT a cheat. Its methods are detectable, and using it in an online game will almost certainly result in a ban. Do not use it for anything other than analysis.**

### Project Overview

This was a personal project to see how far I could push Python for real-time system automation and input emulation. The goal was to build a full-featured application to manage and simulate recoil control patterns for the game Rust, focusing on sophisticated "humanization" techniques to make the mouse movements appear less robotic.

### Technical Features I Implemented:

*   **Custom GUI:** The entire interface is built with CustomTkinter, featuring a modern, borderless window and animated frame transitions.
*   **Advanced Humanization Engine:**
    *   **Perlin Noise:** Injects smooth, organic jitter into mouse movements to avoid perfectly straight lines.
    *   **Quadratic Easing:** Implements an ease-out function so mouse movements feel more natural, starting fast and slowing down.
    *   **Randomized Timings:** The delay between shots and the initial reaction time are randomized within set boundaries.
    *   **Circular Randomization:** Recoil correction is applied to a random point within a circle around the target pixel, not always to the exact same spot.
*   **Low-Level Input Handling:** Uses `pynput` in separate, non-blocking threads to listen for mouse and keyboard events without freezing the GUI.
*   **String Obfuscation:** Weapon names and other strings are hidden in memory using a simple XOR cipher to explore basic signature scanning evasion techniques.
*   **Configuration Management:** All settings (sensitivity, FOV, DPI, etc.) are saved to and loaded from a `config.json` file.

### How to Run (For Analysis Only)

1.  Make sure you have Python 3 installed.
2.  Install the required libraries:
    ```bash
    pip install customtkinter pynput Pillow perlin-noise-python
    ```
3.  Place the `Brand.png` and `config.json` files in the same directory as the script.
4.  Run the main script from your terminal:
    ```bash
    python 1.py
    ```
