from Scrapper import get_car_data, save_to_csv
import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading, re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG    = "#0a0e1a"
PANEL = "#0f1628"
CARD  = "#131929"
ACC   = "#00d4aa"
TEXT  = "#e2e8f0"
DIM   = "#4a5568"
GREEN = "#00c896"
RED   = "#ff6b6b"
CARS  = ["honda", "toyota", "suzuki", "kia", "hyundai", "mg", "changan"]
current_data = []

def clean_price(p):
    m = re.search(r'PKR[\s]?[\d,]+', p)
    return m.group(0).strip() if m else p.split("Get")[0].strip()

def fetch():
    status.configure(text="⏳  Fetching...", text_color=ACC)
    out.configure(state="normal"); out.delete("1.0", "end"); out.configure(state="disabled")
    def work():
        try:
            data = get_car_data(dropdown.get())
            root.after(0, lambda: show(data))
        except Exception as ex:
            root.after(0, lambda: status.configure(text=f"✗  {ex}", text_color=RED))
    threading.Thread(target=work, daemon=True).start()

def show(data):
    global current_data
    current_data = data
    out.configure(state="normal"); out.delete("1.0", "end")
    if data:
        out.insert("end", "\n")
        out.insert("end", f"    {'MODEL / VARIANT':<54}{'PRICE':>22}\n")
        out.insert("end", "    " + "─"*74 + "\n\n")
        for i, d in enumerate(data):
            name  = d['name'].strip()
            price = clean_price(d['price'])
            if name.lower() in ("car version", "model", "variant", ""):
                continue
            out.insert("end", f"    {name:<54}{price:>22}\n\n")
        status.configure(text=f"✓  {len(data)} results for {dropdown.get().title()}", text_color=GREEN)
        save_btn.configure(fg_color=GREEN, text_color="#000", hover_color="#00a87a")
    else:
        out.insert("end", "\n\n    No data found.")
        status.configure(text="No data found.", text_color=ACC)
    out.configure(state="disabled")

def clear():
    global current_data; current_data = []
    out.configure(state="normal"); out.delete("1.0", "end"); out.configure(state="disabled")
    status.configure(text="Ready", text_color=DIM)
    save_btn.configure(fg_color="#1a2a22", text_color=DIM, hover_color="#1a2a22")

def save():
    if not current_data:
        return messagebox.showwarning("No Data", "Search for a brand first.")
    path = filedialog.asksaveasfilename(
        defaultextension=".csv", initialfile=f"{dropdown.get()}_prices.csv",
        filetypes=[("CSV files", "*.csv")])
    if path:
        save_to_csv(current_data, path)
        status.configure(text=f"✓  Saved → {path.split('/')[-1]}", text_color=GREEN)

# ── Window ─────────────────────────────────────────────────────────────────
root = ctk.CTk()
root.title("PakWheels Price Tracker")
root.geometry("920x680")
root.configure(fg_color=BG)

# Header
hdr = ctk.CTkFrame(root, fg_color=PANEL, corner_radius=0)
hdr.pack(fill="x")
ctk.CTkLabel(hdr, text="◈  PakWheels Price Tracker",
             font=ctk.CTkFont("Segoe UI", 20, "bold"),
             text_color=ACC).pack(side="left", padx=24, pady=18)

# Divider
ctk.CTkFrame(root, fg_color=ACC, height=2, corner_radius=0).pack(fill="x")

# Controls
ctrl = ctk.CTkFrame(root, fg_color=BG, corner_radius=0)
ctrl.pack(fill="x", padx=24, pady=20)

ctk.CTkLabel(ctrl, text="Brand", font=ctk.CTkFont("Segoe UI", 11, "bold"),
             text_color=ACC).pack(side="left", padx=(0, 10))

dropdown = ctk.CTkComboBox(ctrl, values=CARS, width=180,
                           font=ctk.CTkFont("Segoe UI", 12, "bold"),
                           fg_color="#1e2d4a", border_color=ACC,
                           button_color=ACC, button_hover_color=ACC,
                           dropdown_fg_color="#131929",
                           dropdown_hover_color=ACC,
                           dropdown_text_color=TEXT,
                           text_color=TEXT, border_width=2,
                           state="readonly")
dropdown.set(CARS[0])
dropdown.pack(side="left", padx=(0, 16))

ctk.CTkButton(ctrl, text="🔍  Search", command=fetch, width=130, height=40,
              fg_color=ACC, hover_color="#00ffcc", text_color="#000",
              font=ctk.CTkFont("Segoe UI", 11, "bold"),
              corner_radius=8).pack(side="left", padx=(0, 10))

ctk.CTkButton(ctrl, text="✕  Clear", command=clear, width=100, height=40,
              fg_color="#1a2035", hover_color="#2a3050", text_color=TEXT,
              font=ctk.CTkFont("Segoe UI", 11, "bold"),
              corner_radius=8).pack(side="left")

# Results
out = ctk.CTkTextbox(root, fg_color=CARD, text_color="#c8d8f0",
                     font=ctk.CTkFont("Consolas", 10),
                     corner_radius=10, border_width=1, border_color="#1e2d4a",
                     scrollbar_button_color="#1e2d4a",
                     scrollbar_button_hover_color=ACC,
                     wrap="none", state="disabled")
out.pack(fill="both", expand=True, padx=24, pady=(0, 10))

# Footer
foot = ctk.CTkFrame(root, fg_color=PANEL, corner_radius=0, height=54)
foot.pack(fill="x"); foot.pack_propagate(False)

status = ctk.CTkLabel(foot, text="Ready",
                      font=ctk.CTkFont("Segoe UI", 10, slant="italic"),
                      text_color=DIM)
status.pack(side="left", padx=18)

ctk.CTkLabel(foot, text="pakwheels.com",
             font=ctk.CTkFont("Segoe UI", 9), text_color=DIM).pack(side="right", padx=14)

save_btn = ctk.CTkButton(foot, text="💾  Export CSV", command=save,
                         width=140, height=36,
                         fg_color="#1a2a22", hover_color="#1a2a22",
                         text_color=DIM,
                         font=ctk.CTkFont("Segoe UI", 10, "bold"),
                         corner_radius=8)
save_btn.pack(side="right", padx=12, pady=9)

root.mainloop()