import tkinter as tk
import nltk
import string

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK resources
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")

# ---------------- FAQ DATA ---------------- #

faq = {
    "What is AI?":"Artificial Intelligence (AI) enables machines to perform tasks that normally require human intelligence.",
"AI":"Artificial Intelligence (AI) enables machines to perform tasks that normally require human intelligence.",
"Explain AI":"Artificial Intelligence (AI) enables machines to perform tasks that normally require human intelligence.",

"What is ML?":"Machine Learning is a subset of Artificial Intelligence that learns from data.",
"ML":"Machine Learning is a subset of Artificial Intelligence that learns from data.",
"Explain ML":"Machine Learning is a subset of Artificial Intelligence that learns from data.",

"What is DL?":"Deep Learning is a subset of Machine Learning based on neural networks.",
"DL":"Deep Learning is a subset of Machine Learning based on neural networks.",

"What is NLP?":"NLP stands for Natural Language Processing.",
"Explain NLP":"NLP stands for Natural Language Processing.",

    "What is Python?":"Python is a high-level programming language.",

    "Who developed Python?":"Python was developed by Guido van Rossum.",

    "What is Artificial Intelligence?":"Artificial Intelligence enables machines to perform tasks that normally require human intelligence.",

    "What is Machine Learning?":"Machine Learning is a subset of Artificial Intelligence that learns from data.",

    "What is Deep Learning?":"Deep Learning is a subset of Machine Learning based on neural networks.",

    "What is NLP?":"NLP stands for Natural Language Processing.",

    "What is Data Science?":"Data Science is the process of extracting useful insights from data.",

    "What is NumPy?":"NumPy is a Python library for numerical computing.",

    "What is Pandas?":"Pandas is a Python library used for data analysis and manipulation.",

    "What is Scikit-learn?":"Scikit-learn is a popular machine learning library in Python.",

    "What is TensorFlow?":"TensorFlow is an open-source deep learning framework developed by Google.",

    "What is PyTorch?":"PyTorch is an open-source deep learning framework developed by Meta.",

    "What is OpenCV?":"OpenCV is a library used for computer vision and image processing.",

    "What is Matplotlib?":"Matplotlib is a Python library used for data visualization.",

    "What is Seaborn?":"Seaborn is a Python library for statistical data visualization.",

    "What is a Variable?":"A variable stores data values.",

    "What is a Function?":"A function is a reusable block of code.",

    "What is a Loop?":"A loop executes a block of code repeatedly.",

    "What is a List?":"A list is an ordered collection of items.",

    "What is a Dictionary?":"A dictionary stores data in key-value pairs.",

    "What is a Tuple?":"A tuple is an ordered and immutable collection.",

    "What is a Set?":"A set stores unique values only.",

    "What is a Class?":"A class is a blueprint for creating objects.",

    "What is an Object?":"An object is an instance of a class.",

    "What is a Compiler?":"A compiler converts source code into machine code.",

    "What is an Interpreter?":"An interpreter executes code line by line.",

    "What is an Algorithm?":"An algorithm is a step-by-step procedure to solve a problem.",

    "What is a Dataset?":"A dataset is a collection of related data used for analysis or training.",

    "What is Overfitting?":"Overfitting occurs when a model learns training data too well and performs poorly on new data.",

    "What is Cloud Computing?":"Cloud computing provides computing resources over the internet.",

    "Hi":"Hello! Welcome to the FAQ Chatbot.",

    "Hello":"Hello! Ask me anything about Python or AI.",

    "Hey":"Hi! How can I help you?",

    "Thank You":"You're welcome!",

    "Bye":"Goodbye! Have a wonderful day!"
}

# ---------------- PREPROCESS ---------------- #
stop_words = set(stopwords.words("english"))
def preprocess(text):

    text = text.lower()

    text = text.replace("ai", "artificial intelligence")
    text = text.replace("ml", "machine learning")
    text = text.replace("dl", "deep learning")
    text = text.replace("nlp", "natural language processing")

    tokens = word_tokenize(text)

    words = []

    for word in tokens:
        if word.isalnum() and word not in stop_words:
            words.append(word)

    return " ".join(words)

# ---------------- TF-IDF ---------------- #

questions = list(faq.keys())

processed_questions = []

for question in questions:

    processed_questions.append(preprocess(question))

vectorizer = TfidfVectorizer()

faq_vectors = vectorizer.fit_transform(processed_questions)
# ---------------- FIND BEST ANSWER ---------------- #

def get_answer(user_question):

    clean_question = preprocess(user_question)

    user_vector = vectorizer.transform([clean_question])

    similarity = cosine_similarity(user_vector, faq_vectors)

    best_match = similarity.argmax()

    score = similarity[0][best_match]

    if score >= 0.15:
        return faq[questions[best_match]]
    else:
        return "Sorry! I couldn't find a suitable answer."

# ---------------- BUTTON FUNCTIONS ---------------- #

def show_answer():

    question = question_entry.get().strip()

    if question == "":
        answer_label.config(text="Please enter a question.")
        return

    answer = get_answer(question)

    answer_label.config(text=answer)


def clear_text():

    question_entry.delete(0, tk.END)

    answer_label.config(text="Answer will appear here")


def enter_key(event):

    show_answer()

# ---------------- WINDOW ---------------- #

root = tk.Tk()

root.title("FAQ Chatbot")

root.geometry("650x430")

root.configure(bg="#1e1e2f")

root.resizable(False, False)

# ---------------- TITLE ---------------- #

title = tk.Label(
    root,
    text="🤖 FAQ Chatbot",
    font=("Arial", 20, "bold"),
    bg="#1e1e2f",
    fg="white"
)

title.pack(pady=15)

# ---------------- ENTRY ---------------- #

question_entry = tk.Entry(
    root,
    width=55,
    font=("Arial", 12)
)

question_entry.pack(pady=10)

question_entry.bind("<Return>", enter_key)
# ---------------- ASK BUTTON ---------------- #

ask_button = tk.Button(
    root,
    text="Ask Question",
    command=show_answer,
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    width=18,
    pady=5
)

ask_button.pack(pady=5)

# ---------------- CLEAR BUTTON ---------------- #

clear_button = tk.Button(
    root,
    text="Clear",
    command=clear_text,
    font=("Arial", 12, "bold"),
    bg="#f44336",
    fg="white",
    width=18,
    pady=5
)

clear_button.pack(pady=5)

# ---------------- ANSWER FRAME ---------------- #

answer_frame = tk.Frame(
    root,
    bg="#2b2b40",
    bd=2,
    relief="groove"
)

answer_frame.pack(pady=20, padx=20, fill="x")

answer_label = tk.Label(
    answer_frame,
    text="Answer will appear here",
    font=("Arial", 12),
    wraplength=550,
    justify="left",
    bg="#2b2b40",
    fg="white",
    padx=15,
    pady=15
)

answer_label.pack()

# ---------------- FOOTER ---------------- #

footer = tk.Label(
    root,
    text="Developed by Alekhya Gaddam | CodeAlpha Task 2",
    font=("Arial", 9),
    bg="#1e1e2f",
    fg="lightgray"
)

footer.pack(side="bottom", pady=8)

# ---------------- RUN APPLICATION ---------------- #

root.mainloop()