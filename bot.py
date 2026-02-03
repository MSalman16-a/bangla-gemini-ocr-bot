import os
import tempfile
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters
)

from pdf_utils import pdf_to_images
from gemini_engine import run_gemini
from formats import make_txt, make_csv, make_json
import prompts

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send PDF with /pdfm, /pdfe or /pdfc")

async def pdfm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_sessions[update.effective_user.id] = {"mode": "ask"}
    await update.message.reply_text(
        "Choose:\n1️⃣ Extract existing MCQs\n2️⃣ Generate new MCQs\nReply 1 or 2"
    )

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in user_sessions:
        return

    if update.message.text not in ["1","2"]:
        return

    user_sessions[uid]["choice"] = update.message.text
    await update.message.reply_text("Now send the PDF.")

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    doc = update.message.document

    with tempfile.TemporaryDirectory() as tmp:
        pdf_path = f"{tmp}/input.pdf"
        await doc.get_file().download_to_drive(pdf_path)

        images = pdf_to_images(pdf_path)

        if user_sessions.get(uid, {}).get("choice") == "1":
            prompt = prompts.EXTRACT_PROMPT
        else:
            prompt = prompts.GENERATE_PROMPT

        mcqs = run_gemini(GEMINI_API_KEY, images, prompt)

        txt = make_txt(mcqs)
        csvf = make_csv(mcqs)
        jsonf = make_json(mcqs)

        await update.message.reply_document(open(csvf,"rb"))
        await update.message.reply_document(open(jsonf,"rb"))

        if len(txt) < 3500:
            await update.message.reply_text(txt)
        else:
            with open(f"{tmp}/quiz.txt","w",encoding="utf-8") as f:
                f.write(txt)
            await update.message.reply_document(open(f"{tmp}/quiz.txt","rb"))

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pdfm", pdfm))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
    app.run_polling()

if __name__ == "__main__":
    main()
