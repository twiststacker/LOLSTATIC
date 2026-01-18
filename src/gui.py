import customtkinter as ctk
import math

# Ultra-modern appearance settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class HextechApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("LOLSTATIC // CORE")
        self.geometry("900x650")
        self.configure(fg_color="#050508")

        # Layout Config
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Glass-morphism Container
        self.container = ctk.CTkFrame(self, fg_color="#0d0d16", corner_radius=30, border_width=1, border_color="#1f1f33")
        self.container.grid(row=0, column=0, padx=60, pady=60, sticky="nsew")
        
        self.setup_ui()
        
        # Animation variables
        self.glow_step = 0
        self.animate_button()

    def setup_ui(self):
        # Header
        self.title_label = ctk.CTkLabel(self.container, text="LOLSTATIC", 
                                        font=ctk.CTkFont(family="Orbitron", size=36, weight="bold"),
                                        text_color="#00d4ff")
        self.title_label.pack(pady=(50, 5))

        self.status_led = ctk.CTkLabel(self.container, text="● SYSTEM ONLINE", font=("Consolas", 10), text_color="#00ff88")
        self.status_led.pack(pady=(0, 40))

        # Pill-Shaped Input
        self.input_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.input_frame.pack(pady=10)

        self.summoner_entry = ctk.CTkEntry(self.input_frame, placeholder_text="SUMMONER NAME #TAG", 
                                           width=380, height=54, corner_radius=27, 
                                           border_color="#00d4ff", fg_color="#08080f",
                                           font=ctk.CTkFont(size=14))
        self.summoner_entry.pack(side="left", padx=10)

        self.forge_btn = ctk.CTkButton(self.input_frame, text="FORGE", width=120, height=54, 
                                        corner_radius=27, fg_color="#00d4ff", text_color="#050508",
                                        font=ctk.CTkFont(size=14, weight="bold"))
        self.forge_btn.pack(side="left")

        # Modern Console
        self.console = ctk.CTkTextbox(self.container, corner_radius=20, fg_color="#050508", 
                                      border_width=1, border_color="#1f1f33",
                                      font=("Consolas", 13), text_color="#8888aa")
        self.console.pack(fill="both", expand=True, padx=50, pady=(40, 50))
        self.console.insert("0.0", ">>> CORE INITIALIZED...\n>>> READY TO ANALYZE MATCH DATA...")

    def animate_button(self):
        """Creates a smooth pulsing glow effect"""
        # Calculate a smooth sine wave for color intensity
        intensity = int(127 + 127 * math.sin(self.glow_step))
        hex_color = f'#00{intensity:02x}ff'
        
        self.forge_btn.configure(fg_color=hex_color)
        self.glow_step += 0.05
        
        # Repeat every 50ms
        self.after(50, self.animate_button)

if __name__ == "__main__":
    app = HextechApp()
    app.mainloop()