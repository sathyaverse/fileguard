# 🛡️ FileGuard – Ultra 3D Cybersecurity Experience
### Suspicious File Type Detection & Holographic Laboratory

> **An advanced, immersive, cinematic 3D cybersecurity web application built with Python, Streamlit, and Three.js (WebGL).**  
> FileGuard protects users against disguised malicious payloads, deceptive double extensions, and file spoofing by analyzing true low-level file signatures (magic bytes) against declared extensions.

---

## 🌟 Key Features

- **Massive 3D Holographic Laboratory**:
  - Interactive 3D extruded crystal shield with central metallic padlock.
  - Orbiting cyan and violet neon energy containment rings.
  - Orbiting 3D floating file badges (`📄 PDF`, `⚙️ EXE`, `🖼️ IMG`, `</> CODE`).
  - Dynamic 1,100+ particle stardust field.
  - **Mouse-Responsive Parallax**: Smooth real-time 3D camera tracking reacting to cursor movement.
  - Built-in Canvas 3D fallback for 100% offline and cross-browser reliability.
- **3D Holographic Scanning Chamber**:
  - Real-time animated cyber-file prism with vertical laser scanning sweep.
  - Live 4-stage forensic inspection telemetry.
- **Dynamic 3D Result Holograms**:
  - 🟢 **Safe Format Match**: Glowing emerald shield with success aura.
  - 🔴 **Suspicious Mismatch**: Warning ruby shield with pulsing hazard core.
  - 🟠 **Unknown / Unsupported**: Amber alert shield for unverified byte signatures.
- **Deep Forensic Detection Engine**:
  - Magic byte header inspection covering 35+ formats (PE Executables, ELF, PDF, OOXML, legacy Office OLE, images, media, archives).
  - ZIP inner container inspection for true modern Office formats (`.docx`, `.xlsx`, `.pptx`).
  - **Double Extension Attack** detection (e.g., `payroll.docx.exe`).
  - **Unicode Right-to-Left Override (RLO / U+202E)** deceptive spoofing detection.
  - SHA-256 and MD5 cryptographic checksum calculation.
- **Multi-Format Export**:
  - Plain Text (`.txt`), Markdown (`.md`), and JSON (`.json`) audit reports.
- **Light Futuristic Glassmorphism Design**:
  - Electric blue, neon cyan, violet, and soft lavender cosmic palette.
  - High-contrast sidebar and telemetry dashboard.

---

## 📁 Project Structure

```text
FileGuard/
├── .streamlit/
│   └── config.toml        # Streamlit light theme & server configuration
├── app.py                 # Main Streamlit web application & multi-page navigation
├── detector.py            # Deep binary signature detection & spoofing engine
├── report.py              # Multi-format forensic audit report generator (TXT, MD, JSON)
├── three_hero.py          # Interactive Three.js WebGL 3D engine & Canvas fallback
├── styles.css             # Light glassmorphism CSS & animation stylesheet
├── requirements.txt       # Production dependencies (streamlit, pillow)
├── .gitignore             # Git ignore patterns
└── README.md              # Project documentation & deployment guide
```

---

## 🚀 Local Installation & Run

### 1. Clone Repository & Navigate
```bash
git clone https://github.com/<your-username>/fileguard.git
cd fileguard
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Web Application
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## ☁️ Deploy to GitHub & Streamlit Community Cloud (Free)

### Step 1: Push to GitHub
1. Create a new repository named `fileguard` on [GitHub](https://github.com/new).
2. Run the following commands in your terminal:
```bash
git remote add origin https://github.com/<your-username>/fileguard.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
2. Click **"New app"**.
3. Select your repository: `<your-username>/fileguard`.
4. Branch: `main`.
5. Main file path: `app.py`.
6. Click **"Deploy!"**.
Your 3D cybersecurity app will be live on a public URL (e.g. `https://fileguard.streamlit.app`)!

---

## 🔒 Security Disclaimer
Format verification confirms whether a file's declared extension aligns with its internal header signature. A matching format does not guarantee the file is free of embedded malicious macros, exploits, or payload scripts. Use FileGuard alongside robust endpoint antivirus solutions.
