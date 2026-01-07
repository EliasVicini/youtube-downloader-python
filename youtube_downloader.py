import yt_dlp
import sys


# =========================
# OBTÉM INFO DO VÍDEO
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


# =========================
# BAIXA VÍDEO
# =========================
def baixar_video(url, format_id):
    ydl_opts = {
        "format": format_id,
        "outtmpl": "%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "noplaylist": True,

        # 🔽 MELHORES CONFIGURAÇÕES
        "quiet": False,
        "no_warnings": True,
        "progress_with_newline": False,

        # 👇 evita problemas futuros com YouTube
        # requer node instalado
        # "js_runtimes": ["node"],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


# =========================
# MAIN
# =========================
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
                filesize = f.get("filesize") or f.get("filesize_approx")

                formatos.append({
                    "format_id": f["format_id"],
                    "resolution": f["resolution"],
                    "filesize": filesize,
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
    print("0 - ❌ Sair do programa")

    for i, f in enumerate(formatos, start=1):
        if f["filesize"]:
            tamanho = f"{f['filesize'] / (1024 * 1024):.1f} MB"
        else:
            tamanho = "streaming (tamanho variável)"

        print(f"{i} - 🎬 {f['resolution']} ({tamanho})")

    escolha = input("\nDigite o número da qualidade desejada: ").strip()

    if escolha == "0":
        print("\n👋 Programa finalizado pelo usuário.")
        sys.exit(0)

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
