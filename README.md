<div align="center">

# 🐍 Python Input Automation & Humanization Demo 🐍

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/CustomTkinter-3A7ABF?style=for-the-badge" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/Input_Control-pynput-A62E2E?style=for-the-badge" alt="pynput">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT">
</p>

A technical proof-of-concept exploring real-time system automation, low-level input control, and advanced "humanization" techniques using Python.

</div>

---

<div align="center">

## 🚨 **VERY IMPORTANT DISCLAIMER** 🚨

**This script is a technical proof-of-concept and an educational tool for exploring system automation and input control. This is NOT a cheat.**

Its methods are detectable, and using it in an online game will almost certainly result in a ban. It should be used for analysis and educational purposes only. **Do not use it for anything other than its intended purpose of analysis.**

</div>

---

<details>
  <summary><strong>Table of Contents</strong></summary>
  <ol>
    <li><a href="#-about-the-project">About The Project</a></li>
    <li><a href="#-technical-features">Technical Features</a></li>
    <li><a href="#-tech-stack">Tech Stack</a></li>
    <li><a href="#-how-to-run-for-analysis-only">How to Run (For Analysis Only)</a></li>
    <li><a href="#-license">License</a></li>
  </ol>
</details>

---

## 📖 About The Project

This was a personal project to see how far I could push Python for real-time system automation and input emulation. The goal was to build a full-featured application to manage and simulate recoil control patterns, focusing on sophisticated "humanization" techniques to make the simulated mouse movements appear less robotic and more organic.

---

## ✨ Technical Features

*   **Custom GUI:** The entire interface is built with CustomTkinter, featuring a modern, borderless window and animated frame transitions.
*   **Advanced Humanization Engine:**
    *   **Perlin Noise:** Injects smooth, organic jitter into mouse movements to avoid perfectly straight lines.
    *   **Quadratic Easing:** Implements an ease-out function so mouse movements feel more natural, starting fast and slowing down.
    *   **Randomized Timings:** The delay between actions and the initial reaction time are randomized within set boundaries.
    *   **Circular Randomization:** Corrections are applied to a random point within a circle around the target pixel, not always to the exact same spot.
*   **Low-Level Input Handling:** Uses `pynput` in separate, non-blocking threads to listen for mouse and keyboard events without freezing the GUI.
*   **String Obfuscation:** Weapon names and other strings are hidden in memory using a simple XOR cipher to explore basic signature scanning evasion techniques.
*   **Configuration Management:** All settings (sensitivity, FOV, DPI, etc.) are saved to and loaded from a `config.json` file.

---

## 🛠️ Tech Stack

*   **Core**: Python 3
*   **GUI**: CustomTkinter
*   **Input Handling**: pynput
*   **Image Handling**: Pillow
*   **Humanization**: perlin-noise-python

---

## 🚀 How to Run (For Analysis Only)

1.  **Prerequisites**: Make sure you have Python 3 installed.
2.  **Install the required libraries**:
    ```sh
    pip install customtkinter pynput Pillow perlin-noise-python
    ```
3.  **Place Required Files**: Ensure the `Brand.png` and `config.json` files are in the same directory as the script.
4.  **Run the main script from your terminal**:
    ```sh
    python 1.py
    ```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
