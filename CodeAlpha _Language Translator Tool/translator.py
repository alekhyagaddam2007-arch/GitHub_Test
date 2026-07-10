import customtkinter as ctk
from deep_translator import GoogleTranslator
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
from tkinter import filedialog
import threading
import os


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


app = ctk.CTk()
app.title("AI Language Translator")
app.geometry("900x650")
app.resizable(False, False)


languages = [
    "english","hindi","telugu","tamil","kannada",
    "malayalam","french","german","spanish",
    "italian","japanese","korean",
    "arabic","urdu","chinese"
]


lang_code = {
    "english":"en",
    "hindi":"hi",
    "telugu":"te",
    "tamil":"ta",
    "kannada":"kn",
    "malayalam":"ml",
    "french":"fr",
    "german":"de",
    "spanish":"es",
    "italian":"it",
    "japanese":"ja",
    "korean":"ko",
    "arabic":"ar",
    "urdu":"ur",
    "chinese":"zh-CN"
}



def translate():

    text = source_text.get("1.0","end").strip()

    if not text:
        status.configure(text="Enter text first")
        return

    try:

        result = GoogleTranslator(
            source="auto",
            target=lang_code[language.get()]
        ).translate(text)


        translated_text.delete(
            "1.0",
            "end"
        )

        translated_text.insert(
            "end",
            result
        )

        status.configure(
            text="Translation Successful ✅"
        )

    except Exception as e:

        status.configure(
            text="Translation Error"
        )



def speak():

    text = translated_text.get(
        "1.0",
        "end"
    ).strip()


    if not text:
        return


    try:

        code = lang_code.get(
            language.get(),
            "en"
        )

        tts = gTTS(
            text=text,
            lang=code
        )

        file="voice.mp3"

        tts.save(file)

        playsound(file)

        os.remove(file)

    except:

        status.configure(
            text="Speech Error"
        )



def listen():

    recognizer = sr.Recognizer()


    try:

        with sr.Microphone() as source:

            status.configure(
                text="Listening 🎤"
            )

            app.update()

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=5
            )


        text = recognizer.recognize_google(
            audio
        )


        source_text.delete(
            "1.0",
            "end"
        )


        source_text.insert(
            "end",
            text
        )


        status.configure(
            text="Voice Captured ✅"
        )


    except:

        status.configure(
            text="Voice not detected"
        )



def start_voice():

    threading.Thread(
        target=listen,
        daemon=True
    ).start()



def copy_text():

    app.clipboard_clear()

    app.clipboard_append(
        translated_text.get(
            "1.0",
            "end"
        )
    )

    status.configure(
        text="Copied ✅"
    )



def clear():

    source_text.delete(
        "1.0",
        "end"
    )

    translated_text.delete(
        "1.0",
        "end"
    )

    status.configure(
        text="Cleared"
    )



def download():

    text = translated_text.get(
        "1.0",
        "end"
    ).strip()


    if not text:

        status.configure(
            text="Nothing to download"
        )

        return


    file = filedialog.asksaveasfilename(
        title="Download Translation",
        defaultextension=".txt",
        filetypes=[
            ("Text File","*.txt")
        ]
    )


    if file:

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(text)


        status.configure(
            text="Downloaded Successfully ⬇"
        )
        # ---------------- UI ----------------


heading = ctk.CTkLabel(
    app,
    text="🌍 AI Language Translator",
    font=("Segoe UI",30,"bold"),
    text_color="#A855F7"
)

heading.pack(pady=20)



ctk.CTkLabel(
    app,
    text="Enter Text",
    font=("Segoe UI",16,"bold")
).pack(
    anchor="w",
    padx=30
)



source_text = ctk.CTkTextbox(
    app,
    width=820,
    height=120,
    corner_radius=12,
    border_width=2,
    border_color="#3B82F6",
    font=("Segoe UI",15)
)

source_text.pack(pady=10)



language = ctk.CTkComboBox(
    app,
    values=languages,
    width=250,
    font=("Segoe UI",14)
)

language.set("hindi")

language.pack(pady=10)



button_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

button_frame.pack(pady=15)



translate_btn = ctk.CTkButton(
    button_frame,
    text="🔄 Translate",
    command=translate,
    width=170
)

translate_btn.grid(
    row=0,
    column=0,
    padx=10,
    pady=8
)



voice_btn = ctk.CTkButton(
    button_frame,
    text="🎤 Voice",
    command=start_voice,
    width=170
)

voice_btn.grid(
    row=0,
    column=1,
    padx=10,
    pady=8
)



speak_btn = ctk.CTkButton(
    button_frame,
    text="🔊 Speak",
    command=speak,
    width=170
)

speak_btn.grid(
    row=1,
    column=0,
    padx=10,
    pady=8
)



copy_btn = ctk.CTkButton(
    button_frame,
    text="📋 Copy",
    command=copy_text,
    width=170
)

copy_btn.grid(
    row=1,
    column=1,
    padx=10,
    pady=8
)



download_btn = ctk.CTkButton(
    button_frame,
    text="⬇ Download",
    command=download,
    width=170,
    fg_color="#10B981",
    hover_color="#059669"
)

download_btn.grid(
    row=2,
    column=0,
    padx=10,
    pady=8
)



clear_btn = ctk.CTkButton(
    button_frame,
    text="🗑 Clear",
    command=clear,
    width=170,
    fg_color="#EF4444",
    hover_color="#DC2626"
)

clear_btn.grid(
    row=2,
    column=1,
    padx=10,
    pady=8
)




ctk.CTkLabel(
    app,
    text="Translated Text",
    font=("Segoe UI",16,"bold")
).pack(
    anchor="w",
    padx=30,
    pady=(10,0)
)



translated_text = ctk.CTkTextbox(
    app,
    width=820,
    height=150,
    corner_radius=12,
    border_width=2,
    border_color="#8B5CF6",
    font=("Segoe UI",15)
)

translated_text.pack(
    pady=10
)



status = ctk.CTkLabel(
    app,
    text="🟢 Ready",
    font=("Segoe UI",14,"bold"),
    text_color="#22C55E"
)

status.pack(
    pady=10
)



app.mainloop()