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

1. Baixe em: https://ffmpeg.org/download.html

2. Extraia o arquivo `.zip`
3. Copie a pasta para `C:\ffmpeg\`
4. Adicione `C:\ffmpeg\bin` ao PATH do sistema
5. Pressione Win + R 
6. Digite: sysdm.cpl
7. Vá em Avançado / Clique em Variáveis de Ambiente / Em Variáveis do sistema, selecione Path / Clique em Editar / Clique em Novo
8. Cole --> C:\ffmpeg\bin
9. Feche todos os terminais
10. Abra um novo terminal e execute: ffmpeg -version

---

### Criando o ambiente virtual (venv)
Linux / macOS
```bash
cd /caminho_do_projeto/
python3 -m venv venv
source venv/bin/activate
```
---

Windows (PowerShell)
```bash
cd /caminho_do_projeto/
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
Via Terminal
```bash
python youtube_downloader.py
```
Via Interface Gráfica
```bash
python youtube_gui.py
```

---

## O programa irá:

    Solicitar a URL do YouTube

    Mostrar as resoluções disponíveis

    Baixar o vídeo na qualidade escolhida

📂 Onde o vídeo é salvo?

    ✔️ Na mesma pasta onde o script está sendo executado ou em uma pasta da sua escolha


### ⚠️ Aviso legal

    Este projeto é apenas para fins educacionais.
    Respeite os termos de uso do YouTube e a legislação vigente.