import sys

import numpy
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

import tkinter as tk

import timsort
import insertion_sort

import os
matplotlib.use('TkAgg')
_TIM = "__TIM__"
_INS = "__INS__"


class ExpData:
    def __init__(self, sort_files):
        self.file_names = []
        self.arr = []

        for f in sort_files:
            self.file_names.append(f.name)
            self.arr.append(f.sequence)

        self.time = {_TIM: [], _INS: []}
        self.sw = {_TIM: [], _INS: []}
        self.cmp = {_TIM: [], _INS: []}

    def experiment(self):
        for f in self.arr:
            ar = f.copy()
            st_tim = timsort.sort(ar)
            ar = f.copy()
            st_ins = insertion_sort.sort(ar)

            self.time[_TIM].append(st_tim.time)
            self.time[_INS].append(st_ins.time)

            self.sw[_TIM].append(st_tim.sw)
            self.sw[_INS].append(st_ins.sw)

            self.cmp[_TIM].append(st_tim.cmp)
            self.cmp[_INS].append(st_ins.cmp)


class Bar(tk.Frame):
    def __init__(self, master, names, title, data, **kw):
        super().__init__(master, **kw)

        self.names = names

        self.data = data
        self.title = title
        self.count = len(self.names)

        f = Figure(figsize=(4, 3), dpi=90)
        ax = f.add_subplot(111)

        index = numpy.arange(self.count)

        bw = 0.3

        ax.set_title(self.title, fontsize=20)

        ax.bar(index, self.data[_TIM], bw, color='b', label="tim")
        ax.bar(index + bw, self.data[_INS], bw, color='g', label="ins")

        ax.set_xticks(numpy.arange(self.count) + bw / 2)
        ax.set_xticklabels(self.names, rotation=45, ha="right")
        ax.legend(bbox_to_anchor=(1, 0.6))

        canvas = FigureCanvasTkAgg(f, master=self)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()

        f.tight_layout()

        canvas.draw()

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        ...


class Exp(tk.Toplevel):
    def __init__(self, master, data):
        super().__init__(master)

        self.data = data

        self.ex_data = ExpData(self.data)
        self.ex_data.experiment()

        self.time = tk.Frame(master=self, bg="red")
        self.sw = tk.Frame(master=self)
        self.cmp = tk.Frame(master=self)

        self.time_bar = Bar(master=self.time, names=self.ex_data.file_names, title="Время", data=self.ex_data.time)
        self.sw_bar = Bar(master=self.sw, names=self.ex_data.file_names, title="Перестановки", data=self.ex_data.sw)
        self.cmp_bar = Bar(master=self.cmp, names=self.ex_data.file_names, title="Сравнения", data=self.ex_data.cmp)

        self.time.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.sw.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.cmp.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        ico = os.path.join(base_path, r"icon.ico")

        self.iconbitmap(ico)

        self.iconbitmap(ico)


if __name__ == "__main__":
    import generation as g

    sf = g.open_file("./files/rnd_1000.sort")
    sf1 = g.open_file("./files/rnd_1000.sort")
    sf2 = g.open_file("./files/rnd_1000.sort")
    sf3 = g.open_file("./files/rnd_1000.sort")

    sf1.name = sf.name + str(1)
    sf2.name = sf.name + str(2)
    sf3.name = sf.name + str(3)

    a = [sf, sf1, sf2, sf3, sf, sf1, sf2, sf3]

    res = ExpData(a)
    res.experiment()

    root = tk.Tk()

    Bar(master=root, names=res.file_names, title="time", data=res.time)

    # Bar.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    root.mainloop()

    print(res.time, res.file_names, res.sw, res.cmp, sep='\n')
