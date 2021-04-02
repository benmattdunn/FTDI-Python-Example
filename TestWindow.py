import tkinter as tk
import sharedDataFile

#matplot
#import matplotlib.pyplot as plt

#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sharedDataFile
#move plot to own class
class GUI(tk.Frame):

    def __init__(self, window):
        tk.Frame.__init__(self)
        #setupframes - remember you MUST attach to self (GUI)
        self.sizeFrame = tk.LabelFrame(self, padx=5, pady=5)
        self.sizeFrame.pack(fill=None, expand = False, padx=10, pady=10)
        self.dataDisplayLabel = tk.Label(self.sizeFrame, text="Default text - If you see this the ardunio is not connected. Try chaning the description of the device")
        self.dataDisplayLabel.pack()
        self.buttonTest = tk.Button(self.sizeFrame, text="CLOSE WINDOW AND END THREAD",
                                    command=self._root().destroy)  # werid syntax but whatever
        self.buttonTest.pack()


        #setup a chart - left this code in for reference for others to save some developement time
        #figure = plt.Figure(figsize=(6,5), dpi = 100)
        #ax = figure.add_subplot(111)
        #chart_type = FigureCanvasTkAgg(figure, sizeFrame)
        #chart_type.get_tk_widget().pack()
        #df = df[['First Column', 'Second Column']].groupby('First Column').sum()
        #df.plot(kind='Chart Type such as bar', legend=True, ax=ax)
        #ax.set_title('The Title for your chart')



    #all methods that update on a clock are called from here. This basically just updates the data. However you CAN
    #put anything here and it will change it as needed.
    def repaint(self):
        self.dataDisplayLabel['text'] = sharedDataFile.sharedDataWindowListener

