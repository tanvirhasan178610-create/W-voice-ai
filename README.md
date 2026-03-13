# 🤖 W-Voice-AI — WhatsApp Voice & Text Translator Bot

## ✅ Features
- 🎤 Voice message → Text (Transcription)
- 🌐 Auto language detect & translate to English
- 📝 Text translate to any language
- 💬 WhatsApp integration via Twilio

---

## 🚀 Setup Guide

### Step 1: Accounts kholo
1. **Twilio**: https://twilio.com → Free account → WhatsApp Sandbox activate koro
2. **OpenAI**: https://platform.openai.com → API key nao

### Step 2: Install packages
```bash
pip install -r requirements.txt
```

### Step 3: .env file banao
```bash
cp .env.example .env
# .env file e tomar API keys bosao
```

### Step 4: Run koro locally
```bash
python app.py
```

### Step 5: Twilio Webhook set koro
- ngrok diye tunnel: `ngrok http 5000`
- Twilio Console → WhatsApp Sandbox → Webhook URL: `https://your-ngrok-url/webhook`

---

## 🌍 Bot Commands (WhatsApp e pathao)

| Command | Result |
|---------|--------|
| Any text | Auto detect & translate to English |
| `translate to bn Hello` | Translate to Bangla |
| `translate to hi Good morning` | Translate to Hindi |
| Voice message | Transcribe + translate |
| `help` | Show all commands |

---

## 📦 Deploy (Free)
- **Render.com** — Free hosting, GitHub connect koro
- **Railway.app** — Easy deploy

---

## 🔑 Language Codes
`bn`=Bangla, `en`=English, `hi`=Hindi, `ar`=Arabic, `fr`=French, `es`=Spanish, `zh-cn`=Chinese, `ru`=Russian, `ja`=Japanese
