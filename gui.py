import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import generation as gen
import graph
import os
import sys


class Select(tk.Frame):
    sequenceType = ("Упорядоченная", "Из едениц", "Случайная", "Частичная", "Обратная")

    def __init__(self, master, index, **kw):
        super().__init__(master, bg="#CCCCCC", **kw)

        self.master = master
        self.index = index
        self.on = tk.IntVar()

        self.sel = tk.Frame(master=self, relief=tk.RIDGE, borderwidth=3, bg="#AAAAAA")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # отметить | тип сортировки | количество | удалить
        # тип: случайно частично один обратно упорядоченно

        self.choose = tk.Checkbutton(master=self.sel, bg="#AAAAAA", variable=self.on)

        self.type = ttk.Combobox(master=self.sel, values=Select.sequenceType, state="readonly")

        self.count = tk.Entry(master=self.sel, width=10)

        self.remove = tk.Button(master=self.sel, text="Удалить", command=self.remove, font=("Arial", 8))

        self.choose.pack(side=tk.LEFT)
        self.type.pack(side=tk.LEFT)
        self.type.current(0)
        self.count.pack(side=tk.LEFT, padx=5)
        self.remove.pack(side=tk.LEFT, padx=5)

        self.pack(fill=tk.X, side=tk.TOP, ipadx=2, ipady=2)
        self.sel.grid(row=0, column=0, sticky=tk.NSEW, padx=3, pady=3)

    def remove(self):
        self.master.remove(self.index)

    def get(self):
        return self.type.get(), int(self.count.get())

    def validate(self):
        if not self.count.get().strip().isdigit() or not 2 <= int(self.count.get()) <= int(2e6):
            self.count.delete(0, tk.END)
            self.count.insert(0, "Error")
            return False
        return True


class SelectList(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, relief=tk.RIDGE, borderwidth=5, bg="#CCCCCC", **kw)

        self.master = master

        self.count = 0
        self.selects = [None] * 8

        self.grid(row=2, column=0, sticky=tk.NSEW, padx=10, pady=5, ipady=5, ipadx=10)

    def add(self):
        for i in range(8):
            if self.selects[i] is None:
                self.selects[i] = Select(master=self, index=i)
                self.count += 1
                self.master.master.console.log("Создан выбор генерации файла.")
                break
        else:
            self.master.master.console.log("ОШИБКА: Вы не можете создать больше 8 файлов.")

    def remove(self, select):
        self.master.master.console.log("Удален выбор генерации файла.")
        self.selects[select].destroy()
        self.selects[select] = None
        self.count -= 1

    def get_on_count(self):
        res = 0
        for i in self.selects:
            if i is not None and i.on.get() == tk.ON:
                res += 1
        # print(res)
        return res


class LeftMenu(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, relief=tk.RIDGE, borderwidth=5, bg="#CCCCCC", **kw)
        self.master = master

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.header = tk.Label(text="Генерация", bg="#CCCCCC", master=self, font=10)
        self.sList = SelectList(master=self)
        self.addButton = tk.Button(master=self, command=self.sList.add, text="+")
        self.genButton = tk.Button(master=self, command=self.generate, text="Сгенерировать")

        self.header.grid(row=0, column=0, sticky=tk.N + tk.EW, padx=5, pady=5)
        self.addButton.grid(row=1, column=0, sticky=tk.EW, padx=10, pady=7)
        self.genButton.grid(row=3, column=0, sticky=tk.S + tk.EW, padx=10, pady=5)

        self.grid(row=0, rowspan=2, column=0, sticky=tk.NSEW, padx=5, pady=5)

    def generate(self):
        all_count = 0
        ok_count = 0
        if self.sList.count < 1 or self.sList.get_on_count() < 1:
            self.master.console.log("Ошибка: Не выбраны файлы для генерации.")
        else:
            self.folder = filedialog.askdirectory()
            if self.folder == "":
                self.master.console.log("Ошибка: Не выбрана директория.")
            else:

                self.master.console.log("Генерация файлов...")

                for s in self.sList.selects:
                    if s is not None:
                        all_count += 1
                        if s.on.get() == 1:
                            self.master.console.log("Проверка поля " + str(all_count))
                            if s.validate():

                                self.master.console.log("Генерация файла из поля " + str(all_count))
                                gen.generate_file(*s.get(), self.folder)
                                ok_count += 1
                            else:
                                self.master.console.log("Ошибка: введено неверное количество.")

                if ok_count == 0:
                    self.master.console.log("Ошибка: Было получено 0 правильных полей")
                else:
                    if ok_count == 1:
                        self.master.console.log("Был сгенерирован " + str(ok_count) + " файл.")
                    elif ok_count <= 4:
                        self.master.console.log("Было сгенерированно " + str(ok_count) + " файла.")
                    else:
                        self.master.console.log("Было сгенерированно " + str(ok_count) + " файлов.")


