import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp
import os


# =========================
# BACKEND
# =========================
def obter_info_video(url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    if "entries" in info:
        info = info["entries"][0]

    return info


def baixar(url, format_id, pasta, progress_cb, status_cb, is_mp3=False):
    def hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            if total:
                progress_cb(downloaded / total * 100)
        elif d["status"] == "finished":
            progress_cb(100)

    def run():
        try:
            status_cb("⬇️ Baixando...")

            ydl_opts = {
                "outtmpl": os.path.join(pasta, "%(title)s.%(ext)s"),
                "progress_hooks": [hook],
                "noplaylist": True,
                "merge_output_format": "mp4",
            }

            if is_mp3:
                ydl_opts.update({
                    "format": "bestaudio/best",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }]
                })
            else:
                ydl_opts["format"] = format_id

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            status_cb("✅ Download concluído!")
        except Exception as e:
            status_cb("❌ Erro")
            messagebox.showerror("Erro", str(e))

    threading.Thread(target=run, daemon=True).start()


# =========================
# GUI
# =========================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("640x460")

        self.style = ttk.Style()
        self.tema_atual = "clam"  # claro
        self.style.theme_use(self.tema_atual)

        self.video_info = None
        self.formatos = []
        self.destino = os.getcwd()

        self.build_ui()

    def alternar_tema(self):
        if self.tema_atual == "clam":
            self.tema_atual = "alt"   # escuro decente
            self.btn_tema.config(text="☀️")
        else:
            self.tema_atual = "clam"
            self.btn_tema.config(text="🌙")

        self.style.theme_use(self.tema_atual)

    def build_ui(self):
        # HEADER
        header = ttk.Frame(self.root)
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        ttk.Label(header, text="YouTube Downloader", font=("Segoe UI", 12, "bold"))\
            .grid(row=0, column=0, sticky="w")

        self.btn_tema = ttk.Button(header, text="🌙", width=3, command=self.alternar_tema)
        self.btn_tema.grid(row=0, column=1, sticky="e")

        header.columnconfigure(0, weight=1)

        # URL
        ttk.Label(self.root, text="URL do YouTube").grid(row=1, column=0, sticky="w", padx=10)
        self.url_entry = ttk.Entry(self.root)
        self.url_entry.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10)

        ttk.Button(self.root, text="🔍 Buscar", command=self.buscar)\
            .grid(row=2, column=3, padx=10)

        # INFO
        self.info_label = ttk.Label(self.root, text="", wraplength=600)
        self.info_label.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

        # FORMATO
        ttk.Label(self.root, text="Formato").grid(row=4, column=0, sticky="w", padx=10)
        self.combo = ttk.Combobox(self.root, state="readonly")
        self.combo.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10)

        self.var_mp3 = tk.BooleanVar()
        ttk.Checkbutton(self.root, text="🎵 Somente MP3", variable=self.var_mp3)\
            .grid(row=5, column=2, sticky="w")

        # DESTINO
        ttk.Label(self.root, text="Destino").grid(row=6, column=0, sticky="w", padx=10)
        self.destino_label = ttk.Label(self.root, text=self.destino)
        self.destino_label.grid(row=7, column=0, columnspan=3, sticky="w", padx=10)

        ttk.Button(self.root, text="📁 Escolher pasta", command=self.escolher_pasta)\
            .grid(row=7, column=3, padx=10)

        # PROGRESSO
        self.progress = ttk.Progressbar(self.root)
        self.progress.grid(row=8, column=0, columnspan=4, sticky="ew", padx=10, pady=15)

        # BAIXAR
        ttk.Button(self.root, text="⬇️ Baixar", command=self.baixar)\
            .grid(row=9, column=0, columnspan=4, pady=5)

        self.status = ttk.Label(self.root, text="")
        self.status.grid(row=10, column=0, columnspan=4)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

    # =========================
    # AÇÕES
    # =========================
    def buscar(self):
        try:
            url = self.url_entry.get().strip()
            if not url:
                return

            self.status.config(text="🔍 Buscando informações...")
            self.video_info = obter_info_video(url)

            self.info_label.config(
                text=f"🎬 {self.video_info['title']}\n"
                     f"📺 {self.video_info.get('uploader','')}\n"
                     f"⏱️ {self.video_info.get('duration_string','')}"
            )

            self.formatos.clear()
            resolucoes = []

            for f in self.video_info["formats"]:
                if f.get("vcodec") != "none" and f.get("acodec") != "none":
                    if f.get("resolution"):
                        self.formatos.append(f)
                        resolucoes.append(f["resolution"])

            self.combo["values"] = resolucoes
            if resolucoes:
                self.combo.current(0)

            self.status.config(text="✅ Pronto para download")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def escolher_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.destino = pasta
            self.destino_label.config(text=pasta)

    def baixar(self):
        if not self.video_info:
            return

        idx = self.combo.current()
        if idx < 0 and not self.var_mp3.get():
            return

        format_id = None if self.var_mp3.get() else self.formatos[idx]["format_id"]

        baixar(
            self.url_entry.get(),
            format_id,
            self.destino,
            lambda v: self.progress.config(value=v),
            lambda t: self.status.config(text=t),
            self.var_mp3.get()
        )


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
