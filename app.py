from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from googletrans import Translator
import openai
import requests
import os
import tempfile

app = Flask(__name__)
translator = Translator()
openai.api_key = os.environ.get("OPENAI_API_KEY")

# ✅ Auto language detect & translate to English
def translate_text(text, dest_lang="en"):
    try:
        detected = translator.detect(text)
        if detected.lang == dest_lang:
            return text, detected.lang, "Already in target language"
        result = translator.translate(text, dest=dest_lang)
        return result.text, detected.lang, detected.lang
    except Exception as e:
        return text, "unknown", str(e)

# ✅ Voice message download & transcribe using Whisper
def transcribe_voice(media_url):
    try:
        # Twilio auth lagbe media download korte
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

        response = requests.get(media_url, auth=(account_sid, auth_token))

        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name

        with open(tmp_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)

        os.unlink(tmp_path)
        return transcript["text"]
    except Exception as e:
        return f"Voice transcribe error: {str(e)}"

# ✅ Main WhatsApp webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body", "").strip()
    media_url = request.form.get("MediaUrl0", None)
    media_type = request.form.get("MediaContentType0", "")

    resp = MessagingResponse()
    msg = resp.message()

    # 🎤 Voice message handle
    if media_url and "audio" in media_type:
        transcript = transcribe_voice(media_url)
        translated, src_lang, _ = translate_text(transcript)
        reply = (
            f"🎤 *Voice Transcript:*\n{transcript}\n\n"
            f"🌐 *Translated to English:*\n{translated}\n\n"
            f"📌 Detected Language: {src_lang.upper()}"
        )

    # 📝 Text message handle
    elif incoming_msg:
        # Special commands
        if incoming_msg.lower().startswith("translate to "):
            parts = incoming_msg.split(" ", 3)
            if len(parts) == 4:
                dest_lang = parts[2].lower()
                text_to_translate = parts[3]
                translated, src_lang, _ = translate_text(text_to_translate, dest_lang)
                reply = (
                    f"🌐 *Translation ({src_lang.upper()} → {dest_lang.upper()}):*\n{translated}"
                )
            else:
                reply = "⚠️ Format: `translate to [lang_code] [your text]`\nExample: `translate to bn Hello how are you`"

        elif incoming_msg.lower() == "help":
            reply = (
                "🤖 *W-Voice-AI Bot Help*\n\n"
                "📌 Commands:\n"
                "• Send any *text* → Auto detect & translate to English\n"
                "• Send *voice message* → Transcribe + Translate\n"
                "• `translate to [lang] [text]` → Translate to specific language\n\n"
                "🌍 Language codes:\n"
                "• bn = Bangla\n• en = English\n• hi = Hindi\n"
                "• ar = Arabic\n• fr = French\n• es = Spanish\n• zh-cn = Chinese"
            )

        else:
            # Auto translate to English
            translated, src_lang, _ = translate_text(incoming_msg)
            if src_lang == "en":
                reply = f"✅ Already in English:\n{incoming_msg}"
            else:
                reply = (
                    f"🌐 *Translation ({src_lang.upper()} → EN):*\n{translated}\n\n"
                    f"📝 Original: {incoming_msg}"
                )
    else:
        reply = "⚠️ Please send a text or voice message."

    msg.body(reply)
    return str(resp)

# ✅ Health check
@app.route("/", methods=["GET"])
def index():
    return "✅ W-Voice-AI Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