class File(tk.Frame):
    def __init__(self, master, file_name, **kw):
        super().__init__(master, bg="#CCCCCC", **kw)

        self.master = master
        self.file_name = file_name

        self.obj = gen.open_file(file_name)

        if self.obj is None:
            self.master.master.master.console.log("ОШИБКА: Невозможно открыть файл.")

        else:
            self.fil = tk.Frame(master=self, relief=tk.RIDGE, borderwidth=3, bg="#AAAAAA")
            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)

            self.name = tk.Label(master=self.fil, bg="#AAAAAA", text=self.obj.name)
            self.type = tk.Label(master=self.fil, bg="#AAAAAA", text=self.obj.type)
            self.count = tk.Label(master=self.fil, bg="#AAAAAA", text=self.obj.count)

            self.name.pack(side=tk.LEFT, padx=5)
            self.type.pack(side=tk.LEFT, padx=5)
            self.count.pack(side=tk.LEFT, padx=5)

            self.pack(fill=tk.X, side=tk.TOP, ipadx=2, ipady=2)
            self.fil.grid(row=0, column=0, sticky=tk.NSEW, padx=3, pady=3)

    def get_data(self):
        return self.obj


class FileList(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, relief=tk.RIDGE, borderwidth=5, bg="#CCCCCC", **kw)

        self.master = master

        self.files = [None] * 8

        self.grid(row=2, column=0, sticky=tk.NSEW, padx=10, pady=5, ipady=5, ipadx=10)

    def add_file(self, file_name):
        for i in range(8):
            if self.files[i] is None:
                self.files[i] = File(master=self, file_name=file_name)
                break

    def clear_files(self):
        for i in range(8):
            if self.files[i] is not None:
                # print(self.files[i])
                self.files[i].destroy()
                self.files[i] = None

    def is_empty(self):
        for f in self.files:
            if f is not None:
                if f.obj is not None:
                    return False
        return True

    def get_data(self):
        res = []
        for f in self.files:
            if f is not None:
                if f.obj is not None:
                    res.append(f.obj)

        return res


class RightMenu(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, relief=tk.RIDGE, borderwidth=5, bg="#CCCCCC", **kw)
        self.master = master

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.header = tk.Label(text="Эксперимент", bg="#CCCCCC", master=self, font=10)
        self.fList = FileList(master=self)
        self.fileButton = tk.Button(master=self, command=self.open_files, text="Открыть файлы")
        self.expButton = tk.Button(master=self, command=self.experiment, text="Эксперементировать")

        self.header.grid(row=0, column=0, sticky=tk.N + tk.EW, padx=5, pady=5)
        self.fileButton.grid(row=1, column=0, sticky=tk.EW, padx=10, pady=7)
        self.expButton.grid(row=3, column=0, sticky=tk.S + tk.EW, padx=10, pady=5)
        self.grid(row=0, rowspan=2, column=1, sticky=tk.NSEW, padx=5, pady=5)

    def open_files(self):
        self.files = filedialog.askopenfilenames(filetypes=(("Файлы эксперимента", "*.sort"),),
                                                 initialdir="./files",
                                                 multiple=True)
        if len(self.files) < 1:
            self.master.console.log("ОШИБКА: Вы не выбрали ни одного файла.")
        else:
            if len(self.files) > 8:
                self.master.console.log("ОШИБКА: Вы не можете выбрать больше 8 файлов.")
            else:
                self.fList.clear_files()
                for f in self.files:
                    self.master.console.log("Открытие файла: <" + f + ">")
                    self.fList.add_file(file_name=f)

    def experiment(self):
        if self.fList.is_empty():
            self.master.console.log("Ошибка: Не выбрано файлов для эксперимента.")
        else:
            self.master.console.log("Проведение эксперемента...")
            self.results = graph.Exp(master=self, data=self.fList.get_data())


class Console(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, relief=tk.RIDGE, borderwidth=5, bg="#CCCCCC", **kw)
        self.master = master

        self.header = tk.Label(text="Console log", bg="#CCCCCC", master=self)
        self.console = tk.Text(master=self, width=113, height=4, relief=tk.RIDGE,
                               borderwidth=5, font=("Courier", 10), state=tk.DISABLED)

        self.scroll = tk.Scrollbar(command=self.console.yview, master=self)

        self.header.pack(fill=tk.X, side=tk.TOP)
        self.console.pack(side=tk.LEFT, fill=tk.Y)
        self.scroll.pack(side=tk.LEFT, fill=tk.Y)

        self.console.config(yscrollcommand=self.scroll.set)

        self.grid(row=3, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

    def log(self, text):
        self.console.configure(state=tk.NORMAL)
        self.console.insert(1.0, str(text) + '\n')
        self.console.configure(state=tk.DISABLED)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.lMenu = LeftMenu(master=self)
        self.rMenu = RightMenu(master=self)
        self.console = Console(master=self)


class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("960x600")
        self.title("Experiment")
        self.resizable(False, False)

        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        ico = os.path.join(base_path, r"icon.ico")

        self.iconbitmap(ico)

        self.app = Application(master=self)

        self.mainloop()


if __name__ == "__main__":
    Root()
