import tkinter as tk
import pyttsx3
from langchain_community.llms import Ollama

# === CONFIG ===
OLLAMA_MODEL = "phi3:mini"

# === VOICE SETUP ===
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# === LLM SETUP ===
llm = Ollama(model=OLLAMA_MODEL)

# === QUERY HANDLING ===
def process_query(query):
    return llm.invoke(query)

# === GUI ===
class AssistantGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sarvwigyan Chatbot")

        self.label = tk.Label(master, text="Ask your question:")
        self.label.pack()

        self.text_entry = tk.Entry(master, width=70)
        self.text_entry.pack()

        self.ask_button = tk.Button(master, text="Ask", command=self.ask_question)
        self.ask_button.pack()

        self.response_box = tk.Text(master, height=20, width=80)
        self.response_box.pack()

    def ask_question(self):
        query = self.text_entry.get()
        self.response_box.delete(1.0, tk.END)
        self.response_box.insert(tk.END, "⏳ Thinking...\n")
        self.master.update()

        answer = process_query(query)

        self.response_box.delete(1.0, tk.END)
        self.response_box.insert(tk.END, answer)
        speak(answer)

# === RUN APP ===
if __name__ == "__main__":
    root = tk.Tk()
    app = AssistantGUI(root)
    root.mainloop()
