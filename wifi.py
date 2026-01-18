import customtkinter as ctk
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from typing import List, Tuple, Dict
import platform
import locale
import json
import csv
import qrcode
from PIL import Image, ImageTk
import os
import sys
import ctypes
import threading
import pystray
from pystray import MenuItem as item

# --- Konsolu Gizle ---
def hide_console():
    if platform.system() == "Windows":
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        hWnd = kernel32.GetConsoleWindow()
        if hWnd:
            user32.ShowWindow(hWnd, 0)

hide_console()

# --- Konfigürasyon & Tema ---
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class WiFiManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Temel Ayarlar
        self.title("Aura Wireless Intelligence")
        self.geometry("1100x700")
        self.minsize(900, 600)
        
        # State
        self.language = "tr"
        self.wifi_data: List[Dict] = []
        self.filtered_data: List[Dict] = []
        self.is_masked = True
        
        # Çeviriler
        self.translations = {
            "tr": {
                "title": "Aura Wi-Fi İstihbaratı",
                "search": "Ağlarda veya parolalarda ara...",
                "refresh": "Sistemi Tara",
                "export": "Dışa Aktar",
                "settings": "Ayarlar",
                "theme": "Görünüm",
                "lang": "Dil",
                "mask": "Parolaları Gizle",
                "unmask": "Parolaları Göster",
                "copy": "Kopyala",
                "qr": "QR Kod",
                "details": "Detaylar",
                "admin_req": "Yönetici Yetkisi Gerekli",
                "export_success": "Veriler başarıyla dışa aktarıldı.",
                "no_data": "Gösterilecek ağ bulunamadı.",
                "interface_info": "Aktif Bağlantı Detayları",
                "found_count": "Kayıtlı Profil",
                "sec_type": "Güvenlik",
                "signal": "Sinyal",
                "disconnected": "Bağlı Değil",
                "os_not_supported": "İşletim sistemi henüz desteklenmiyor."
            },
            "en": {
                "title": "Aura Wi-Fi Intelligence",
                "search": "Search networks or passwords...",
                "refresh": "Scan System",
                "export": "Export Data",
                "settings": "Settings",
                "theme": "Theme",
                "lang": "Language",
                "mask": "Mask Passwords",
                "unmask": "Show Passwords",
                "copy": "Copy",
                "qr": "QR Code",
                "details": "Details",
                "admin_req": "Admin Privileges Required",
                "export_success": "Data exported successfully.",
                "no_data": "No networks found.",
                "interface_info": "Active Connection Details",
                "found_count": "Saved Profiles",
                "sec_type": "Security",
                "signal": "Signal",
                "disconnected": "Disconnected",
                "os_not_supported": "Operating system not supported."
            }
        }

        # UI Başlatma
        self.language = "tr" # Başlangıç dili Türkçe
        self.setup_main_ui()
        self.update_translations() # UI metinlerini dile göre ayarla
        self.refresh_data()

    def setup_main_ui(self):
        # Grid Yapısı
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Main Content
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="AURA", font=ctk.CTkFont(size=28, weight="bold", family="Orbitron"))
        self.logo.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.btn_refresh = ctk.CTkButton(self.sidebar, text="Scan Now", command=self.refresh_data, corner_radius=8)
        self.btn_refresh.grid(row=1, column=0, padx=20, pady=10)

        self.btn_mask = ctk.CTkButton(self.sidebar, text="Show Passwords", command=self.toggle_mask, 
                                     fg_color="#4B5563", hover_color="#374151", border_width=0)
        self.btn_mask.grid(row=2, column=0, padx=20, pady=10)

        self.btn_export = ctk.CTkOptionMenu(self.sidebar, values=["Export CSV", "Export JSON"], command=self.export_data)
        self.btn_export.grid(row=3, column=0, padx=20, pady=10)
        self.btn_export.set("Export")

        # Görünüm & Dil Alt Panel
        self.settings_pane = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.settings_pane.grid(row=5, column=0, padx=20, pady=20, sticky="s")
        self.sidebar.grid_rowconfigure(4, weight=1)

        self.label_theme = ctk.CTkLabel(self.settings_pane, text="Theme:", font=ctk.CTkFont(size=12))
        self.label_theme.pack(anchor="w")
        self.theme_menu = ctk.CTkOptionMenu(self.settings_pane, values=["System", "Dark", "Light"], command=lambda m: ctk.set_appearance_mode(m))
        self.theme_menu.pack(pady=(0, 10))

        self.label_lang = ctk.CTkLabel(self.settings_pane, text="Language:", font=ctk.CTkFont(size=12))
        self.label_lang.pack(anchor="w")
        self.lang_menu = ctk.CTkOptionMenu(self.settings_pane, values=["Türkçe", "English"], command=self.change_lang)
        self.lang_menu.pack()
        self.lang_menu.set("Türkçe")

        # --- Main Content ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=1)

        # Search & Info
        self.top_bar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.top_bar.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(self.top_bar, placeholder_text="Intelligence Search...", height=45, corner_radius=10)
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.filter_results)

        # Active Network Stats
        self.stats_frame = ctk.CTkFrame(self.content_frame, height=100)
        self.stats_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        self.interface_label = ctk.CTkLabel(self.stats_frame, text="Scanning interface...", font=ctk.CTkFont(size=13))
        self.interface_label.pack(pady=15, padx=20, side="left")

        # Scrollable List
        self.scroll_frame = ctk.CTkScrollableFrame(self.content_frame, label_text="Network Database")
        self.scroll_frame.grid(row=2, column=0, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

    def get_wifi_intel(self) -> List[Dict]:
        """Gelişmiş Wi-Fi verisi toplama (Encoding ve Dil Duyarlı)."""
        system = platform.system()
        # En yaygın Windows encodingleri deneme sırasıyla
        encodings = ['cp854', 'utf-8', locale.getpreferredencoding(False)]
        intel = []

        if system == "Windows":
            raw_profiles = ""
            creation_flags = subprocess.CREATE_NO_WINDOW if system == "Windows" else 0
            for enc in encodings:
                try:
                    res = subprocess.run(["netsh", "wlan", "show", "profiles"], 
                                         capture_output=True, text=True, encoding=enc, 
                                         creationflags=creation_flags)
                    if res.returncode == 0:
                        raw_profiles = res.stdout
                        break
                except: continue

            if raw_profiles:
                profile_names = []
                for line in raw_profiles.split('\n'):
                    if ":" in line:
                        parts = line.split(":", 1)
                        key = parts[0].strip()
                        if "Profile" in key or "Profili" in key:
                            profile_names.append(parts[1].strip())

                for name in profile_names:
                    try:
                        raw_pass = ""
                        for enc in encodings:
                            try:
                                p_res = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], 
                                                      capture_output=True, text=True, encoding=enc,
                                                      creationflags=creation_flags)
                                if p_res.returncode == 0:
                                    raw_pass = p_res.stdout
                                    break
                            except: continue
                        
                        if raw_pass:
                            password = "N/A"
                            sec_type = "Unknown"
                            for line in raw_pass.split('\n'):
                                if ":" in line:
                                    p_parts = line.split(":", 1)
                                    p_key = p_parts[0].strip()
                                    if "Key Content" in p_key or "Anahtar İçeriği" in p_key:
                                        password = p_parts[1].strip()
                                    if "Authentication" in p_key or "Kimlik Doğrulama" in p_key:
                                        sec_type = p_parts[1].strip()
                            
                            intel.append({
                                "ssid": name,
                                "password": password,
                                "security": sec_type,
                                "type": "Saved"
                            })
                    except: continue
        
        return sorted(intel, key=lambda x: x['ssid'].lower())

    def get_active_interface_info(self):
        """Aktif bağlantı bilgisini çekme."""
        encodings = ['cp854', 'utf-8', locale.getpreferredencoding(False)]
        t = self.translations[self.language]
        system = platform.system()
        creation_flags = subprocess.CREATE_NO_WINDOW if system == "Windows" else 0
        try:
            raw_int = ""
            for enc in encodings:
                try:
                    res = subprocess.run(["netsh", "wlan", "show", "interfaces"], 
                                         capture_output=True, text=True, encoding=enc,
                                         creationflags=creation_flags)
                    if res.returncode == 0:
                        raw_int = res.stdout
                        break
                except: continue

            if raw_int:
                info = {}
                for line in raw_int.split('\n'):
                    if ":" in line:
                        key, val = line.split(":", 1)
                        info[key.strip()] = val.strip()
                
                ssid = info.get("SSID", t["disconnected"])
                # Hem Türkçe hem İngilizce keyleri dene
                signal = info.get("Signal", info.get("Sinyal", "0%"))
                rate = info.get("Receive rate (Mbps)", info.get("Alım hızı (Mbps)", "0"))
                
                txt = f"📡 {ssid} | 🔋 {t['signal']}: {signal} | 🚀 {rate} Mbps"
                self.interface_label.configure(text=txt)
            else:
                self.interface_label.configure(text=t["disconnected"])
        except:
            self.interface_label.configure(text=t["disconnected"])

    def refresh_data(self):
        self.wifi_data = self.get_wifi_intel()
        self.get_active_interface_info()
        self.filter_results()

    def filter_results(self, event=None):
        query = self.search_entry.get().lower()
        self.filtered_data = [i for i in self.wifi_data if query in i['ssid'].lower() or query in i['password'].lower()]
        self.render_list()

    def render_list(self):
        for w in self.scroll_frame.winfo_children(): w.destroy()
        
        t = self.translations[self.language]
        self.scroll_frame.configure(label_text=f"{len(self.filtered_data)} {t['found_count']}")

        for i, item in enumerate(self.filtered_data):
            card = ctk.CTkFrame(self.scroll_frame, height=100)
            card.grid(row=i, column=0, sticky="ew", padx=10, pady=8)
            card.grid_columnconfigure(1, weight=1)

            # Icon/Avatar tasarımı
            icon_label = ctk.CTkLabel(card, text="◈", font=ctk.CTkFont(size=30), text_color="#3B8ED0")
            icon_label.grid(row=0, column=0, padx=20, rowspan=2)

            # Info
            ctk.CTkLabel(card, text=item['ssid'], font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=1, sticky="w", pady=(10,0))
            
            display_pass = "••••••••" if self.is_masked else item['password']
            pass_label = ctk.CTkLabel(card, text=f"{t['password']}: {display_pass}  |  {t['sec_type']}: {item['security']}", 
                                     font=ctk.CTkFont(size=12), text_color="gray")
            pass_label.grid(row=1, column=1, sticky="w", pady=(0,10))

            # Actions
            btn_box = ctk.CTkFrame(card, fg_color="transparent")
            btn_box.grid(row=0, column=2, rowspan=2, padx=15)

            ctk.CTkButton(btn_box, text=t['copy'], width=70, height=28, command=lambda p=item['password']: self.copy_to(p)).pack(side="left", padx=5)
            ctk.CTkButton(btn_box, text="QR", width=50, height=28, fg_color="#4B5563", command=lambda it=item: self.show_qr(it)).pack(side="left", padx=5)

    def copy_to(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        # Toast message representation
        self.show_toast("Copied to clipboard!")

    def show_toast(self, msg):
        toast = ctk.CTkToplevel(self)
        toast.overrideredirect(True)
        toast.geometry(f"200x40+{self.winfo_x()+500}+{self.winfo_y()+600}")
        lbl = ctk.CTkLabel(toast, text=msg)
        lbl.pack(expand=True)
        self.after(2000, toast.destroy)

    def show_qr(self, item):
        # Wi-Fi QR Format: WIFI:S:SSID;T:WPA;P:PASSWORD;;
        qr_data = f"WIFI:S:{item['ssid']};T:{item['security']};P:{item['password']};;"
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        qr_win = ctk.CTkToplevel(self)
        qr_win.title(f"QR: {item['ssid']}")
        qr_win.geometry("400x450")
        
        img_tk = ImageTk.PhotoImage(img)
        lbl = tk.Label(qr_win, image=img_tk, bg="white")
        lbl.image = img_tk
        lbl.pack(pady=20)
        
        ctk.CTkLabel(qr_win, text=item['ssid'], font=ctk.CTkFont(size=18, weight="bold")).pack()
        ctk.CTkButton(qr_win, text="Save QR", command=lambda: self.save_qr(img, item['ssid'])).pack(pady=10)

    def save_qr(self, img, name):
        path = filedialog.asksaveasfilename(defaultextension=".png", initialfile=f"WiFi_QR_{name}.png")
        if path:
            img.save(path)

    def toggle_mask(self):
        self.is_masked = not self.is_masked
        self.update_mask_button_text()
        self.render_list()

    def change_lang(self, choice):
        self.language = "tr" if choice == "Türkçe" else "en"
        self.update_translations()
        self.render_list()

    def update_translations(self):
        t = self.translations[self.language]
        # Titles & Sidebar
        self.title(t['title'])
        self.btn_refresh.configure(text=t['refresh'])
        self.update_mask_button_text()
        self.btn_export.set(t['export'])
        
        self.label_theme.configure(text=t['theme'] + ":")
        self.label_lang.configure(text=t['lang'] + ":")
        
        # Main Content
        self.search_entry.configure(placeholder_text=t['search'])
        self.get_active_interface_info() # Refresh interface text in correct language
        
        # Scrollable Frame Label
        self.scroll_frame.configure(label_text=t['found_count'])
        
    def update_mask_button_text(self):
        t = self.translations[self.language]
        self.btn_mask.configure(text=t['mask'] if not self.is_masked else t['unmask'])

    def export_data(self, mode):
        if not self.wifi_data: return
        file_type = "csv" if "CSV" in mode else "json"
        path = filedialog.asksaveasfilename(defaultextension=f".{file_type}")
        if not path: return
        
        if file_type == "json":
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.wifi_data, f, indent=4)
        else:
            keys = self.wifi_data[0].keys()
            with open(path, 'w', newline='', encoding='utf-8') as f:
                dict_writer = csv.DictWriter(f, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(self.wifi_data)
        
        messagebox.showinfo("Success", self.translations[self.language]["export_success"])

    def on_closing(self):
        """Uygulamayı sistem tepsisine küçültme."""
        try:
            self.withdraw()
            # Basit bir 64x64 mavi ikon oluştur (eğer dosya yoksa)
            icon_img = Image.new('RGB', (64, 64), color=(59, 142, 208))
            menu = (item('Show', self.show_app), item('Exit', self.exit_app))
            self.tray_icon = pystray.Icon("aura", icon_img, "Aura Wi-Fi", menu)
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
        except Exception as e:
            print(f"Tray error: {e}")
            self.destroy()
            os._exit(0)

    def show_app(self):
        self.tray_icon.stop()
        self.deiconify()

    def exit_app(self):
        self.tray_icon.stop()
        self.destroy()
        os._exit(0)

if __name__ == "__main__":
    # Yönetici kontrolü
    def is_admin():
        try: return ctypes.windll.shell32.IsUserAnAdmin()
        except: return False

    if platform.system() == "Windows" and not is_admin():
        # Kendini yönetici olarak yeniden başlat (Konsolsuz pythonw.exe tercih et)
        executable = sys.executable.replace("python.exe", "pythonw.exe")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, " ".join(sys.argv), None, 0)
    else:
        app = WiFiManagerApp()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
