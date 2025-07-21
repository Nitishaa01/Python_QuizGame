import requests
import random
import tkinter as tk
from tkinter import messagebox

class QuizGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Game")
        self.master.geometry("500x300")
        self.score = 0
        self.question_index = 0
        self.questions = []

        self.question_label = tk.Label(master, wraplength=480, font=('Arial', 14))
        self.question_label.pack(pady=20)

        self.options = []
        for i in range(4):
            btn = tk.Button(master, text="", width=40, font=('Arial', 12), command=lambda idx=i: self.check_answer(idx))
            btn.pack(pady=5)
            self.options.append(btn)

        self.fetch_questions()

    def fetch_questions(self):
        try:
            response = requests.get("https://opentdb.com/api.php?amount=5&type=multiple")
            data = response.json()

            for item in data['results']:
                question = item['question']
                correct = item['correct_answer']
                incorrect = item['incorrect_answers']
                options = incorrect + [correct]
                random.shuffle(options)
                self.questions.append({
                    'question': question,
                    'correct': correct,
                    'options': options
                })

            self.display_question()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch questions: {e}")

    def display_question(self):
        if self.question_index < len(self.questions):
            current = self.questions[self.question_index]
            self.question_label.config(text=f"Q{self.question_index + 1}: {current['question']}")
            for i in range(4):
                self.options[i].config(text=current['options'][i])
        else:
            messagebox.showinfo("Quiz Complete", f"Your score: {self.score}/{len(self.questions)}")
            self.master.destroy()

    def check_answer(self, idx):
        selected = self.options[idx].cget('text')
        correct = self.questions[self.question_index]['correct']
        if selected == correct:
            self.score += 1
        self.question_index += 1
        self.display_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizGame(root)
    root.mainloop()