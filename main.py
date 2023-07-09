import time
import threading
import tkinter as tk
from tkinter import ttk

class PomodoroTimer:

    def __init__(self):
        # configura a janela
        self.root = tk.Tk()
        self.root.geometry("600x300")
        self.root.title("POMODORO TIMER")

        # configura o estilo das abas
        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font=('Ubuntu', 16))
        self.s.configure("TButton", font=("Ubuntu", 16))

        # inicia as "abas"
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill='both', pady=10, expand=True)

        # cria as abas
        self.tabs1 = ttk.Frame(self.tabs, width=600, height=100)
        self.tabs2 = ttk.Frame(self.tabs, width=600, height=100)
        self.tabs3 = ttk.Frame(self.tabs, width=600, height=100)

        self.pomodoro_timer_label = ttk.Label(self.tabs1, text="25:00", font=("Ubuntu", 48))
        self.pomodoro_timer_label.pack(pady=20)

        self.pausa_rapida_label = ttk.Label(self.tabs2, text="05:00", font=("Ubuntu", 48))
        self.pausa_rapida_label.pack(pady=20)

        self.pausa_longa_label = ttk.Label(self.tabs3, text="15:00", font=("Ubuntu", 48))
        self.pausa_longa_label.pack(pady=20)

        # nomeia as abas
        self.tabs.add(self.tabs1, text='POMODORO')
        self.tabs.add(self.tabs2, text='PAUSA RAPIDA')
        self.tabs.add(self.tabs3, text="PAUSA LONGA")

        # pega grade de layout
        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)

        # cria os botoes
        self.botaoIniciar = ttk.Button(self.grid_layout, text="Iniciar", command=self.iniciar_thread_time)
        self.botaoIniciar.grid(row=0, column=0)

        self.botaoSkip = ttk.Button(self.grid_layout, text="Skip", command=self.pular_relogio)
        self.botaoSkip.grid(row=0, column=1)

        self.botaoReset = ttk.Button(self.grid_layout, text="Reset", command=self.resetar_relogio)
        self.botaoReset.grid(row=0, column=2)

        self.pomodoroCounterLabel = ttk.Label(self.grid_layout, text="Pomodoros: 0", font=("Ubuntu", 16))
        self.pomodoroCounterLabel.grid(row=1, column=0, columnspan=3, pady=10)

        self.pomodoroCounter = 0
        self.skipped = False
        self.stopped = False
        self.running = False

        self.root.mainloop()
        # roda tudo

    def iniciar_thread_time(self):
        if not self.running:
            t = threading.Thread(target=self.inicar_timer)
            t.start()
            self.running = True

    def inicar_timer(self):
        self.skipped = False
        self.stopped = False
        timerId = self.tabs.index(self.tabs.select())

        if timerId == 0:  # timer do pomodoro
            segundosCompletos = 60 * 25
            while segundosCompletos > 0 and not self.stopped:
                minutos, segundos = divmod(segundosCompletos, 60)
                self.pomodoro_timer_label.config(text=f'{minutos:02d}:{segundos:02d}')
                self.root.update()
                time.sleep(1)
                segundosCompletos -= 1
            if not self.stopped or self.skipped:
                self.pomodoroCounter += 1
                self.pomodoroCounterLabel.config(text=f'Pomodoros: {self.pomodoroCounter}')
                if self.pomodoroCounter % 4 == 0:
                    self.tabs.select(1)
                    self.inicar_timer()
                else:
                    self.tabs.select(0)
                    self.inicar_timer()

        elif timerId == 1: # pausa curta
            segundosCompletos = 60 * 5
            while segundosCompletos > 0 and not self.stopped:
                minutos, segundos = divmod(segundosCompletos, 60)
                self.pausa_rapida_label.config(text=f'{minutos:02d}:{segundos:02d}')
                self.root.update()
                time.sleep(1)
                segundosCompletos -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.inicar_timer()

        elif timerId == 2: # pausa longa
            segundosCompletos = 60 * 15
            while segundosCompletos > 0 and not self.stopped:
                minutos, segundos = divmod(segundosCompletos, 60)
                self.pausa_longa_label.config(text=f'{minutos:02d}:{segundos:02d}')
                self.root.update()
                time.sleep(1)
                segundosCompletos -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.inicar_timer()

    def resetar_relogio(self):
        self.pomodoroCounter = 0
        self.skipped = False
        self.stopped = True

        self.pomodoro_timer_label.config(text="25:00")
        self.pausa_rapida_label.config(text="05:00")
        self.pausa_longa_label.config(text="15:00")
        self.running = False

        self.pomodoroCounterLabel.config(text="Pomodoros: 0")
    def pular_relogio(self):
        Id = self.tabs.index(self.tabs.select())

        if Id == 0:
            self.pomodoro_timer_label.config(text="25:00")

        elif Id == 1:
            self.pausa_rapida_label.config(text="05:00")

        elif \
                Id == 2:
            self.pausa_longa_label.config(text="15:00")

        self.stopped = True
        self.skipped = True
PomodoroTimer()
print('fim')
