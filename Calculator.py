from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
import imageio
from model import model
from tkinter import messagebox

class Calculator:

    ####---- this function is the design of the GUI---###
    def __init__(self, master):
        m = model()
        self.master = master
        master.title("K Means Clustering")


        self.total=0
        self.entered_number=0
        self.cluster = 0 #number of clusters
        self.runs = 0 #number of runs
        self.path ="" #path for data
        self.isPrepareDone = False #check if the preparetion went well

        vcmd = master.register(self.validate)  # we have to wrap the command

        #first row of the GUI
        self.label_path = Label(master, text="File Path")
        self.entry_path = Entry(master,state=DISABLED)
        self.browse_button = Button(master, text="browse", command=lambda: self.browsefile(m))

        #second row of the GUI
        self.label_clusters = Label(master, text="Num of clusters k")
        self.entry_clusters = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        #third row of the GUI
        self.label_runs = Label(master, text="Num of runs")
        self.entry_runs = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        #4th row of the GUI
        self.prepare_button = Button(master, text="Pre-process", command=lambda: self.prepare_data(m))

        #5th row of the GUI
        self.cluster_button = Button(master, text="Cluster",state=DISABLED, command=lambda: self.Cluster(m))

        #6th row of the GUI
        self.label_msg = Label(master, text="Message Box: ")
        self.entry_msg = Entry(master,width='100')
        self.entry_msg.delete(0,END)
        self.entry_msg.insert(0," Welcome to assignment 4!")

        # LAYOUT
        #Positions in the first row
        self.label_path.grid(row=0, column=0,columnspan=2,sticky=W)
        self.entry_path.grid(row=0, column=1, columnspan=10,sticky=W)
        self.browse_button.grid(row=0, column=2,sticky=E)

        #Positions in the second row
        self.label_clusters.grid(row=1, column=0, columnspan=2,sticky=W)
        self.entry_clusters.grid(row=1, column=1,sticky=W)

        #Positions in the third row
        self.label_runs.grid(row=2, column=0, columnspan=2,sticky=W)
        self.entry_runs.grid(row=2, column=1,sticky=W)

        #Positions in the 4th row
        self.prepare_button.grid(row=3, column=0, sticky=W)

        #Positions in the 5th row
        self.cluster_button.grid(row=4, column=0, sticky=W)

        #Positions in the 6th row
        self.label_msg.grid(row=5, column=0, sticky=W)
        self.entry_msg.grid(row=5, column=1, sticky=W)

    #Changing the value of the Message Box on line 6
    def PrintToMessageBox(self, text):
        self.entry_msg.delete(0, END)
        self.entry_msg.insert(0, text)

    # Show new dialog
    def ShowDialog(self,text):
        messagebox.showinfo("K Means Clustering", text)

    # Show an Error dialog
    def ShowErrorDialog(self, text):
        messagebox.showerror("K Means Clustering",text)

    # activate the data preparation in the model, and checks all values are correct
    def prepare_data(self,m):
        self.cluster = int(self.entry_clusters.get())
        self.runs = int(self.entry_runs.get())
        m.initBeforePrepare(self.path,self.cluster,self.runs)
        m.PrepareData()
        if len(m.df) == 0:
            self.ShowErrorDialog('You have chosen an empty database')
            self.PrintToMessageBox('Please choose a none empty databse')
        elif self.cluster < 1 or self.cluster >= len(m.df):
            self.ShowErrorDialog('You have to choose the clusters number in the range: 0 to number of countries')
            self.PrintToMessageBox('Please choose a correct value')
        else:
            self.isPrepareDone = True
            self.cluster_button.configure(state=NORMAL)
            self.ShowDialog('Preprocessing completed successfully!')
            self.PrintToMessageBox('Preprocessing completed successfully! now you can cluster')

    # allow the user to choose the path for the data
    def browsefile(self,m):
        self.path = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                      filetypes=(("data files", "*.xl*"), ("all files", "*.*")))
        m.ReadCsv(self.path)
        self.entry_path.configure(state=NORMAL)
        self.entry_path.delete(0, END)
        self.entry_path.insert(0, self.path)
        self.entry_path.configure(state=DISABLED)

    # activate the cluster in the model, and print the cluster results
    def Cluster(self,m):
        if self.isPrepareDone:
            if self.cluster == 0 or self.runs == 0 or  self.path =="":
                self.ShowErrorDialog('Please choose a path for data,num of clusters and numer of runs')
                self.PrintToMessageBox('choose path,clusters and runs')
            else:
                m.KmeansModel()
                self.ConvertToGif()

                imgPath1 = r'./name.gif'
                photo1 = PhotoImage(file=imgPath1)
                self.image1_label = Label(image=photo1, width='400px', height='400px')
                self.image1_label.image = photo1  # keep a reference!

                # image2
                imgPath2 = r'./scatter.gif'
                photo2 = PhotoImage(file=imgPath2)
                self.image2_label = Label(image=photo2, width='400px', height='400px')
                self.image2_label.image = photo2  # keep a reference!
                # self.image2_label.grid(row=5, column=10,sticky=E)


                self.image1_label.grid(row=6, column=0, sticky=W)
                self.image2_label.grid(row=6, column=1, sticky=E)
                self.ShowDialog('Clustering completed successfully!')
                self.PrintToMessageBox('Clustering completed successfully!')
        else:
            self.ShowErrorDialog("You try to cluster without preparation")
            self.PrintToMessageBox("You try to cluster without preparation")

    # a function that convert the format of the image from png to gif
    def ConvertToGif(self):
        images = []
        filesnames = ['./name.png']
        for filename in filesnames:
            images.append(imageio.imread(filename))
        imageio.mimsave('./name.gif', images)

        images = []
        filesnames = ['./scatter.png']
        for filename in filesnames:
            images.append(imageio.imread(filename))
        imageio.mimsave('./scatter.gif', images)
        # image1

        # self.image1_label.grid(row=5, column=0,sticky=W)

    # make sure that the inserted value to the entry is an integer
    def validate(self, new_text):
        if not new_text:  # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

root = Tk()
my_gui = Calculator(root)
root.mainloop()
