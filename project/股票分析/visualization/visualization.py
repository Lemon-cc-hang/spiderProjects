"""
窗口界面可视化
"""
from tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import pandas as pd
import re

class StockChart(Frame):
	def __init__(self):
		Frame.__init__(self, parent=None)
		self.pack(expand=YES, fill=BOTH)
		l = Label(self, text="股票名")
		l.pack()
		self.stock_text = Entry()
		self.stock_text.pack()
		Button(self, command=self.run, text="显示").pack()

	def __schart(self, stock):
		if stock == '510050':
			name = 'SH510050'
			title = 'StockChart_SH510050'
		elif stock == '510310':
			name = 'SH510310'
			title = 'StockChart_SH510310'
		elif stock == '159915':
			name = 'SZ159915'
			title = 'StockChart_SZ159915'
		else:
			print("输入错误清重新输入~")
			return
		print(stock)
		df = pd.read_csv('../data/data_{}.csv'.format(name), encoding='utf8')
		df = df[df.date >= '2020-03-06']
		df.set_index('date', inplace=True)
		df.plot(kind='line')
		plt.xlabel('date')
		plt.ylabel('data')
		plt.title(title)
		plt.show()

	def __makeWidgets(self, stock):
		self.f = self.__schart(stock)
		self.canvas = FigureCanvasTkAgg(self.f)
		self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
		self.canvas.show()

	def run(self):
		stock = self.stock_text.get()
		self.__makeWidgets(stock)


if __name__ == '__main__':
	StockChart().mainloop()