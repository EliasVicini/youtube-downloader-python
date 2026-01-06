# 🎬 YouTube Downloader (Python)

Script em Python para baixar vídeos do YouTube com seleção de qualidade.
Compatível com Windows e Linux, utilizando ambiente virtual (`venv`).

---

## 📋 Requisitos

- Python 3.9 ou superior
- Internet
- FFmpeg (recomendado para melhor compatibilidade)

---

## 🔧 Instalação do FFmpeg (opcional, mas recomendado)

### Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install ffmpeg
```

### Windows

Baixe em: https://ffmpeg.org/download.html

Extraia e adicione o caminho bin ao PATH

Teste: ffmpeg -version


### Criando o ambiente virtual (venv)
Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```
---

Windows (PowerShell)
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

Se houver erro de política de execução:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 📦 Instalando dependências
```bash
pip install -r requirements.txt
```

### ▶️ Executando o programa
```bash
python youtube_downloader.py  // Via Terminal
```
```bash
python youtube_gui.py  // Via Interface Gráfica
```

O programa irá:

    Solicitar a URL do YouTube

    Mostrar as resoluções disponíveis

    Baixar o vídeo na qualidade escolhida

📂 Onde o vídeo é salvo?

    ✔️ Na mesma pasta onde o script está sendo executado
    ✔️ Com o nome original do vídeo