# --- IMPORTS ---
import time
import threading
import customtkinter as ctk
from pynput import mouse, keyboard
from PIL import Image
import os
import sys
import json
import math
import random
import ctypes

# For advanced humanization (Perlin noise is still used for smooth movement jitter)
from perlin_noise import PerlinNoise

# --- TIER 1: OBFUSCATION ---
def xor_cipher(s, key):
    """Simple XOR cipher for hiding strings in memory to evade signature scanning."""
    return "".join(chr(ord(c) ^ ord(k)) for c, k in zip(s, key * (len(s) // len(key) + 1)))

CIPHER_KEY = "kH8sJk3mNfP2qR5s" 

E_ASSAULT_RIFLE = xor_cipher("Assault Rifle", CIPHER_KEY)
E_MP5A4 = xor_cipher("MP5A4", CIPHER_KEY)
E_CUSTOM_SMG = xor_cipher("Custom SMG", CIPHER_KEY)
E_LR300 = xor_cipher("LR300", CIPHER_KEY)
E_THOMPSON = xor_cipher("Thompson", CIPHER_KEY)
E_HMLMG = xor_cipher("HMLMG", CIPHER_KEY)
E_M249 = xor_cipher("M249", CIPHER_KEY)
E_SAR = xor_cipher("Semi Automatic Rifle", CIPHER_KEY)
E_REVOLVER = xor_cipher("Revolver", CIPHER_KEY)
E_SAP = xor_cipher("Semi Automatic Pistol", CIPHER_KEY)
E_M92 = xor_cipher("M92", CIPHER_KEY)
E_M39 = xor_cipher("M39", CIPHER_KEY)
E_PYTHON = xor_cipher("Python", CIPHER_KEY)
E_NAILGUN = xor_cipher("Nail Gun", CIPHER_KEY)

# --- BRAND COLORS & APPEARANCE ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
WINDOW_BG_COLOR = "#1B1B1B"
FRAME_BG_COLOR = "#242424"
SIDEBAR_COLOR = "#212121"
BUTTON_COLOR = "#333333"
BUTTON_HOVER_COLOR = "#474747"
TEXT_COLOR = "#F0F0F0"
SUBTEXT_COLOR = "#A0A0A0"
ACCENT_GREEN = "#2E7D32"
ACCENT_RED = "#B71C1C"

# --- FULL WEAPON DATA (FROM PROVIDED SOURCE) ---
WEAPONS = {
    E_ASSAULT_RIFLE: {"pattern": [(0.000000,-2.257792),(0.323242,-2.300758),(0.649593,-2.299759),(0.848786,-2.259034),(1.075408,-2.323947),(1.268491,-2.215956),(1.330963,-2.236556),(1.336833,-2.218203),(1.505516,-2.143454),(1.504423,-2.233091),(1.442116,-2.270194),(1.478543,-2.204318),(1.392874,-2.165817),(1.480824,-2.177887),(1.597069,-2.270915),(1.449996,-2.145893),(1.369179,-2.270450),(1.582363,-2.298334),(1.516872,-2.235066),(1.498249,-2.238401),(1.465769,-2.331642),(1.564812,-2.242621),(1.517519,-2.235066),(1.422433,-2.211946),(1.553195,-2.248043),(1.510463,-2.285327),(1.553878,-2.240047),(1.520380,-2.221839),(1.553878,-2.240047),(1.553195,-2.248043)], "delay": 133.3 / 1000.0},
    E_MP5A4: {"pattern": [(0.125361,-1.052446),(-0.099548,-0.931548),(0.027825,-0.954094),(-0.013715,-0.851504),(-0.007947,-1.070579),(0.096096,-1.018017),(-0.045937,-0.794216),(0.034316,-1.112618),(-0.003968,-0.930040),(-0.009403,-0.888503),(0.140813,-0.970807),(-0.015052,-1.046551),(0.095699,-0.860475),(-0.269643,-1.038896),(0.000285,-0.840478),(0.018413,-1.038126),(0.099191,-0.851701),(0.199659,-0.893041),(-0.082660,-1.069278),(0.006826,-0.881493),(0.091709,-1.150956),(-0.108677,-0.965513),(0.169612,-1.099499),(-0.038244,-1.120084),(-0.085513,-0.876956),(0.136279,-1.047589),(0.196392,-1.039977),(-0.152513,-1.209291),(-0.214510,-0.956648),(0.034276,-0.095177)], "delay": 100.0 / 1000.0},
    E_CUSTOM_SMG: {"pattern": [(-0.114414,-0.680635),(0.008685,-0.676597),(0.010312,-0.682837),(0.064825,-0.691344),(0.104075,-0.655617),(-0.088118,-0.660429),(0.089906,-0.675183),(0.037071,-0.632623),(0.178466,-0.634737),(0.034653,-0.669444),(-0.082658,-0.664827),(0.025551,-0.636631),(0.082413,-0.647118),(-0.123305,-0.662104),(0.028164,-0.662354),(-0.117346,-0.693475),(-0.268777,-0.661123),(-0.053086,-0.677493),(0.004238,-0.647037),(0.014169,-0.551440),(-0.009907,-0.552079),(0.044076,-0.577694),(-0.043187,-0.549581)], "delay": 90.0 / 1000.0},
    E_LR300: {"pattern": [(0.000000,-2.052616),(0.055584,-1.897695),(-0.247226,-1.863222),(-0.243871,-1.940010),(0.095727,-1.966751),(0.107707,-1.885520),(0.324888,-1.946722),(-0.181137,-1.880342),(0.162399,-1.820107),(-0.292076,-1.994940),(0.064575,-1.837156),(-0.126699,-1.887880),(-0.090568,-1.832799),(0.065338,-1.807480),(-0.197343,-1.705888),(-0.216561,-1.785949),(0.042567,-1.806371),(-0.065534,-1.757623),(0.086380,-1.904010),(-0.097326,-1.969296),(-0.213034,-1.850288),(-0.017790,-1.730867),(-0.045577,-1.783686),(-0.053309,-1.886260),(0.055072,-1.793076),(-0.091874,-1.921906),(-0.033719,-1.796160),(0.266464,-1.993952),(0.079090,-1.921165)], "delay": 120.0 / 1000.0},
    E_THOMPSON: {"pattern": [(-0.114413,-0.680635),(0.008686,-0.676598),(0.010312,-0.682837),(0.064825,-0.691345),(0.104075,-0.655618),(-0.088118,-0.660429),(0.089906,-0.675183),(0.037071,-0.632623),(0.178465,-0.634737),(0.034654,-0.669443),(-0.082658,-0.664826),(0.025550,-0.636631),(0.082414,-0.647118),(-0.123305,-0.662104),(0.028164,-0.662354),(-0.117346,-0.693475),(-0.268777,-0.661123),(-0.053086,-0.677493),(0.04238,-0.647038), (0.04238,-0.647038)], "delay": 90.0 / 1000.0},
    E_HMLMG: {"pattern": [(0,-1.4),(-0.39,-1.4),(-0.73,-1.4)]+ [(-0.73, -1.4)] * 57, "delay": 100.0 / 1000.0},
    E_M249: {"pattern": [(0,-1.49),(0.39,-1.49),(0.72,-1.49)]+ [(0.72, -1.49)] * 54 + [(0.0, -1.49)] * 43, "delay": 100.0 / 1000.0},
    E_SAR: {"pattern": [(0,-1.4)], "delay": 175.0 / 1000.0},
    E_REVOLVER: {"pattern": [(0,-1.7)], "delay": 175.0 / 1000.0},
    E_SAP: {"pattern": [(0,-0.95)], "delay": 150.0 / 1000.0},
    E_M92: {"pattern": [(0,-3)], "delay": 150.0 / 1000.0},
    E_M39: {"pattern": [(0.9,-1.6)], "delay": 175.0 / 1000.0},
    E_PYTHON: {"pattern": [(0,-5.8)], "delay": 150.0 / 1000.0},
    E_NAILGUN: {"pattern": [(0.2,-2.1)], "delay": 150.0 / 1000.0},
}
SCOPES = {"None": 1.0, "Holo": 1.2, "8x": 3.8, "16x": 7.6}
MUZZLES = {"None": 1.0, "Muzzle Brake": 0.8, "Suppressor": 0.8}

# --- APPLICATION STATE MANAGEMENT ---
class AppState:
    def __init__(self):
        self.script_enabled = False
        self.lmb_down = False
        self.rmb_down = False
        self.crouching = False 
        self.config_file = "config.json"
        self.defaults = {
            "current_weapon": "Assault Rifle",
            "current_scope": "None",
            "current_muzzle": "None",
            "sensitivity": 0.5, 
            "ads_sensitivity": 1.0, 
            "fov": 90.0, 
            "toggle_key": "x1",
            "recoil_randomization_radius": 3.0,
            "dpi": 800.0,
            "reaction_time_randomness_ms": 20.0 # NEW: Control for randomized reaction time (0-X ms)
        }
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            for key, value in self.defaults.items():
                setattr(self, key, config.get(key, value))
        except (FileNotFoundError, json.JSONDecodeError):
            for key, value in self.defaults.items():
                setattr(self, key, value)
        self.save_config()

    def save_config(self):
        config_data = {key: getattr(self, key) for key in self.defaults.keys()}
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=4)

app_state = AppState()
CROUCH_KEY = keyboard.Key.ctrl_l

# Initialize pynput mouse controller globally
mouse_controller = mouse.Controller()

REFERENCE_DPI = 800.0 

# --- HUMANIZATION UTILITIES ---

def ease_out_quad(t):
    """Easing function for smoother movements."""
    return t * (2 - t)

def move_mouse_smoothly(dx, dy, duration, steps=20):
    """
    Moves the mouse smoothly by breaking down the movement into smaller steps.
    Incorporates a bit of perlin noise for micro-jitter within the smooth move.
    """
    if dx == 0 and dy == 0:
        return

    current_x, current_y = 0, 0 
    
    noise_gen_x_micro = PerlinNoise(octaves=2, seed=random.randint(1, 10000))
    noise_gen_y_micro = PerlinNoise(octaves=2, seed=random.randint(1, 10000))

    for i in range(steps):
        if not (app_state.lmb_down and app_state.rmb_down):
            break 

        t = (i + 1) / steps 
        eased_t = ease_out_quad(t) 

        target_step_x = dx * eased_t
        target_step_y = dy * eased_t

        move_this_step_x = target_step_x - current_x
        move_this_step_y = target_step_y - current_y

        jitter_x = noise_gen_x_micro(i * 0.5) * random.uniform(0.1, 0.5) 
        jitter_y = noise_gen_y_micro(i * 0.5) * random.uniform(0.1, 0.5)

        final_move_x = int(move_this_step_x + jitter_x)
        final_move_y = int(move_this_step_y + jitter_y)

        mouse_controller.move(final_move_x, final_move_y)
        
        current_x += final_move_x
        current_y += final_move_y

        time.sleep(duration / steps)

# Removed: background_tremor_thread as per user request

# --- BACKEND LOGIC ---
def recoil_control_thread():
    recoil_active = False
    
    noise_x_gen = PerlinNoise(octaves=4, seed=random.randint(1, 100000))
    noise_y_gen = PerlinNoise(octaves=4, seed=random.randint(1, 100000))
    
    while True:
        try:
            if app_state.script_enabled and app_state.lmb_down and app_state.rmb_down and not recoil_active:
                recoil_active = True
                print("Recoil control activated.") 
                
                # Randomized reaction time control
                # Base 80ms + up to reaction_time_randomness_ms
                reaction_delay = 0.080 + random.uniform(0, app_state.reaction_time_randomness_ms / 1000.0)
                time.sleep(reaction_delay) 

                encrypted_weapon_key = xor_cipher(app_state.current_weapon, CIPHER_KEY)
                weapon = WEAPONS[encrypted_weapon_key]
                
                movement_factor = 2.0 if app_state.crouching else 1.0 

                for i, (dx_center, dy_center) in enumerate(weapon["pattern"]): 
                    if not (app_state.lmb_down and app_state.rmb_down):
                        break

                    num_shots = len(weapon["pattern"])
                    progress = i / num_shots if num_shots > 0 else 0

                    compensation_strength = random.uniform(0.85, 0.95) 
                    if progress < 0.2: 
                        compensation_strength *= random.uniform(0.9, 1.0) 
                    elif progress > 0.8:
                        compensation_strength *= random.uniform(0.95, 1.05) 

                    scope_mult = SCOPES[app_state.current_scope]
                    muzzle_mult = MUZZLES[app_state.current_muzzle]

                    # --- PRECISE PIXEL CONVERSION MATH (BASED ON YOUR PROVIDED FORMULA) ---
                    calculated_denominator = (-0.03 * \
                                              ((app_state.sensitivity * app_state.ads_sensitivity) * movement_factor) * \
                                              3.0 * \
                                              (app_state.fov / 100.0))
                    
                    if app_state.dpi > 0: 
                        calculated_denominator *= (REFERENCE_DPI / app_state.dpi)
                    else:
                        print("ERROR: DPI is set to 0. Please set a valid DPI. Skipping movement for this step.")
                        time.sleep(0.01)
                        continue

                    if calculated_denominator == 0: 
                        print("ERROR: Calculated denominator is ZERO after DPI adjustment. Check settings/formula. Skipping movement for this step.")
                        time.sleep(0.01)
                        continue
                    
                    center_pixel_x = (dx_center * scope_mult * muzzle_mult) / calculated_denominator
                    center_pixel_y = (dy_center * scope_mult * muzzle_mult) / calculated_denominator

                    # Circle-based Randomization
                    random_radius = app_state.recoil_randomization_radius * math.sqrt(random.uniform(0, 1)) 
                    random_angle = random.uniform(0, 2 * math.pi)

                    offset_x_in_circle = random_radius * math.cos(random_angle)
                    offset_y_in_circle = random_radius * math.sin(random_angle)

                    target_pixel_x = center_pixel_x + offset_x_in_circle
                    target_pixel_y = center_pixel_y + offset_y_in_circle

                    target_pixel_x *= compensation_strength
                    target_pixel_y *= compensation_strength

                    # Perlin Noise Injection for organic movement (on top of circle randomization)
                    noise_intensity = 2.5 
                    if progress < 0.2: noise_intensity *= random.uniform(1.2, 1.5) 
                    elif progress > 0.8: noise_intensity *= random.uniform(0.8, 1.0) 

                    noise_x = noise_x_gen(i * 0.1) * noise_intensity
                    noise_y = noise_y_gen(i * 0.1) * noise_intensity
                    
                    final_dx = target_pixel_x + noise_x
                    final_dy = target_pixel_y + noise_y

                    # Removed: Micro-flicks/overcorrections as per user request

                    step_duration = weapon["delay"] * random.uniform(0.9, 1.1)
                    move_mouse_smoothly(final_dx, final_dy, step_duration)
                    
                recoil_active = False
                print("Recoil control deactivated.") 
            
            time.sleep(0.001) 
        except Exception as e:
            print(f"Error in recoil thread: {e}")
            recoil_active = False
            time.sleep(1) 

# --- LOW-LEVEL LISTENERS ---
def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        app_state.lmb_down = pressed
    elif button == mouse.Button.right:
        app_state.rmb_down = pressed
    elif (app_state.toggle_key == 'x1' and button == mouse.Button.x1 and pressed) or \
         (app_state.toggle_key == 'x2' and button == mouse.Button.x2 and pressed):
        app_state.script_enabled = not app_state.script_enabled
        status_str = "ENABLED" if app_state.script_enabled else "DISABLED"
        print(f"--- SCRIPT {status_str} ---")
        if 'app' in globals() and app.winfo_exists():
            app.frames['controls'].update_status_display()

def on_press(key):
    if key == CROUCH_KEY:
        app_state.crouching = True

def on_release(key):
    if key == CROUCH_KEY:
        app_state.crouching = False

# --- UTILITY & ANIMATION ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def create_resized_image(image_path, new_width):
    try:
        img = Image.open(image_path)
        w, h = img.size
        aspect_ratio = h / w
        new_h = int(new_width * aspect_ratio)
        return ctk.CTkImage(img, size=(new_width, new_h))
    except (FileNotFoundError, AttributeError) as e:
        print(f"ERROR: Image loading failed for {image_path}. Ensure it exists and is valid. Error: {e}")
        return None

class Animator:
    def __init__(self, widget):
        self.widget = widget
    def slide(self, start_pos, end_pos, duration=0.4, on_complete=None, axis='y'):
        steps = int(duration * 60)
        total_delta = end_pos - start_pos
        def ease_out_quad(n): return 1 - (1 - n) * (1 - n)
        def _animate(step):
            if not self.widget.winfo_exists(): return
            progress = min(1.0, step / steps)
            eased_progress = ease_out_quad(progress)
            current_pos = start_pos + total_delta * eased_progress
            if axis == 'y': self.widget.place_configure(rely=current_pos)
            else: self.widget.place_configure(relx=current_pos)
            if step < steps: self.widget.after(int(duration * 1000 / steps), _animate, step + 1)
            elif on_complete: on_complete()
        _animate(0)

class HoverButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_color = self.cget("fg_color")
        # Hover binds are re-enabled as they seem stable now
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    def on_enter(self, event): self.configure(fg_color=self.cget("hover_color"))
    def on_leave(self, event): self.configure(fg_color=self.original_color)

# --- GUI FRAMES / VIEWS ---
class BaseFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.widgets = []
    def animate_in(self, delay_step=70):
        for i, widget in enumerate(self.widgets):
            widget.place(relx=0.5, rely=1.5, anchor="n")
            self.after(i * delay_step, lambda w=widget: Animator(w).slide(start_pos=1.5, end_pos=w.default_y, axis='y'))
    def animate_out(self, on_complete=None):
        for i, widget in enumerate(reversed(self.widgets)):
            self.after(i * 50, lambda w=widget: Animator(w).slide(start_pos=w.default_y, end_pos=1.5, duration=0.3, on_complete=on_complete if w == self.widgets[0] else None))

class ControlsFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pulse_active = False
        self.setup_widgets()
        self.animate_in()
        self.update_status_display() 

    def setup_widgets(self):
        status_card = ctk.CTkFrame(self, fg_color=FRAME_BG_COLOR, corner_radius=12)
        status_card.default_y = 0.1
        loadout_card = ctk.CTkFrame(self, fg_color=FRAME_BG_COLOR, corner_radius=12)
        loadout_card.default_y = 0.4
        self.widgets.extend([status_card, loadout_card])
        self.status_value = ctk.CTkLabel(status_card, text="INACTIVE", text_color=ACCENT_RED, font=("Arial", 22, "bold"))
        self.status_value.pack(pady=(20, 15), padx=20)
        self.toggle_switch = ctk.CTkSwitch(status_card, text="Enable Script", command=self.toggle_script, progress_color=ACCENT_GREEN)
        self.toggle_switch.pack(pady=(0, 20), padx=20)
        title_frame = ctk.CTkFrame(loadout_card, fg_color="transparent")
        title_frame.pack(pady=(15, 10))
        ctk.CTkLabel(title_frame, text="🔫", font=("Arial", 16)).pack(side="left", padx=(0, 6))
        ctk.CTkLabel(title_frame, text="WEAPON", font=("Arial", 12, "bold"), text_color=SUBTEXT_COLOR).pack(side="left")
        decrypted_weapon_names = [xor_cipher(w, CIPHER_KEY) for w in WEAPONS.keys()]
        self.weapon_menu = ctk.CTkOptionMenu(loadout_card, values=decrypted_weapon_names, command=self.set_weapon, fg_color=BUTTON_COLOR, button_color=BUTTON_COLOR, button_hover_color=BUTTON_HOVER_COLOR)
        self.weapon_menu.pack(pady=5, padx=15, fill="x")
        self.scope_menu = ctk.CTkOptionMenu(loadout_card, values=list(SCOPES.keys()), command=self.set_scope, fg_color=BUTTON_COLOR, button_color=BUTTON_COLOR, button_hover_color=BUTTON_HOVER_COLOR)
        self.scope_menu.pack(pady=5, padx=15, fill="x")
        self.muzzle_menu = ctk.CTkOptionMenu(loadout_card, values=list(MUZZLES.keys()), command=self.set_muzzle, fg_color=BUTTON_COLOR, button_color=BUTTON_COLOR, button_hover_color=BUTTON_HOVER_COLOR)
        self.muzzle_menu.pack(pady=5, padx=15, fill="x")
        self.load_state()

    def load_state(self):
        self.weapon_menu.set(app_state.current_weapon)
        self.scope_menu.set(app_state.current_scope)
        self.muzzle_menu.set(app_state.current_muzzle)

    def update_status_display(self):
        is_enabled = app_state.script_enabled
        if is_enabled:
            self.toggle_switch.select()
            self.status_value.configure(text="ACTIVE", text_color=ACCENT_GREEN)
            if not self.pulse_active:
                self.pulse_active = True
                self.pulse_animation()
        else:
            self.toggle_switch.deselect()
            self.status_value.configure(text="INACTIVE", text_color=ACCENT_RED)
            self.pulse_active = False

    def toggle_script(self):
        app_state.script_enabled = not app_state.script_enabled
        self.update_status_display()

    def pulse_animation(self):
        if self.pulse_active and self.winfo_exists():
            self.status_value.configure(text_color="#66BB6A" if self.status_value.cget("text_color")[1] == ACCENT_GREEN else ACCENT_GREEN)
            self.after(750, self.pulse_animation)

    def set_weapon(self, choice):
        app_state.current_weapon = choice
        app_state.save_config()
    def set_scope(self, choice):
        app_state.current_scope = choice
        app_state.save_config()
    def set_muzzle(self, choice):
        app_state.current_muzzle = choice
        app_state.save_config()

class SettingsFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        self.setup_widgets()
        self.animate_in()
    def setup_widgets(self):
        settings_card = ctk.CTkFrame(self, fg_color=FRAME_BG_COLOR, corner_radius=12)
        settings_card.default_y = 0.1
        self.widgets.append(settings_card)
        title_frame = ctk.CTkFrame(settings_card, fg_color="transparent")
        title_frame.pack(pady=(15, 10))
        ctk.CTkLabel(title_frame, text="⚙️", font=("Arial", 14)).pack(side="left", padx=(0, 6))
        ctk.CTkLabel(title_frame, text="SETTINGS", font=("Arial", 12, "bold"), text_color=SUBTEXT_COLOR).pack(side="left")
        
        # Sensitivity
        sens_frame = ctk.CTkFrame(settings_card, fg_color="transparent")
        ctk.CTkLabel(sens_frame, text="Sensitivity", font=("Arial", 14)).pack(side="left", padx=10)
        self.sens_entry = ctk.CTkEntry(sens_frame, justify="center", width=80)
        self.sens_entry.pack(side="right", padx=10)
        sens_frame.pack(pady=10, padx=10, fill="x")
        
        # ADS Sensitivity
        ads_frame = ctk.CTkFrame(settings_card, fg_color="transparent")
        ctk.CTkLabel(ads_frame, text="ADS Sensitivity", font=("Arial", 14)).pack(side="left", padx=10)
        self.ads_entry = ctk.CTkEntry(ads_frame, justify="center", width=80)
        self.ads_entry.pack(side="right", padx=10)
        ads_frame.pack(pady=10, padx=10, fill="x")
        
        # FOV
        fov_frame = ctk.CTkFrame(settings_card, fg_color="transparent")
        ctk.CTkLabel(fov_frame, text="Field of View (FOV)", font=("Arial", 14)).pack(side="left", padx=10)
        self.fov_entry = ctk.CTkEntry(fov_frame, justify="center", width=80)
        self.fov_entry.pack(side="right", padx=10)
        fov_frame.pack(pady=10, padx=10, fill="x")

        # Recoil Randomization Radius 
        radius_frame = ctk.CTkFrame(settings_card, fg_color="transparent")
        ctk.CTkLabel(radius_frame, text="Recoil Randomness (px)", font=("Arial", 14)).pack(side="left", padx=10)
        self.radius_entry = ctk.CTkEntry(radius_frame, justify="center", width=80)
        self.radius_entry.pack(side="right", padx=10)
        radius_frame.pack(pady=10, padx=10, fill="x")

        # DPI Setting
        dpi_frame = ctk.CTkFrame(settings_card, fg_color="transparent")
        ctk.CTkLabel(dpi_frame, text="Mouse DPI", font=("Arial", 14)).pack(side="left", padx=10)
        self.dpi_entry = ctk.CTkEntry(dpi_frame, justify="center", width=80)
        self.dpi_entry.pack(side="right", padx=10)
        dpi_frame.pack(pady=10, padx=10, fill="x")

        # NEW: Randomized Reaction Time Control
        react_time_frame = ctk.CTkFrame(settings_card, fg_color="transparent")
        ctk.CTkLabel(react_time_frame, text="Reaction Time Randomness (ms)", font=("Arial", 14)).pack(side="left", padx=10)
        self.react_time_entry = ctk.CTkEntry(react_time_frame, justify="center", width=80)
        self.react_time_entry.pack(side="right", padx=10)
        react_time_frame.pack(pady=10, padx=10, fill="x")

        self.save_button = ctk.CTkButton(settings_card, text="Save Settings", fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, command=self.save_settings)
        self.save_button.pack(pady=20)
        self.load_state()

    def load_state(self):
        self.sens_entry.insert(0, str(app_state.sensitivity))
        self.ads_entry.insert(0, str(app_state.ads_sensitivity))
        self.fov_entry.insert(0, str(app_state.fov))
        self.radius_entry.insert(0, str(app_state.recoil_randomization_radius))
        self.dpi_entry.insert(0, str(app_state.dpi)) 
        self.react_time_entry.insert(0, str(app_state.reaction_time_randomness_ms)) # Load reaction time randomness

    def save_settings(self):
        try:
            app_state.sensitivity = float(self.sens_entry.get())
            app_state.ads_sensitivity = float(self.ads_entry.get())
            app_state.fov = float(self.fov_entry.get())
            app_state.recoil_randomization_radius = float(self.radius_entry.get()) 
            app_state.dpi = float(self.dpi_entry.get()) 
            app_state.reaction_time_randomness_ms = float(self.react_time_entry.get()) # Save reaction time randomness
            app_state.save_config()
            self.save_button.configure(text="Saved!", fg_color=ACCENT_GREEN, hover_color=ACCENT_GREEN)
            self.after(2000, lambda: self.save_button.configure(text="Save Settings", fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR))
        except ValueError:
            self.save_button.configure(text="Invalid Input!", fg_color=ACCENT_RED, hover_color=ACCENT_RED)
            self.after(2000, lambda: self.save_button.configure(text="Save Settings", fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR))

class LoginWindow(BaseFrame):
    def __init__(self, master, on_complete):
        super().__init__(master)
        self.on_complete = on_complete
        self.setup_widgets()
        self.animate_in(delay_step=100)
    def setup_widgets(self):
        self.logo_label = ctk.CTkLabel(self, text="", image=create_resized_image(resource_path("Brand.png"), new_width=250))
        self.logo_label.default_y = 0.35
        self.key_entry = ctk.CTkEntry(self, placeholder_text="Authentication Key", width=300, height=40, justify="center", fg_color=FRAME_BG_COLOR, border_width=0, corner_radius=8)
        self.key_entry.default_y = 0.6
        # Adjusted default_y for better placement of the Activate button
        self.activate_button = ctk.CTkButton(self, text="Activate", command=self.launch_main_app, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, height=40, corner_radius=8, font=("Arial", 12, "bold"))
        self.activate_button.default_y = 0.85 
        self.widgets.extend([self.logo_label, self.key_entry, self.activate_button])
    def animate_in(self, delay_step=70):
        for i, widget in enumerate(self.widgets):
            anchor_point = "center" if widget == self.logo_label else "n"
            widget.place(relx=0.5, rely=1.5, anchor=anchor_point)
            self.after(i * delay_step, lambda w=widget: Animator(w).slide(start_pos=1.5, end_pos=w.default_y, axis='y'))
    def launch_main_app(self):
        self.animate_out(on_complete=self.on_complete)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("420x550")
        self.title(xor_cipher("Ukgtbgtv EQPZVT", "somekey")) 
        self.configure(fg_color=WINDOW_BG_COLOR)
        self.overrideredirect(True) 
        
        self.update() 
        self.center_window() 
        
        self.show_splash() 
        print("App initialized. Starting splash display.")

    def center_window(self):
        w, h = self.winfo_width(), self.winfo_height()
        x, y = (self.winfo_screenwidth() // 2) - (w // 2), (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def show_splash(self):
        splash_label = ctk.CTkLabel(self, text="", fg_color=WINDOW_BG_COLOR)
        splash_label.pack(fill="both", expand=True)
        splash_image = create_resized_image(resource_path("Brand.png"), new_width=300)
        if splash_image:
            ctk.CTkLabel(splash_label, text="", image=splash_image, fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")
        self.after(2500, lambda: self.show_login(splash_label))
        print("Splash screen setup complete. Timer for login started.")

    def show_login(self, splash_label):
        splash_label.destroy()
        login_frame = LoginWindow(self, on_complete=self.show_main_interface)
        login_frame.pack(fill="both", expand=True)
        print("Login window displayed.")

    def show_main_interface(self): 
        for widget in self.winfo_children():
            if isinstance(widget, LoginWindow):
                widget.destroy()
        sidebar = ctk.CTkFrame(self, width=70, fg_color=SIDEBAR_COLOR, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        self.content_area = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.content_area.pack(side="right", fill="both", expand=True)
        # Close button for borderless window
        HoverButton(self, text="✕", command=self.destroy, fg_color="transparent", hover_color=ACCENT_RED, width=30, height=30, font=("Arial", 16)).place(relx=1.0, rely=0, anchor="ne")
        sidebar.bind("<ButtonPress-1>", self.start_move)
        sidebar.bind("<B1-Motion>", self.do_move)
        
        # MODIFIED: Use .place() for more precise positioning of sidebar elements
        sidebar_logo_label = ctk.CTkLabel(sidebar, text="", image=create_resized_image(resource_path("Brand.png"), new_width=50))
        if sidebar_logo_label.cget("image"): 
            sidebar_logo_label.place(relx=0.5, rely=0.08, anchor="center") # Adjusted rely for logo (was 0.10)

        self.frames = {}
        self.current_frame_name = None
        # Gamepad icon (Controls)
        HoverButton(sidebar, text="🎮", fg_color="transparent", hover_color="#2c2c2c", text_color=SUBTEXT_COLOR, 
                    width=50, font=("Arial", 28), command=lambda: self.show_frame("controls")) \
                    .place(relx=0.5, rely=0.22, anchor="center") # Adjusted rely (was 0.25)

        # Settings wheel icon (Settings)
        HoverButton(sidebar, text="⚙️", fg_color="transparent", hover_color="#2c2c2c", text_color=SUBTEXT_COLOR, 
                    width=50, font=("Arial", 24), command=lambda: self.show_frame("settings")) \
                    .place(relx=0.5, rely=0.36, anchor="center") # Adjusted rely (was 0.40)
        
        self.show_frame("controls")
        self.after(100, self.lift) 
        self.after(150, self.attributes, '-topmost', True) 
        self.after(200, self.attributes, '-topmost', False) 
        print("Main interface setup complete. Attempted to bring window to foreground.")

    def show_frame(self, name):
        if name == self.current_frame_name: return
        if self.current_frame_name and self.frames.get(self.current_frame_name):
            old_frame = self.frames[self.current_frame_name]
            old_frame.animate_out(on_complete=lambda: self._create_new_frame(name, old_frame))
        else: self._create_new_frame(name)

    def _create_new_frame(self, name, old_frame_to_destroy=None):
        if old_frame_to_destroy: old_frame_to_destroy.destroy()
        frame_class = ControlsFrame if name == "controls" else SettingsFrame
        self.frames[name] = frame_class(self.content_area)
        self.frames[name].pack(fill="both", expand=True)
        self.current_frame_name = name
        print(f"Frame '{name}' loaded and packed.")

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        self.geometry(f"+{self.winfo_x() + event.x - self.x}+{self.winfo_y() + event.y - self.y}")

# --- MAIN STARTUP BLOCK ---
if __name__ == "__main__":
    app = None
    try:
        print("Starting input listeners...")
        mouse_listener = mouse.Listener(on_click=on_click)
        keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        mouse_listener.start()
        keyboard_listener.start()
        print("SUCCESS: Input listeners started.")

        threading.Thread(target=recoil_control_thread, daemon=True).start()
        print("SUCCESS: Recoil control thread started.")
        
        print("Starting GUI...")
        app = App() 
        app.mainloop()

    except Exception as e:
        print(f"A fatal error occurred: {e}")
        if "No module named 'pynput'" in str(e):
            ctypes.windll.user32.MessageBoxW(0, "Pynput library not found. Please install it: pip install pynput", "Missing Library Error", 0x10)
        elif "Brand.png" in str(e) or "image" in str(e).lower(): 
            ctypes.windll.user32.MessageBoxW(0, f"Error loading image resource (e.g., Brand.png). Ensure it's in the script folder and not corrupted. Error: {e}", "Image Load Error", 0x10)
        else:
            ctypes.windll.user32.MessageBoxW(0, f"A fatal error occurred: {e}", "Fatal Error", 0x10)

    finally:
        print("Exiting. Stopping threads and listeners...")
        time.sleep(0.1) 
        if 'mouse_listener' in locals() and mouse_listener.is_alive(): mouse_listener.stop()
        if 'keyboard_listener' in locals() and keyboard_listener.is_alive(): keyboard_listener.stop()
        print("Script finished.")