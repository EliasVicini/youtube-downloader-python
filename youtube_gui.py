import threading
import yt_dlp
import os
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox


# =========================
# BACKEND
# =========================
def obter_info_video(url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
        "no_warnings": True,
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
            baixado = d.get("downloaded_bytes", 0)
            if total:
                progress_cb(baixado / total * 100)
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
                "quiet": True,
                "no_warnings": True,
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
        self.video_info = None
        self.formatos = []
        self.destino = os.getcwd()
        self.temas = {
            "🌙 Darkly": "darkly",
            "🦇 Superhero": "superhero",
            "🤖 Cyborg": "cyborg",
            "☀️ Flatly": "flatly",
            "📄 Litera": "litera",
        }


        self.build_ui()

    def trocar_tema(self, event=None):
        tema_visivel = self.theme_var.get()
        tema_real = self.temas.get(tema_visivel)

        if tema_real:
            self.root.style.theme_use(tema_real)

    def build_ui(self):
        # HEADER
        # HEADER
        header = tb.Frame(self.root)
        header.pack(fill=X, padx=15, pady=10)

        tb.Label(
            header,
            text="YouTube Downloader",
            font=("Segoe UI", 14, "bold")
        ).pack(side=LEFT)

        # 🌈 Seletor de tema (canto direito)
        self.theme_var = tb.StringVar(value="🌙 Darkly")

        self.theme_combo = tb.Combobox(
            header,
            textvariable=self.theme_var,
            values=list(self.temas.keys()),
            width=14,
            state="readonly"
        )
        self.theme_combo.pack(side=RIGHT)
        self.theme_combo.bind("<<ComboboxSelected>>", self.trocar_tema)


        # URL
        tb.Label(self.root, text="URL do YouTube").pack(anchor=W, padx=15)
        self.url_entry = tb.Entry(self.root)
        self.url_entry.pack(fill=X, padx=15)

        tb.Button(
            self.root,
            text="🔍 Buscar",
            bootstyle=PRIMARY,
            command=self.buscar
        ).pack(padx=15, pady=5)

        # INFO
        self.info_label = tb.Label(self.root, wraplength=580)
        self.info_label.pack(padx=15, pady=10)

        # FORMATO
        form = tb.Frame(self.root)
        form.pack(fill=X, padx=15)

        self.combo = tb.Combobox(form, state="readonly")
        self.combo.pack(side=LEFT, fill=X, expand=True)

        self.var_mp3 = tb.BooleanVar()
        tb.Checkbutton(
            form,
            text="🎵 Somente MP3",
            variable=self.var_mp3,
            bootstyle=SUCCESS
        ).pack(side=LEFT, padx=10)

        # DESTINO
        dest = tb.Frame(self.root)
        dest.pack(fill=X, padx=15, pady=5)

        self.destino_label = tb.Label(dest, text=self.destino)
        self.destino_label.pack(side=LEFT, fill=X, expand=True)

        tb.Button(
            dest,
            text="📁",
            bootstyle=SECONDARY,
            command=self.escolher_pasta
        ).pack(side=RIGHT)

        # PROGRESSO
        self.progress = tb.Progressbar(
            self.root,
            bootstyle=INFO,
            maximum=100
        )
        self.progress.pack(fill=X, padx=15, pady=15)

        # BAIXAR
        tb.Button(
            self.root,
            text="⬇️ Baixar",
            bootstyle=SUCCESS,
            command=self.baixar
        ).pack(padx=15, pady=5)

        self.status = tb.Label(self.root)
        self.status.pack(pady=5)

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
    app = tb.Window(
        title="YouTube Downloader",
        themename="darkly",  # 🔥 dark mode REAL
        size=(640, 520),
        resizable=(False, False)
    )
    App(app)
    app.mainloop()
