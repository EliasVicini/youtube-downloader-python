import tkinter as tk
from tkinter import ttk, messagebox
import threading
import yt_dlp


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


def baixar_video(url, format_id, status_label):
    def run():
        try:
            status_label.config(text="⬇️ Baixando vídeo...")
            ydl_opts = {
                "format": format_id,
                "outtmpl": "%(title)s.%(ext)s",
                "merge_output_format": "mp4",
                "noplaylist": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            status_label.config(text="✅ Download concluído!")
        except Exception as e:
            status_label.config(text="❌ Erro no download")
            messagebox.showerror("Erro", str(e))

    threading.Thread(target=run, daemon=True).start()


class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("520x380")

        self.video_info = None
        self.formatos = []

        ttk.Label(root, text="URL do YouTube:").pack(anchor="w", padx=10, pady=5)
        self.url_entry = ttk.Entry(root)
        self.url_entry.pack(fill="x", padx=10)

        ttk.Button(root, text="🔍 Buscar vídeo", command=self.buscar_video).pack(pady=10)

        self.info_label = ttk.Label(root, text="", wraplength=480)
        self.info_label.pack(padx=10)

        ttk.Label(root, text="Qualidade:").pack(anchor="w", padx=10, pady=5)
        self.combo = ttk.Combobox(root, state="readonly")
        self.combo.pack(fill="x", padx=10)

        ttk.Button(root, text="⬇️ Baixar", command=self.baixar).pack(pady=10)

        self.status_label = ttk.Label(root, text="")
        self.status_label.pack(pady=10)

    def buscar_video(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Informe a URL do vídeo.")
            return

        try:
            self.status_label.config(text="🔍 Obtendo informações...")
            self.video_info = obter_info_video(url)

            titulo = self.video_info.get("title", "Desconhecido")
            canal = self.video_info.get("uploader", "Desconhecido")
            duracao = self.video_info.get("duration_string", "?")

            self.info_label.config(
                text=f"🎬 {titulo}\n📺 {canal}\n⏱️ {duracao}"
            )

            self.formatos.clear()
            opcoes = []

            for f in self.video_info.get("formats", []):
                if f.get("vcodec") != "none" and f.get("acodec") != "none":
                    if f.get("resolution"):
                        self.formatos.append(f)
                        opcoes.append(f["resolution"])

            self.combo["values"] = opcoes
            if opcoes:
                self.combo.current(0)

            self.status_label.config(text="✅ Vídeo carregado")
        except Exception as e:
            self.status_label.config(text="❌ Erro")
            messagebox.showerror("Erro", str(e))

    def baixar(self):
        if not self.video_info:
            messagebox.showwarning("Aviso", "Busque um vídeo primeiro.")
            return

        idx = self.combo.current()
        if idx < 0:
            messagebox.showwarning("Aviso", "Selecione uma qualidade.")
            return

        format_id = self.formatos[idx]["format_id"]
        url = self.url_entry.get().strip()

        baixar_video(url, format_id, self.status_label)


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()
