import customtkinter as ctk
import threading
import webbrowser
import requests
from PIL import Image
from io import BytesIO
from .backend import Backend

# --- HEXTECH THEME PALETTE ---
C_BG = "#010A13"        # Deepest Navy
C_PANEL = "#091428"     # Riot Navy
C_GOLD = "#C8AA6E"      # Hextech Gold
C_GOLD_HOVER = "#F0E6D2"
C_ACCENT = "#0AC8B9"    # Hextech Cyan (Magic)
C_TEXT = "#F0E6D2"      # High-contrast Pearl

class HextechApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.backend = Backend()
        self.patch = self.backend.get_patch_version()
        self.model_name = self.backend.ollama_model.upper()

        # Window Configuration
        self.geometry("950x750")
        self.title(f"LOLSTATIC // {self.model_name}")
        self.configure(fg_color=C_BG)

        # 1. HEADER SECTION
        self.header = ctk.CTkFrame(self, fg_color=C_PANEL, height=75, corner_radius=0, border_width=1, border_color=C_GOLD)
        self.header.pack(fill="x", side="top")
        
        ctk.CTkLabel(self.header, text="LOLSTATIC", font=("Impact", 35), text_color=C_GOLD).pack(side="left", padx=25)
        ctk.CTkLabel(self.header, text=f"PATCH {self.patch}", font=("Arial", 14, "bold"), text_color=C_ACCENT).pack(side="right", padx=25)

        # 2. NAVIGATION TABS (Hextech Styled)
        self.tabs = ctk.CTkTabview(self, width=920, height=640, fg_color=C_PANEL, 
                                   segmented_button_selected_color=C_GOLD, 
                                   segmented_button_selected_hover_color=C_ACCENT,
                                   segmented_button_unselected_color=C_BG,
                                   text_color="white", border_width=1, border_color=C_GOLD)
        self.tabs.pack(pady=15, padx=15, fill="both", expand=True)
        
        # Initialize Tabs
        for name in ["COACH", "TIER LIST", "CHAMPIONS", "PATCH NOTES"]:
            self.tabs.add(name)

        self.setup_coach()
        self.setup_tier_list()
        self.setup_champions()
        self.setup_patch_notes()

    def log(self, text, box):
        """Thread-safe logging helper"""
        box.insert("end", text + "\n")
        box.see("end")

    # ==========================
    # TAB 1: AI COACH
    # ==========================
    def setup_coach(self):
        tab = self.tabs.tab("COACH")
        
        # Input Frame
        frame = ctk.CTkFrame(tab, fg_color="transparent")
        frame.pack(pady=20)
        
        self.name = ctk.CTkEntry(frame, placeholder_text="Summoner Name", width=200, fg_color="#1E2328", border_color=C_GOLD)
        self.name.grid(row=0, column=0, padx=10)
        self.name.bind("<Return>", lambda e: self.run_coach())
        
        self.tag = ctk.CTkEntry(frame, placeholder_text="Tag", width=100, fg_color="#1E2328", border_color=C_GOLD)
        self.tag.grid(row=0, column=1, padx=10)
        self.tag.bind("<Return>", lambda e: self.run_coach())

        self.region = ctk.CTkComboBox(frame, values=["EUW1", "NA1", "KR", "OC1"], width=110, fg_color="#1E2328", border_color=C_GOLD, button_color=C_GOLD)
        self.region.grid(row=0, column=2, padx=10)

        # Action Button
        self.btn_coach = ctk.CTkButton(tab, text="ANALYZE PERFORMANCE", font=("Arial", 14, "bold"), 
                                         fg_color=C_ACCENT, text_color="black", hover_color="#08A092", 
                                         height=45, command=self.run_coach)
        self.btn_coach.pack(pady=10)

        # Output Console
        self.out_coach = ctk.CTkTextbox(tab, width=850, height=400, fg_color=C_BG, text_color=C_TEXT, 
                                        font=("Consolas", 13), border_width=1, border_color=C_GOLD)
        self.out_coach.pack(pady=10)
        self.log(">> COACH SYSTEM ONLINE. WAITING FOR PLAYER DATA...", self.out_coach)

    def run_coach(self):
        self.btn_coach.configure(state="disabled", text="THINKING...")
        self.out_coach.delete("0.0", "end")
        threading.Thread(target=self._coach_thread, daemon=True).start()

    def _coach_thread(self):
        name, tag, region = self.name.get(), self.tag.get().replace("#",""), self.region.get()
        self.log(f">> ACCESSING RIOT SERVERS FOR: {name} #{tag}...", self.out_coach)
        
        puuid = self.backend.get_player_puuid(name, tag, region)
        
        if not puuid:
            self.log("❌ ERROR 401: Unauthorized. Please check your Riot API Key in settings.json.", self.out_coach)
        else:
            matches = self.backend.get_recent_matches(puuid, region)
            stats = [self.backend.analyze_match(m, puuid, region) for m in matches if self.backend.analyze_match(m, puuid, region)]
            
            if not stats:
                self.log("⚠️ No recent match data found for this account.", self.out_coach)
            else:
                data_str = "\n".join(stats)
                self.log(f">> DATA ACQUIRED:\n{data_str}", self.out_coach)
                self.log(f">> CONSULTING {self.model_name}...", self.out_coach)
                
                prompt = f"Act as a professional LoL Coach. Analyze these games:\n{data_str}\nProvide 3 analytical tips for macro/farming."
                self.backend.ask_ai(prompt, lambda r: self.log(f"\n📋 COACH REPORT:\n{r}", self.out_coach))
        
        self.after(0, lambda: self.btn_coach.configure(state="normal", text="ANALYZE PERFORMANCE"))

    # ==========================
    # TAB 2: TIER LIST
    # ==========================
    def setup_tier_list(self):
        tab = self.tabs.tab("TIER LIST")
        ctk.CTkButton(tab, text="GENERATE META ANALYSIS", font=("Arial", 14, "bold"), 
                      fg_color=C_GOLD, text_color="black", hover_color=C_GOLD_HOVER, 
                      command=self.run_tier).pack(pady=20)
        
        self.out_tier = ctk.CTkTextbox(tab, width=850, height=450, fg_color=C_BG, text_color=C_ACCENT, 
                                       font=("Consolas", 13), border_width=1, border_color=C_GOLD)
        self.out_tier.pack()

    def run_tier(self):
        self.out_tier.delete("0.0", "end")
        self.log(">> GENERATING TIER LIST FROM LOCAL AI CORE...", self.out_tier)
        prompt = f"List S-Tier champions for Patch {self.patch} for all LoL roles. Be concise and professional."
        threading.Thread(target=lambda: self.backend.ask_ai(prompt, lambda r: self.log(r, self.out_tier)), daemon=True).start()

    # ==========================
    # TAB 3: CHAMPIONS (With Images)
    # ==========================
    def setup_champions(self):
        tab = self.tabs.tab("CHAMPIONS")
        self.champ_search = ctk.CTkEntry(tab, placeholder_text="Search Champion Database...", width=400, border_color=C_GOLD)
        self.champ_search.pack(pady=15)
        
        # ✅ FIX: Use lambda to correctly bind the event
        self.champ_search.bind("<KeyRelease>", lambda event: self.filter_champs(event))
        
        self.scroll = ctk.CTkScrollableFrame(tab, width=850, height=450, fg_color=C_BG, border_width=1, border_color=C_GOLD)
        self.scroll.pack(pady=10)
        
        self.all_champs = []
        threading.Thread(target=self.load_champs, daemon=True).start()

    def load_champs(self):
        self.all_champs = self.backend.get_champions(self.patch)
        self.update_list(self.all_champs)

    def update_list(self, champs):
        """Loads champion icons from Data Dragon"""
        for w in self.scroll.winfo_children(): w.destroy()
        
        # Limit to first 60 for performance
        for c in champs[:60]:
            try:
                # Fetch Icon from Riot CDN
                url = f"https://ddragon.leagueoflegends.com/cdn/{self.patch}/img/champion/{c}.png"
                img_data = Image.open(BytesIO(requests.get(url, timeout=5).content))
                img = ctk.CTkImage(img_data, size=(45, 45))
                
                btn = ctk.CTkButton(self.scroll, text=f"  {c}", image=img, compound="left", anchor="w", 
                                     fg_color="#1E2328", hover_color=C_GOLD, text_color="white", corner_radius=8)
                btn.pack(fill="x", pady=4, padx=10)
            except:
                # Fallback if image fails to load
                ctk.CTkButton(self.scroll, text=c, anchor="w", fg_color="#1E2328").pack(fill="x", pady=2)

    # ✅ FIX: Added 'event' parameter for Tkinter binder
    def filter_champs(self, event=None):
        q = self.champ_search.get().lower()
        filtered = [c for c in self.all_champs if q in c.lower()]
        self.update_list(filtered)

    # ==========================
    # TAB 4: PATCH NOTES
    # ==========================
    def setup_patch_notes(self):
        tab = self.tabs.tab("PATCH NOTES")
        
        ctk.CTkLabel(tab, text=f"HEXTECH ARCHIVE: {self.patch}", font=("Impact", 45), text_color=C_GOLD).pack(pady=60)
        ctk.CTkLabel(tab, text="Direct connection to Riot News Servers established.", font=("Arial", 14), text_color="gray").pack()
        
        ctk.CTkButton(tab, text="VIEW LIVE PATCH NOTES", font=("Arial", 22, "bold"), 
                      height=70, width=400, fg_color=C_ACCENT, text_color="black", hover_color="#08A092",
                      command=lambda: webbrowser.open("https://www.leagueoflegends.com/en-us/news/game-updates/patch-notes/")).pack(pady=30)