import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np


class Exp(tk.Toplevel):
    def __init__(self, master, data):
        super(Exp, self).__init__(master)



# index = np.arange(5)
#
# values1 = [5,7,3,4,6]
# values2 = [6,6,4,5,7]
# bw = 0.4
# plt.axis([0,5,0,8])
# plt.title('A Multiseries Bar Chart', fontsize=20)
# plt.bar(index, values1, bw, color='b', label="tim")
# plt.bar(index+bw, values2, bw, color='g', label="ins")
# plt.xticks(index+1.5*bw,['inseption_1000000.sort','Bjjjjjjjjjjjj','C','D','E'])
#
# plt.legend(loc=2)
# plt.show()








import matplotlib, numpy, sys
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as Tk

root = Tk.Tk()

f = Figure(figsize=(5,4), dpi=100)
ax = f.add_subplot(111)

data = (20, 35, 30, 35, 27)

ind = numpy.arange(5)  # the x locations for the groups
width = .5

rects1 = ax.bar(ind, data, width)

canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.draw()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

Tk.mainloop()