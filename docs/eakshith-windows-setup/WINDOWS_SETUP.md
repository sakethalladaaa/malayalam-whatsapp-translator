# EAKSHITH — WINDOWS DEVELOPMENT SETUP

This guide is for setting up the Malayalam WhatsApp Translator project on Windows.

## 1. Clone the Repository

Open PowerShell and run:

```powershell
git clone https://github.com/sakethalladaaa/malayalam-whatsapp-translator.git
cd malayalam-whatsapp-translator
```

## 2. Check Python

```powershell
py --version
```

Required: Python 3.11 or newer.

## 3. Create Virtual Environment

```powershell
py -3.11 -m venv .venv
```

## 4. Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

## 5. Install Backend Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn
```

## 6. Start the Backend

```powershell
python -m uvicorn backend.app.main:app --reload
```

Backend: http://127.0.0.1:8000

## 7. Test the Backend

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected response: `status: ok`

## 8. Load the Chrome Extension

Open `chrome://extensions` in Google Chrome.

1. Enable Developer mode.
2. Click Load unpacked.
3. Select the project `extension` folder.

## 9. Project Stack

- Chrome Extension — Manifest V3
- JavaScript
- HTML/CSS
- Python 3.11+
- FastAPI
- Uvicorn
- AI4Bharat IndicLID
- AI4Bharat IndicXlit
- AI4Bharat IndicTrans2

## 10. Git Workflow

Create a feature branch instead of working directly on main:

```powershell
git checkout -b eakshith/extension-ui
```

Then commit and push:

```powershell
git status
git add .
git commit -m "feat: improve extension UI"
git push -u origin eakshith/extension-ui
```
