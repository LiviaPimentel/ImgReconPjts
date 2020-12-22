import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import cv2
import PIL.Image
import PIL.ImageTk
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import win32api #pip install pypiwin32
import numpy as np
from sklearn.cluster import KMeans
import os
from shutil import copyfile

class Menubar:

    def __init__(self, parent):
        font_specs = ("sans Serif", 14)

        menubar = tk.Menu(parent.master, font=font_specs)
        parent.master.config(menu=menubar)

        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label="Ouvrir",
                                  accelerator="Ctrl+O",
                                  command=parent.open_file)
        file_dropdown.add_command(label="Enregistrer",
                                  accelerator="Ctrl+S",
                                  command=parent.save)
        file_dropdown.add_command(label="Enregistrer sous",
                                  accelerator="Ctrl+Shift+S",
                                  command=parent.save_as)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Sortir",
                                  command=parent.master.destroy)

        menubar.add_cascade(label="Fichier", menu=file_dropdown)


class ImageEditeur:
    def __init__(self, master):
        master.title("Pas Enregistre - PyText")

        font_specs = ("sans Serif", 18)

        self.master = master
        self.filename = None
        self.filedata = None
        self.canvas = None
        self.tdir = "tempImageEditeur"
        if(not os.path.exists(self.tdir)):os.mkdir(self.tdir)

        self.tdir = self.tdir + "/"


        img = PhotoImage(file="blank.png")
        self.image = tk.Label(master,image = img, bg = "snow")
        self.image.image = img;
        self.image.grid(row=0, column=0, rowspan=4, columnspan=4, padx=5, pady=5,sticky="NS")
        self.image.bind('<ButtonPress-1>', lambda a:self.open_image_link())
        self.image.bind("<Double-Button>", lambda a:self.open_image_link2())
        self.afficeImage(PIL.Image.open("blank.png"));


        self.b_contours = Button(master, text="Contours")
        self.b_contours.grid(row=4, column=0)
        self.b_contours.bind('<ButtonPress-1>', lambda a:self.call_contours())   
        self.b_transforma = Button(master, text="Transformations")
        self.b_transforma.grid(row=4, column=1)
        self.b_transforma.bind('<ButtonPress-1>', lambda a:self.open_dialog_transforma())             
        self.b_binarisation = Button(master, text="Filtres")
        self.b_binarisation.grid(row=4, column=2)
        self.b_binarisation.bind('<ButtonPress-1>', lambda a:self.open_dialog_binar())
        self.b_segmentation = Button(master, text="Segmentation")
        self.b_segmentation.grid(row=4, column=3)
        self.b_segmentation.bind('<ButtonPress-1>', lambda a:self.open_dialog_segmentation())

        self.menubar = Menubar(self)
    def open_dialog_binar(self):
        if self.filename==None or self.filename=="":
            win32api.MessageBox(0, "Il n'y a pas des images pour traiter", "Error au moment de traiter")
            return None
        self.dialog = tk.Tk()
        self.dialog.title("Filtres et Binarisation")
        self.rw_dialog = 0
        Label(self.dialog, text="Type de filtre:").grid(row=self.rw_dialog,column=0,pady=5,padx=5);


        self.comboB = Combobox(self.dialog, values=["Filtre Gaussien","Binarisation d'OTSU","Gaussien + d'ORSU" ],state="readonly");
        self.comboB.grid(row=self.rw_dialog, column=1,pady=5,padx=5)
        self.rw_dialog = self.rw_dialog + 1
        self.comboB.bind("<<ComboboxSelected>>", self.select_comboB)
        self.comboB.current(1)

        self.b_apliqueT= Button(self.dialog, text="Apliquer");
        self.b_apliqueT.grid(row=self.rw_dialog, column=0);
        self.b_apliqueT.bind('<ButtonPress-1>', lambda a:self.aplique_transformation());

        self.b_annuleT= Button(self.dialog, text="Annuler");
        self.b_annuleT.grid(row=self.rw_dialog, column=1);
        self.b_annuleT.bind('<ButtonPress-1>', lambda a:self.annuler_transformation());
        self.select_comboB();
    def select_comboB(self,*args):
        img = cv2.imread(self.filename, 0)
        if(self.comboB.get()=="Filtre Gaussien"): dst = cv2.GaussianBlur(img, (5, 5), 0)
        if(self.comboB.get()=="Binarisation d'OTSU"): ret2, dst = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if(self.comboB.get()=="Gaussien + d'ORSU"):
            blur = cv2.GaussianBlur(img, (5, 5), 0)
            ret3, dst = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        cv2.imwrite(self.filename + '_tempo2.png', dst)
        self.filedata = PIL.Image.open(self.filename + '_tempo2.png')
        self.afficeImage(self.filedata);

    def open_dialog_transforma(self):
        if self.filename==None or self.filename=="":
            win32api.MessageBox(0, "Il n'y a pas des images pour traiter", "Error au moment de traiter")
            return None
        self.dialog = tk.Tk()
        self.dialog.title("Transformer image")
        self.rw_dialog = 0
        Label(self.dialog, text="Type de Transformation:").grid(row=self.rw_dialog,column=0,pady=5,padx=5);
        self.comboT = Combobox(self.dialog, values=["Scaler","Rotation"],state="readonly");
        self.comboT.grid(row=self.rw_dialog, column=1,pady=5,padx=5)
        self.rw_dialog = self.rw_dialog + 1
        self.comboT.bind("<<ComboboxSelected>>", self.select_comboT)
        self.comboT.current(1)

        self.frame_opcT= LabelFrame(self.dialog, text="Configuration");
        self.frame_opcT.grid(row=self.rw_dialog, column=0,columnspan=2, padx=5, pady=5);
        self.rw_dialog = self.rw_dialog + 1

        self.b_apliqueT= Button(self.dialog, text="Apliquer");
        self.b_apliqueT.grid(row=self.rw_dialog, column=0);
        self.b_apliqueT.bind('<ButtonPress-1>', lambda a:self.aplique_transformation());

        self.b_annuleT= Button(self.dialog, text="Annuler");
        self.b_annuleT.grid(row=self.rw_dialog, column=1);
        self.b_annuleT.bind('<ButtonPress-1>', lambda a:self.annuler_transformation());
        self.select_comboT();

    def select_combo2(self,*args):
        img = cv2.imread(self.filename, 0)
        if(self.comboB.get()=="HSV"): self.ache = True
        if(self.comboB.get()=="RGB"): self.ache = False
        self.segmentation()
        
  

    def open_dialog_segmentation(self):
        if self.filename==None or self.filename=="":
            win32api.MessageBox(0, "Il n'y a pas des images pour traiter", "Error au moment de traiter")
            return None
        self.dialog = tk.Tk()
        self.dialog.title("Segmentation")
        self.rw_dialog = 0
        Label(self.dialog, text="Type:").grid(row=self.rw_dialog,column=0,pady=5,padx=5);


        self.comboB = Combobox(self.dialog, values=["HSV","RGB" ],state="readonly");
        self.comboB.grid(row=self.rw_dialog, column=1,pady=5,padx=5)
        self.rw_dialog = self.rw_dialog + 1
        self.comboB.bind("<<ComboboxSelected>>", lambda a:self.select_combo2())
        self.comboB.current(1)


        
    def aplique_transformation(self):
        copyfile(self.filename+ "_tempo2.png", self.filename + "_tempo.png")
        self.filedata = PIL.Image.open(self.filename+'_tempo.png')
        self.afficeImage(self.filedata);
        self.afficheHisto()
        self.dialog.destroy()
        return "break"
    def annuler_transformation(self):
        self.filedata = PIL.Image.open(self.filename+'_tempo.png')
        self.afficeImage(self.filedata);
        self.dialog.destroy()
        return "break"

    def select_comboT(self,*args):
        if(self.comboT.get()=='Scaler'): self.d_scaler_image()
        if(self.comboT.get()=='Rotation'): self.d_rotation_image()
        #if(self.comboT.get()=='Perspective'): self.d_perspective_image()
    def vide_frame_opcT(self):
        self.frame_opcT.destroy()
        self.frame_opcT= LabelFrame(self.dialog, text="Configuration");
        self.frame_opcT.grid(row=1, column=0,columnspan=2, padx=5, pady=5);
    def d_scaler_image(self):
        self.vide_frame_opcT()
        Label(self.frame_opcT, text="Scale X").grid(row=0, column=0, pady=5, padx=5);
        self.scalexT = Spinbox(self.frame_opcT, format='%2.f',from_=1, to=10, increment=1,command=self.c_scalerT)
        self.scalexT.grid(row=0, column=1, pady=5, padx=5);
        Label(self.frame_opcT, text="Scale Y").grid(row=0, column=2, pady=5, padx=5);
        self.scaleyT = Spinbox(self.frame_opcT, format='%2.f',from_=1, to=10, increment=1,command=self.c_scalerT)
        self.scaleyT.grid(row=0, column=3, pady=5, padx=5);
    def c_scalerT(self):
        img = cv2.imread(self.filename)
        rows, cols, n= img.shape
        dst= cv2.resize(img, None, fx=int(self.scalexT.get()), fy=int(self.scaleyT.get()), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(self.filename + '_tempo2.png', dst)
        self.filedatatemp = PIL.Image.open(self.filename + '_tempo2.png')
        self.afficeImage(self.filedatatemp)
    def d_rotation_image(self):
        self.vide_frame_opcT()
        Label(self.frame_opcT, text="Angle(en Degré)").grid(row=0, column=0, pady=5, padx=5);
        self.valrotT = DoubleVar()
        self.rotationT = Spinbox(self.frame_opcT, format='%2.f',from_=0, to=360, increment=1,command=self.c_rotatioT);
        self.rotationT.grid(row=0, column=1, pady=5, padx=5);
        self.rotationT.bind("<Control-Button-1>", lambda a: self.c_rotatioT())
    def c_rotatioT(self,*args):
        img = cv2.imread(self.filename)
        rows, cols, n= img.shape
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), int(self.rotationT.get()), 1)
        dst = cv2.warpAffine(img, M, (cols, rows))
        cv2.imwrite(self.filename + '_tempo2.png', dst)
        self.filedatatemp = PIL.Image.open(self.filename + '_tempo2.png')
        self.afficeImage(self.filedatatemp)

    def d_perspective_image(self):
        self.vide_frame_opcT()
        Label(self.frame_opcT, text="Point de vu ").grid(row=0, column=0, pady=5, padx=5);
        self.comboPerspecT = Combobox(self.frame_opcT, values=["Top", "Bottom", "Left","Right"], state="readonly")
        self.comboPerspecT.bind("<<ComboboxSelected>>", self.c_perspectiveT)
        self.comboPerspecT.grid(row=0, column=1, pady=5, padx=5)

    def c_perspectiveT(self,*args):
        img = cv2.imread(self.filename)#cv2.IMREAD_COLOR
        rows, cols, ch = img.shape
        pts1 = np.float32([[0, 0], [128, 75], [75, 0], [75, 218]])
        pts2 = np.float32([[0, 0], [218, 0], [0, 218], [218, 218]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(img, M, (218, 218))
        cv2.imwrite(self.filename + '_tempo2.png', dst)
        self.filedatatemp = PIL.Image.open(self.filename + '_tempo2.png')
        self.afficeImage(self.filedatatemp)


    def call_contours(self):
        if self.filename == None or self.filename == "":
            win32api.MessageBox(0, "Il n'y a pas des images pour traiter", "Error au moment de traiter")
            return None
        img = cv2.imread(self.filename)
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
        cv2.imwrite(self.filename + '_tempo.png', img)
        self.filedata = PIL.Image.open(self.filename + '_tempo.png')
        self.afficeImage(self.filedata);

    def segmentation(self):
        if self.filename == None or self.filename == "":
            win32api.MessageBox(0, "Il n'y a pas des images pour traiter", "Error au moment de traiter")
            return None

        image = cv2.imread(self.filename)
        orig = image.copy()
        if self.ache == True:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        channels = cv2.split(image)
        channelIndices = [0, 2]
        image = image[:, :, channelIndices]
        numClusters = 3
        if len(image.shape) == 2:
            image.reshape(image.shape[0], image.shape[1], 1)

        reshaped = image.reshape(image.shape[0] * image.shape[1], image.shape[2])

        kmeans = KMeans(n_clusters=numClusters, n_init=40, max_iter=500).fit(reshaped)
        clustering = np.reshape(np.array(kmeans.labels_, dtype=np.uint8), (image.shape[0], image.shape[1]))

        sortedLabels = sorted([n for n in range(numClusters)], key=lambda x: -np.sum(clustering == x))
        kmeansImage = np.zeros(image.shape[:2], dtype=np.uint8)
        for i, label in enumerate(sortedLabels):
            kmeansImage[clustering == label] = int((255) / (numClusters - 1)) * i

        cv2.imwrite(self.filename + '_tempo.png', kmeansImage)
        self.filedata = PIL.Image.open(self.filename + '_tempo.png')
        self.afficeImage(self.filedata);
    def set_window_title(self, name=None):
        if name:
            self.master.title(name + " - ImageEditor")
        else:
            self.master.title("Pas enregistre - ImageEditor")

    def open_image_link (self, *args):
        if(self.filename==None or self.filename==""):self.open_file()

    def open_image_link2(self, *args):
        self.open_file()

    def open_file(self, *args):
        tempfn = askopenfilename(
            defaultextension=".txt",
            filetypes=[("Tous les Fichier", "*.*"),
                       ("Bitmap monochrome", "*.bmp"),
                       ("JPG", "*.jpg"),
                       ("JPEG", "*.jpeg"),
                       ("GIF", "*.gif"),
                       ("PNG", "*.png")])
        if(tempfn != ""):self.filename = tempfn;
        if self.filename and tempfn!="":
            self.filenameorig = self.filename
            nomf = self.filename.split("/")
            copyfile(self.filename,self.tdir +nomf[len(nomf) - 1])
            self.filename = self.tdir + nomf[len(nomf) - 1]
            copyfile(self.filename,self.filename+"_tempo.png")
            self.filedata = PIL.Image.open(self.filename)
            self.afficeImage(self.filedata)
            self.master.title(self.filename + " - ImageEditor")
            self.afficheHisto()
    def afficeImage(self, dataImage):
        width = 200
        print(dataImage)
        height = int(dataImage.height * width / dataImage.width)
        img = dataImage.resize((width, height))
        img2 = PIL.ImageTk.PhotoImage(img)
        self.image.configure(image=img2)
        self.image.image = img2
    def afficheHisto(self):

        self.frame_opcT = LabelFrame(self.master, text="Description");
        self.frame_opcT.grid(row=5, column=0, columnspan=4, padx=5, pady=5);
        cv_img = cv2.imread( self.filename + "_tempo.png")
        h,w,n = cv_img.shape
        Label(self.frame_opcT,text="Stockage: ").grid(row=0,column=0, sticky=W)
        Label(self.frame_opcT,text="%d Ko "%(os.stat(self.filename).st_size)).grid(row=0,column=1, sticky=W)
        Label(self.frame_opcT,text="Dimensions: ").grid(row=1,column=0, sticky=W)
        Label(self.frame_opcT,text="%d x %d "%(h,w)).grid(row=1,column=1, sticky=W)
        Label(self.frame_opcT,text="Histogramme").grid(row=2,column=0,columnspan=2)

        hsv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
        cv_img = cv2.cvtColor(cv2.imread( self.filename + "_tempo.png"), cv2.COLOR_BGR2RGB)

        color = ('r', 'g', 'b')
        labels = ('h', 's', 'v')

        f = Figure(figsize=(5, 5), dpi=60)
        a = f.add_subplot(111)
        for i, col in enumerate(color):
            hist = cv2.calcHist([hsv], [i], None, [256], [0, 256])
            a.plot(hist, color=col, label=labels[i])
        if(self.canvas != None):self.canvas.get_tk_widget().destroy();
        self.canvas = FigureCanvasTkAgg(f, master=self.frame_opcT)

        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, sticky="NS")
        self.canvas.draw()

        vsbar = tk.Scrollbar(self.frame_opcT, orient=tk.VERTICAL, command=self.canvas.get_tk_widget().yview)
        vsbar.grid(row=3, column=2, sticky=tk.NS)

    def save(self, *args):
        if self.filename and self.filename != "":
            try:
                copyfile(self.filename+"_tempo.png", self.filenameorig)
            except Exception as e:
                print(e)


    def save_as(self, *args):
        if self.filename and self.filename != "":
            try:
                ext = self.filename.split(".")
                nomf = self.filename.split("/")
                new_file = asksaveasfilename(
                    initialfile=nomf[len(nomf)-1],
                    defaultextension="."+ext[1],
                    filetypes=[("Bitmap monochrome", "*.bmp"),
                               ("JPG", "*.jpg"),
                               ("JPEG", "*.jpeg"),
                               ("GIF", "*.gif"),
                               ("PNG", "*.png")])
                if new_file != "":
                    self.set_window_title(new_file)
                    self.filenameorig = new_file
                    copyfile(self.filename+"_tempo.png", self.filenameorig)

            except Exception as e:
                print(e)



if __name__ == "__main__":
    master = tk.Tk()
    pt = ImageEditeur(master)
    master.mainloop()

