import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import os
import subprocess
from file_manager import FileManager

class FileSorterGUI:
    def __init__(self):
        self.manager = FileManager()
        self.root = tk.Tk()
        self.root.title("Fájlrendező – Forrás és Cél tallózás")
        self.root.geometry("680x300")
        self.root.resizable(False, False)

        self.last_log_path = None  # ÚJ: Az utolsó log fájl helye

        # Forrás mappa
        frm_src = tk.Frame(self.root)
        frm_src.pack(pady=(12,6), padx=12, fill="x")
        tk.Label(frm_src, text="Forrás mappa:").grid(row=0, column=0, sticky="w")
        self.src_entry = tk.Entry(frm_src, width=54)
        self.src_entry.grid(row=1, column=0, sticky="w")
        tk.Button(frm_src, text="Tallózás", command=self.browse_source).grid(row=1, column=1, padx=(8,0))

        # Cél mappa
        frm_dst = tk.Frame(self.root)
        frm_dst.pack(pady=(6,6), padx=12, fill="x")
        tk.Label(frm_dst, text="Cél mappa (ide jön létre a fájlokkal az almappa):").grid(row=0, column=0, sticky="w")
        self.dst_entry = tk.Entry(frm_dst, width=54)
        self.dst_entry.grid(row=1, column=0, sticky="w")
        tk.Button(frm_dst, text="Tallózás", command=self.browse_target).grid(row=1, column=1, padx=(8,0))

        # Kiterjesztés + gombok
        frm_ctrl = tk.Frame(self.root)
        frm_ctrl.pack(pady=(6,12))
        tk.Label(frm_ctrl, text="Kiterjesztés (pl. xlsx, docx, pdf, stb.):").grid(row=0, column=0, padx=(0,8))
        self.ext_entry = tk.Entry(frm_ctrl, width=20)
        self.ext_entry.grid(row=0, column=1)

        self.btn_sort = tk.Button(frm_ctrl, text="Rendezés", width=12, command=self.start_sort_thread)
        self.btn_sort.grid(row=0, column=2, padx=(12,6))

        # ÚJ: Log megnyitása gomb
        self.btn_open_log = tk.Button(frm_ctrl, text="Log megnyitása", width=14,
                                      state="disabled", command=self.open_last_log)
        self.btn_open_log.grid(row=0, column=3, padx=(6,8))

        # Kilépés gomb
        self.btn_exit = tk.Button(frm_ctrl, text="Kilépés", width=12, command=self.root.destroy)
        self.btn_exit.grid(row=0, column=4)

        # Status sor
        self.status_var = tk.StringVar(value="Készen áll.")
        self.status_label = tk.Label(self.root, textvariable=self.status_var, anchor="w", justify="left")
        self.status_label.pack(fill="x", padx=12, pady=(4,0))

    # ---- Tallózások ----
    def browse_source(self):
        folder = filedialog.askdirectory(title="Forrás mappa")
        if folder:
            self.src_entry.delete(0, tk.END)
            self.src_entry.insert(0, folder)

    def browse_target(self):
        folder = filedialog.askdirectory(title="Cél mappa")
        if folder:
            self.dst_entry.delete(0, tk.END)
            self.dst_entry.insert(0, folder)

    # ---- Log megnyitása ----
    def open_last_log(self):
        if self.last_log_path and os.path.exists(self.last_log_path):
            try:
                os.startfile(self.last_log_path)  # Windows Notepad
            except Exception:
                messagebox.showerror("Hiba", "Nem sikerült megnyitni a log fájlt.")
        else:
            messagebox.showwarning("Nincs log", "Még nem készült log fájl.")

    # ---- Indítás külön szálon ----
    def start_sort_thread(self):
        src = self.src_entry.get().strip()
        dst = self.dst_entry.get().strip()
        ext = self.ext_entry.get().strip().lstrip('.').lower()

        if not src or not dst or not ext:
            messagebox.showerror("Hiba", "Minden mezőt ki kell tölteni!")
            return

        if not os.path.isdir(src):
            messagebox.showerror("Hiba", "A forrás mappa nem létezik!")
            return

        if not os.path.isdir(dst):
            messagebox.showerror("Hiba", "A cél mappa nem létezik!")
            return

        self.btn_sort.config(state="disabled")
        self.btn_exit.config(state="disabled")
        self.btn_open_log.config(state="disabled")
        self.status_var.set("Feldolgozás...")

        t = threading.Thread(target=self._run_sort, args=(src, dst, ext), daemon=True)
        t.start()

    # ---- A tényleges futás külön szálon ----
    def _run_sort(self, src, dst, ext):
        try:
            moved_count, log_path = self.manager.sort_by_extension(ext=ext, src_dir=src, target_root=dst)

            self.last_log_path = log_path  # ÚJ: eltároljuk a logot
            self.btn_open_log.config(state="normal")  # Aktiváljuk a gombot

            self.status_var.set(f"Kész: {moved_count} fájl áthelyezve. Log: {log_path}")
            messagebox.showinfo("Kész", f"{moved_count} fájl áthelyezve.\n\nLog fájl:\n{log_path}")

        except Exception as e:
            self.status_var.set("Hiba történt.")
            messagebox.showerror("Hiba", f"Hiba történt:\n{e}")

        finally:
            self.btn_sort.config(state="normal")
            self.btn_exit.config(state="normal")

    def run(self):
        try:
            self.root.lift()
            self.root.attributes("-topmost", True)
            self.root.after(200, lambda: self.root.attributes('-topmost', False))
        except:
            pass

        self.root.mainloop()
