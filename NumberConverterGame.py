import tkinter as tk
import random


class ConverterTrainerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Тренажер перевода чисел")
        
        self.question_count = tk.IntVar(value=3)
        self.number_type = tk.StringVar(value="Целые числа")
        self.questions = []
        self.answers = []
        self.systems = ["2", "3", "5", "6", "8", "10", "16"]
        
        self.setup_start_screen()
        
    def setup_start_screen(self):
        label = tk.Label(self.root, text="Выберите количество примеров и вид перевода")
        label.pack(pady=10)
        
        count_label = tk.Label(self.root, text="Количество примеров:")
        count_label.pack()
        count_menu = tk.OptionMenu(self.root, self.question_count, 3, 5, 7, 10)
        count_menu.pack(pady=5)
        
        type_label = tk.Label(self.root, text="Вид перевода:")
        type_label.pack()
        type_menu = tk.OptionMenu(self.root, self.number_type, "Целые числа", "Десятичные числа")
        type_menu.pack(pady=5)
        
        start_button = tk.Button(self.root, text="Начать", command=self.start_quiz)
        start_button.pack(pady=10)
    
    def start_quiz(self):
        self.questions = []
        self.answers = []
        self.quiz_window = tk.Toplevel(self.root)
        self.quiz_window.title("Вопросы")
        
        for i in range(self.question_count.get()):
            self.generate_question(i)
        
        submit_button = tk.Button(self.quiz_window, text="Проверить ответы", command=self.check_answers)
        submit_button.pack(pady=10)
        
    def generate_question(self, question_index):
        initial_base = random.choice(self.systems)
        target_base = random.choice([b for b in self.systems if b != initial_base])
        
        if self.number_type.get() == "Целые числа":
            number = random.randint(1, 100)
        else:
            number = random.uniform(1, 100)
        
        question = {
            "initial_base": initial_base,
            "target_base": target_base,
            "number": number
        }
        self.questions.append(question)
        
        self.display_question(question, question_index)
    
    def display_question(self, question, question_index):
        number_in_initial_base = self.convert_number(question["number"], 10, int(question["initial_base"]))
        
        label = tk.Label(self.quiz_window, text=f"Пример {question_index + 1}: Переведите число {number_in_initial_base} из системы {question['initial_base']} в систему {question['target_base']}")
        label.pack()
        
        entry = tk.Entry(self.quiz_window)
        entry.pack(pady=5)
        self.answers.append(entry)
    
    def convert_number(self, number, from_base, to_base):
        if from_base == 10:
            number_in_decimal = int(number) if isinstance(number, int) else float(number)
        else:
            number_in_decimal = int(str(number), from_base)
        
        if to_base == 10:
            return str(number_in_decimal)
        else:
            return self.convert_from_decimal(number_in_decimal, to_base)
    
    def convert_from_decimal(self, number, base):
        if base == 10:
            return str(int(number))
        digits = "0123456789ABCDEF"
        result = ""
        while number:
            result = digits[number % base] + result
            number //= base
        return result
    
    def check_answers(self):
        correct = True
        result_window = tk.Toplevel(self.root)
        result_window.title("Результаты")
        
        for i, question in enumerate(self.questions):
            user_answer = self.answers[i].get()
            correct_answer = self.convert_number(question["number"], 10, int(question["target_base"]))
            
            result_label = tk.Label(result_window, text=f"Пример {i + 1}: Ваш ответ: {user_answer}, Правильный ответ: {correct_answer}")
            result_label.pack()
            
            if user_answer != correct_answer:
                correct = False
        
        final_label = tk.Label(result_window, text="Все ответы верны!" if correct else "Есть ошибки в ответах.")
        final_label.pack(pady=10)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterTrainerApp(root)
    root.mainloop()
