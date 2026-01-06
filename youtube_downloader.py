import yt_dlp
import sys


def listar_formatos(url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,  # 🔴 ESSENCIAL
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # Se mesmo assim vier playlist, pega só o primeiro vídeo
    if "entries" in info:
        info = info["entries"][0]

    formats = info.get("formats", [])
    videos = []

    for f in formats:
        if f.get("vcodec") != "none" and f.get("acodec") != "none":
            if f.get("resolution"):
                videos.append({
                    "format_id": f["format_id"],
                    "resolution": f["resolution"],
                    "filesize": f.get("filesize"),
                })

    # remove resoluções duplicadas
    unicos = {}
    for v in videos:
        unicos[v["resolution"]] = v

    return list(unicos.values())



def baixar_video(url, format_id):
    ydl_opts = {
        "format": format_id,
        "outtmpl": "%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "noplaylist": True,  # 🔴 ESSENCIAL
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def obter_info_video(url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # Se vier playlist por acidente, pega o primeiro vídeo
    if "entries" in info:
        info = info["entries"][0]

    return info

def main():
    url = input("Cole a URL do YouTube: ").strip()

    print("\n🔍 Obtendo informações do vídeo...\n")
    info = obter_info_video(url)

    titulo = info.get("title", "Título desconhecido")
    canal = info.get("uploader", "Canal desconhecido")
    duracao = info.get("duration_string", "Duração desconhecida")

    print("📌 Vídeo encontrado:")
    print(f"🎬 Título : {titulo}")
    print(f"📺 Canal  : {canal}")
    print(f"⏱️ Duração: {duracao}\n")

    formatos = []

    for f in info.get("formats", []):
        if f.get("vcodec") != "none" and f.get("acodec") != "none":
            if f.get("resolution"):
                formatos.append({
                    "format_id": f["format_id"],
                    "resolution": f["resolution"],
                    "filesize": f.get("filesize"),
                })

    # remove resoluções duplicadas
    unicos = {}
    for f in formatos:
        unicos[f["resolution"]] = f

    formatos = list(unicos.values())

    if not formatos:
        print("❌ Nenhuma qualidade compatível encontrada.")
        return

    print("Qualidades disponíveis:\n")
    for i, f in enumerate(formatos, start=1):
        tamanho = (
            f"{f['filesize'] / (1024 * 1024):.1f} MB"
            if f["filesize"] else "tamanho desconhecido"
        )
        print(f"{i} - 🎬 {f['resolution']} ({tamanho})")

    escolha = input("\nDigite o número da qualidade desejada: ").strip()

    try:
        index = int(escolha) - 1
        formato = formatos[index]
    except (ValueError, IndexError):
        print("❌ Opção inválida.")
        return

    print(f"\n⬇️ Baixando: {titulo}")
    print(f"📥 Qualidade: {formato['resolution']}\n")

    baixar_video(url, formato["format_id"])

    print("\n✅ Download concluído!")

if __name__ == "__main__":
    main()
