from tkinter import *
from tkinter import ttk, messagebox
import random
import os

class DiceGame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Игра в Кости")
        self.window.geometry("600x750")
        self.window.resizable(False, False)
        self.window.configure(bg='#2c3e50')
        
        # Загрузка изображений кубиков
        self.dice_images = {}
        for i in range(1, 7):
            try:
                self.dice_images[i] = PhotoImage(file=f"dice_{i}.png").subsample(2, 2)
            except:
                # Если файлы не найдены, создаем заглушки
                self.dice_images[i] = PhotoImage(width=80, height=80)
        
        # Переменные для хранения результатов
        self.player_score = 0
        self.computer_score = 0
        self.round_count = 1
        
        self.setup_ui()
        
    def setup_ui(self):
        # Создаем стиль для виджетов
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=10)
        style.configure('Title.TLabel', font=('Arial', 20, 'bold'), background='#2c3e50', foreground='white')
        style.configure('Score.TLabel', font=('Arial', 14), background='#2c3e50', foreground='white')
        
        # Главный фрейм
        main_frame = Frame(self.window, bg='#2c3e50')
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="🎲 Игра в Кости", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Фрейм для кубиков
        dice_frame = Frame(main_frame, bg='#34495e', relief=RAISED, bd=2)
        dice_frame.pack(pady=20, fill=X, padx=10)
        
        # Игрок
        player_frame = Frame(dice_frame, bg='#34495e')
        player_frame.pack(side=LEFT, expand=True, pady=20)
        
        Label(player_frame, text="Ваш кубик", font=('Arial', 12), 
              bg='#34495e', fg='white').pack(pady=(0, 10))
        
        self.player_dice_label = Label(player_frame, image="", 
                                     bg='#34495e', fg='#e74c3c')
        self.player_dice_label.pack(pady=5)
        
        self.player_value_label = Label(player_frame, text="", font=('Arial', 16, 'bold'),
                                      bg='#34495e', fg='#e74c3c')
        self.player_value_label.pack(pady=5)
        
        # Разделитель
        separator = Frame(dice_frame, bg='#7f8c8d', width=2, height=150)
        separator.pack(side=LEFT, padx=20, fill=Y)
        
        # Компьютер
        computer_frame = Frame(dice_frame, bg='#34495e')
        computer_frame.pack(side=RIGHT, expand=True, pady=20)
        
        Label(computer_frame, text="Кубик компьютера", font=('Arial', 12), 
              bg='#34495e', fg='white').pack(pady=(0, 10))
        
        self.computer_dice_label = Label(computer_frame, image="", 
                                       bg='#34495e', fg='#3498db')
        self.computer_dice_label.pack(pady=5)
        
        self.computer_value_label = Label(computer_frame, text="", font=('Arial', 16, 'bold'),
                                        bg='#34495e', fg='#3498db')
        self.computer_value_label.pack(pady=5)
        
        # Фрейм для кнопок
        button_frame = Frame(main_frame, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        # Кнопки
        self.roll_button = ttk.Button(button_frame, text="🎲 Бросить кубики", 
                                    command=self.roll_dice, style='TButton')
        self.roll_button.pack(pady=5, fill=X)
        
        self.reset_button = ttk.Button(button_frame, text="🔄 Новая игра", 
                                     command=self.reset_game, style='TButton')
        self.reset_button.pack(pady=5, fill=X)
        
        # Фрейм для статистики
        stats_frame = Frame(main_frame, bg='#34495e', relief=GROOVE, bd=2)
        stats_frame.pack(pady=20, fill=X, padx=10)
        
        # Статистика
        Label(stats_frame, text="Статистика игры", font=('Arial', 14, 'bold'), 
              bg='#34495e', fg='white').pack(pady=(10, 15))
        
        stats_grid = Frame(stats_frame, bg='#34495e')
        stats_grid.pack(pady=(0, 15))
        
        # Счетчик раундов
        self.round_label = Label(stats_grid, text=f"Раунд: {self.round_count}", 
                               font=('Arial', 12), bg='#34495e', fg='white')
        self.round_label.grid(row=0, column=0, padx=20, pady=5, columnspan=2)
        
        # Счет игрока
        Label(stats_grid, text="Ваши очки:", font=('Arial', 12), 
              bg='#34495e', fg='#e74c3c').grid(row=1, column=0, padx=20, pady=5, sticky='w')
        self.player_score_label = Label(stats_grid, text=str(self.player_score), 
                                      font=('Arial', 12, 'bold'), bg='#34495e', fg='#e74c3c')
        self.player_score_label.grid(row=1, column=1, padx=20, pady=5)
        
        # Счет компьютера
        Label(stats_grid, text="Очки компьютера:", font=('Arial', 12), 
              bg='#34495e', fg='#3498db').grid(row=2, column=0, padx=20, pady=5, sticky='w')
        self.computer_score_label = Label(stats_grid, text=str(self.computer_score), 
                                        font=('Arial', 12, 'bold'), bg='#34495e', fg='#3498db')
        self.computer_score_label.grid(row=2, column=1, padx=20, pady=5)
        
        # Метка результата
        self.result_label = Label(main_frame, text="Нажмите 'Бросить кубики' чтобы начать!", 
                                font=('Arial', 14, 'bold'), bg='#2c3e50', fg='#f39c12')
        self.result_label.pack(pady=10)
        
    def roll_dice(self):
        # Генерация случайных чисел для кубиков
        player_roll = random.randint(1, 6)
        computer_roll = random.randint(1, 6)
        
        # Отображение изображений кубиков
        self.player_dice_label.config(image=self.dice_images[player_roll])
        self.computer_dice_label.config(image=self.dice_images[computer_roll])
        
        # Отображение числовых значений
        self.player_value_label.config(text=f"Выпало: {player_roll}")
        self.computer_value_label.config(text=f"Выпало: {computer_roll}")
        
        # Определение победителя раунда
        if player_roll > computer_roll:
            self.player_score += 1
            result_text = "🎉 Вы выиграли этот раунд!"
            result_color = "#27ae60"
        elif computer_roll > player_roll:
            self.computer_score += 1
            result_text = "🤖 Компьютер выиграл этот раунд!"
            result_color = "#e74c3c"
        else:
            result_text = "⚖️ Ничья!"
            result_color = "#f39c12"
        
        # Обновление статистики
        self.round_count += 1
        self.round_label.config(text=f"Раунд: {self.round_count}")
        self.player_score_label.config(text=str(self.player_score))
        self.computer_score_label.config(text=str(self.computer_score))
        self.result_label.config(text=result_text, fg=result_color)
        
        # Проверка на победу в игре (лучший из 5 раундов)
        if self.player_score >= 3 or self.computer_score >= 3:
            if self.player_score > self.computer_score:
                messagebox.showinfo("Игра окончена", "🎊 Поздравляем! Вы выиграли игру!")
            else:
                messagebox.showinfo("Игра окончена", "Игра окончена! Компьютер выиграл.")
            self.reset_game()
    
    def reset_game(self):
        # Сброс всех значений к начальным
        self.player_score = 0
        self.computer_score = 0
        self.round_count = 1
        
        # Обновление интерфейса
        self.player_dice_label.config(image="")
        self.computer_dice_label.config(image="")
        self.player_value_label.config(text="")
        self.computer_value_label.config(text="")
        self.round_label.config(text=f"Раунд: {self.round_count}")
        self.player_score_label.config(text=str(self.player_score))
        self.computer_score_label.config(text=str(self.computer_score))
        self.result_label.config(text="Нажмите 'Бросить кубики' чтобы начать!", fg="#f39c12")
    
    def run(self):
        self.window.mainloop()

# Запуск приложения
if __name__ == "__main__":
    game = DiceGame()
    game.run()