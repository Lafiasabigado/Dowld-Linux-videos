import os
import yt_dlp
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
from datetime import datetime

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader Pro")
        self.root.geometry("700x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")
        
        self.downloads_history = []
        self.is_downloading = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#16213e", height=80)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="YouTube Downloader Pro",
            font=("Arial", 24, "bold"),
            bg="#16213e",
            fg="#00d9ff"
        )
        title_label.pack(pady=20)
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(padx=30, fill="both", expand=True)
        
        # URL Section
        url_label = tk.Label(
            main_frame,
            text="URL de la vidéo YouTube:",
            font=("Arial", 11, "bold"),
            bg="#1a1a2e",
            fg="#ffffff"
        )
        url_label.pack(anchor="w", pady=(0, 5))
        
        url_frame = tk.Frame(main_frame, bg="#1a1a2e")
        url_frame.pack(fill="x", pady=(0, 15))
        
        self.entry_url = tk.Entry(
            url_frame,
            font=("Arial", 11),
            bg="#0f3460",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat",
            borderwidth=2
        )
        self.entry_url.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        
        btn_info = tk.Button(
            url_frame,
            text="ℹInfo",
            font=("Arial", 10, "bold"),
            bg="#533483",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.get_video_info,
            padx=15,
            pady=5
        )
        btn_info.pack(side="right")
        
        # Video info section
        self.info_frame = tk.Frame(main_frame, bg="#0f3460", relief="flat", borderwidth=2)
        self.info_frame.pack(fill="x", pady=(0, 15))
        self.info_frame.pack_forget()  # Hidden by default
        
        self.info_text = tk.Label(
            self.info_frame,
            text="",
            font=("Arial", 9),
            bg="#0f3460",
            fg="#00d9ff",
            justify="left",
            anchor="w"
        )
        self.info_text.pack(padx=15, pady=10, fill="x")
        
        # Format Selection
        format_label = tk.Label(
            main_frame,
            text="Type de téléchargement:",
            font=("Arial", 11, "bold"),
            bg="#1a1a2e",
            fg="#ffffff"
        )
        format_label.pack(anchor="w", pady=(0, 5))
        
        self.format_var = tk.StringVar(value="video")
        
        format_frame = tk.Frame(main_frame, bg="#1a1a2e")
        format_frame.pack(fill="x", pady=(0, 15))
        
        radio_video = tk.Radiobutton(
            format_frame,
            text="Vidéo",
            variable=self.format_var,
            value="video",
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="#ffffff",
            selectcolor="#16213e",
            activebackground="#1a1a2e",
            activeforeground="#00d9ff",
            command=self.update_quality_options
        )
        radio_video.pack(side="left", padx=(0, 20))
        
        radio_audio = tk.Radiobutton(
            format_frame,
            text="Audio (MP3)",
            variable=self.format_var,
            value="audio",
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="#ffffff",
            selectcolor="#16213e",
            activebackground="#1a1a2e",
            activeforeground="#00d9ff",
            command=self.update_quality_options
        )
        radio_audio.pack(side="left")
        
        # Quality Selection
        quality_label = tk.Label(
            main_frame,
            text="Qualité:",
            font=("Arial", 11, "bold"),
            bg="#1a1a2e",
            fg="#ffffff"
        )
        quality_label.pack(anchor="w", pady=(0, 5))
        
        self.quality_var = tk.StringVar(value="best")
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "Custom.TCombobox",
            fieldbackground="#0f3460",
            background="#0f3460",
            foreground="#ffffff",
            arrowcolor="#00d9ff"
        )
        
        self.quality_combo = ttk.Combobox(
            main_frame,
            textvariable=self.quality_var,
            values=["Meilleure qualité", "1080p", "720p", "480p", "360p"],
            state="readonly",
            font=("Arial", 10),
            style="Custom.TCombobox"
        )
        self.quality_combo.pack(fill="x", ipady=5, pady=(0, 15))
        self.quality_combo.current(0)
        
        # Output folder
        folder_label = tk.Label(
            main_frame,
            text="Dossier de destination:",
            font=("Arial", 11, "bold"),
            bg="#1a1a2e",
            fg="#ffffff"
        )
        folder_label.pack(anchor="w", pady=(0, 5))
        
        folder_frame = tk.Frame(main_frame, bg="#1a1a2e")
        folder_frame.pack(fill="x", pady=(0, 20))
        
        self.folder_path = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        
        self.entry_folder = tk.Entry(
            folder_frame,
            textvariable=self.folder_path,
            font=("Arial", 10),
            bg="#0f3460",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat",
            state="readonly"
        )
        self.entry_folder.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 10))
        
        btn_browse = tk.Button(
            folder_frame,
            text="📁 Parcourir",
            font=("Arial", 10, "bold"),
            bg="#533483",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.browse_folder,
            padx=15,
            pady=5
        )
        btn_browse.pack(side="right")
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            length=640,
            mode='determinate',
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=(0, 10))
        
        style.configure(
            "Custom.Horizontal.TProgressbar",
            background="#00d9ff",
            troughcolor="#0f3460",
            bordercolor="#1a1a2e",
            lightcolor="#00d9ff",
            darkcolor="#00d9ff"
        )
        
        self.progress_label = tk.Label(
            main_frame,
            text="",
            font=("Arial", 9),
            bg="#1a1a2e",
            fg="#00d9ff"
        )
        self.progress_label.pack(pady=(0, 15))
        
        # Download button
        self.btn_download = tk.Button(
            main_frame,
            text="⬇TÉLÉCHARGER",
            font=("Arial", 14, "bold"),
            bg="#e94560",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            command=self.start_download,
            padx=30,
            pady=12
        )
        self.btn_download.pack(pady=(0, 15))
        
        # History section
        history_label = tk.Label(
            main_frame,
            text="📋 Historique:",
            font=("Arial", 10, "bold"),
            bg="#1a1a2e",
            fg="#ffffff"
        )
        history_label.pack(anchor="w", pady=(10, 5))
        
        history_frame = tk.Frame(main_frame, bg="#0f3460")
        history_frame.pack(fill="both", expand=True)
        
        self.history_text = tk.Text(
            history_frame,
            height=5,
            font=("Arial", 8),
            bg="#0f3460",
            fg="#ffffff",
            relief="flat",
            state="disabled"
        )
        self.history_text.pack(fill="both", expand=True, padx=2, pady=2)
        
    def update_quality_options(self):
        if self.format_var.get() == "audio":
            self.quality_combo['values'] = ["Haute qualité (320kbps)", "Moyenne (192kbps)", "Faible (128kbps)"]
            self.quality_combo.current(0)
        else:
            self.quality_combo['values'] = ["Meilleure qualité", "1080p", "720p", "480p", "360p"]
            self.quality_combo.current(0)
    
    def browse_folder(self):
        folder = filedialog.askdirectory(title="Choisir le dossier de destination")
        if folder:
            self.folder_path.set(folder)
    
    def get_video_info(self):
        url = self.entry_url.get().strip()
        if not url:
            messagebox.showwarning("Attention", "Veuillez entrer une URL YouTube.")
            return
        
        try:
            ydl_opts = {'quiet': True, 'no_warnings': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'N/A')
                duration = info.get('duration', 0)
                uploader = info.get('uploader', 'N/A')
                
                mins, secs = divmod(duration, 60)
                
                info_text = f"Titre: {title}\n👤 Créateur: {uploader}\n⏱️ Durée: {mins}:{secs:02d}"
                self.info_text.config(text=info_text)
                self.info_frame.pack(fill="x", pady=(0, 15))
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de récupérer les infos: {e}")
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                percent = d.get('_percent_str', '0%').strip()
                speed = d.get('_speed_str', 'N/A').strip()
                eta = d.get('_eta_str', 'N/A').strip()
                
                self.progress_label.config(
                    text=f"📊 {percent} | ⚡ {speed} | ⏳ ETA: {eta}"
                )
                
                # Update progress bar
                percent_num = float(percent.replace('%', ''))
                self.progress['value'] = percent_num
                
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_label.config(text="✅ Téléchargement terminé! Traitement en cours...")
            self.progress['value'] = 100
    
    def download_thread(self):
        url = self.entry_url.get().strip()
        output_path = self.folder_path.get()
        format_type = self.format_var.get()
        quality = self.quality_combo.get()
        
        if not url:
            messagebox.showwarning("Attention", "Veuillez entrer une URL YouTube.")
            self.is_downloading = False
            self.btn_download.config(state="normal", text="⬇TÉLÉCHARGER")
            return
        
        # Configure download options
        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'progress_hooks': [self.progress_hook],
        }
        
        if format_type == "audio":
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320' if 'Haute' in quality else '192' if 'Moyenne' in quality else '128',
            }]
        else:
            if quality == "Meilleure qualité":
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
            elif quality == "1080p":
                ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
            elif quality == "720p":
                ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
            elif quality == "480p":
                ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
            elif quality == "360p":
                ydl_opts['format'] = 'bestvideo[height<=360]+bestaudio/best[height<=360]'
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Vidéo')
                
            # Add to history
            timestamp = datetime.now().strftime("%H:%M:%S")
            history_entry = f"[{timestamp}] {title} ({format_type.upper()} - {quality})\n"
            self.downloads_history.append(history_entry)
            
            self.history_text.config(state="normal")
            self.history_text.insert("1.0", history_entry)
            self.history_text.config(state="disabled")
            
            messagebox.showinfo("Succès", f"Téléchargement terminé!\n\n📁 Fichier sauvegardé dans:\n{output_path}")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec du téléchargement:\n{str(e)}")
        
        finally:
            self.is_downloading = False
            self.btn_download.config(state="normal", text="⬇️ TÉLÉCHARGER", bg="#e94560")
            self.progress['value'] = 0
            self.progress_label.config(text="")
    
    def start_download(self):
        if self.is_downloading:
            messagebox.showinfo("Info", "Un téléchargement est déjà en cours!")
            return
        
        self.is_downloading = True
        self.btn_download.config(state="disabled", text="⏳ Téléchargement...", bg="#666")
        self.progress['value'] = 0
        
        # Start download in separate thread
        thread = threading.Thread(target=self.download_thread, daemon=True)
        thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()