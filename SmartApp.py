# Python Version: 3.7.3
# Modules:
# Pillow 6.1.0
# Matplotlib 3.1.1
# Numpy 1.20.2
# Opencv_python 4.5.1.48
# Scipy 1.6.2

import tkinter as tk
import numpy as np
import time, sys, os, cv2, datetime, matplotlib
from tkinter import ttk, Tk, Label, Button, StringVar
from PIL import ImageDraw, Image, ImageTk
from tkinter.filedialog import askdirectory
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import webbrowser
matplotlib.use("TkAgg")

LARGE_FONT = ("Verdana", 12)
#Global Variables list:
global_variables = []
IP_adress = ['"None"']
global_photos_coordinates = ['"None"']
global_photos_folder = ['"None"']
global_input_interval = ['"None"','"None"']
global_process = []
global_counter_manual = []

class SmartAPP(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        tk.Tk.iconbitmap(self, default = 'mainicon.ico')
        tk.Tk.wm_title(self, 'Smartphotometer Application')
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage,MainPage_Automatizated,
                  ThirdPage_Automatizated, MainPage_Manual,
                  ThirdPage_Manual, MainPage_FolderData, Help):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Smartphotometer Application", font=LARGE_FONT)
        label.pack(pady=20, padx=10)

        button1 = ttk.Button(self, width=30, text="Automatized Process",
                           command=lambda: controller.show_frame(MainPage_Automatizated))
        button1.pack(pady=10, padx=10)

        button4 = ttk.Button(self, width=30, text='Manual Process',
                             command=lambda: controller.show_frame(MainPage_Manual))
        button4.pack(pady=10, padx=10)

        button2 = ttk.Button(self, width=30,text="Photo Set Process",
                           command=lambda: controller.show_frame(MainPage_FolderData))
        button2.pack(pady=10, padx=10)

        button3 = ttk.Button(self, width=30,text="Help",
                            command=lambda: controller.show_frame(Help))
        button3.pack(pady=10, padx=10)

        label2 = tk.Label(self, text="version: 1.0")
        label2.pack(pady=20, padx=10, side = tk.BOTTOM)

        '''def restart():
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        button5 = ttk.Button(self, width=20, text="Restart Program",
                             command=restart)
        button5.pack(pady=10, padx=10, side=tk.BOTTOM)'''

class MainPage_Automatizated(tk.Frame):
    def __init__(self, parent, controller):
        def Create_file():
            init_time = time.time()
            global global_input_interval
            photos_interval = global_input_interval[-2]
            ttotal_photos = global_input_interval[-1]
            photos_number = int((float(ttotal_photos) / float(photos_interval)) + 1)

            global global_photos_coordinates
            x1 = int(global_photos_coordinates[-4])
            y1 = int(global_photos_coordinates[-3])
            x2 = int(global_photos_coordinates[-2])
            y2 = int(global_photos_coordinates[-1])

            global global_photos_folder
            txt_file = os.path.join(global_photos_folder[-2] + "\\", 'report.txt')
            with open(txt_file, "w") as f:
                f.write(str('Time') + '\t')
                f.write(str('Intensity') + '\t')
                f.write(str('Intensity') + '\t')
                f.write(str('Intensity') + '\n')
                f.write(str('min') + '\t')
                f.write('\t')
                f.write('\t')
                f.write('\n')
                f.write('\t')
                f.write(str('Red Intensity') + '\t')
                f.write(str('Green Intensity') + '\t')
                f.write(str('Blue Intensity') + '\n')
            x_axis = []
            Intensity_r = []
            Intensity_g = []
            Intensity_b = []
            time_initial = 0
            x1_counter = x1
            y1_counter = y1
            global global_process
            global_process.extend([init_time, photos_interval,ttotal_photos,photos_number,x1,y1,x2,y2,txt_file,x_axis,Intensity_r,Intensity_g,Intensity_b,time_initial,x1_counter,y1_counter])
            controller.show_frame(ThirdPage_Automatizated)

        def Interval():
            interval = interval_entry.get()
            ttotal = ttotal_entry.get()
            global global_input_interval
            global_input_interval.extend([interval, ttotal])
            Create_file()

        def LoadFolder():
            directory = askdirectory()
            now = datetime.datetime.now()
            folder1_created = 'SP '+now.strftime("%Y-%m-%d %H.%M")
            folder2_created = 'Photos'
            global global_photos_folder
            global_photos_folder.extend([directory,directory+'//'+folder1_created,directory+'//'+folder1_created+'//'+folder2_created])
            os.makedirs(directory+'//'+folder1_created+'//'+folder2_created)

        def IP():
            a = IP_entry.get()
            global IP_adress
            IP_adress.append('http://'+str(a))

        def Get_frame():
            global IP_adress
            cam = cv2.VideoCapture(str(IP_adress[-1])+'//video')
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
            img_name = "first_frame.png"
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            cam.release()
            cv2.destroyAllWindows()
            X = []
            Y = []

            def click_event(event, x, y, flags, params):
                if event == cv2.EVENT_LBUTTONDOWN:
                    X.append(x)
                    Y.append(y)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img, (str(len(X))), (x, y), font,
                                1, (255, 0, 0), 2)
                    if len(X) == 2:
                        start_point = (X[0],Y[0])
                        end_point = (X[1], Y[1])
                        image = cv2.rectangle(img, start_point, end_point, (255,0,0), 2)
                    cv2.imshow('image', img)

            if __name__ == "__main__":
                img = cv2.imread('first_frame.png', 1)
                cv2.namedWindow("image", cv2.WINDOW_NORMAL)
                cv2.imshow('image', img)
                cv2.setMouseCallback('image', click_event)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            x1_entry.delete(0, tk.END)
            y1_entry.delete(0, tk.END)
            x2_entry.delete(0, tk.END)
            y2_entry.delete(0, tk.END)
            x1_entry.insert(0,str(X[0]))
            y1_entry.insert(0,str(Y[0]))
            x2_entry.insert(0,str(X[1]))
            y2_entry.insert(0,str(Y[1]))

        def Next_frame():
            global global_photos_coordinates
            x1 = x1_entry.get()
            y1 = y1_entry.get()
            x2 = x2_entry.get()
            y2 = y2_entry.get()
            global_photos_coordinates.extend([x1,y1,x2,y2])
            Interval()

        tk.Frame.__init__(self, parent)

        button1 = ttk.Button(self, text="Home Page", command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10)
        label = tk.Label(self, text="Automatized Process", font=LARGE_FONT)
        label.pack(pady=20)

        group_1 = tk.LabelFrame(self, padx=43, pady=10,
                                text="1. Enter Camera's IP")
        group_1.pack(padx=10, pady=5)

        labe2 = Label(group_1, text='http://')
        labe2.grid(row=2, column=0)
        IP_entry = tk.Entry(group_1, width=20)
        IP_entry.grid(row=2, column=1)
        IP_entry.insert(0, '192.168.0.2:8080')
        button4 = ttk.Button(group_1, text="Enter", command=IP)
        button4.grid(row=2, column=2)

        group_2 = tk.LabelFrame(self, padx=115, pady=10,
                                text="2. Select Area")
        group_2.pack(padx=10, pady=5)
        frame_button = ttk.Button(group_2, text='Get Frame', command=Get_frame)
        frame_button.grid(row=3, column=2, pady=10, padx=10)

        group_3 = tk.LabelFrame(self, padx=80, pady=10,
                                text="3. Coordinates")
        group_3.pack(padx=10, pady=5)

        label3 = tk.Label(group_3, text="X1")
        label3.grid(row=5, column=0)
        x1_entry = tk.Entry(group_3, width=10)
        x1_entry.grid(row=5, column=1)
        label4 = tk.Label(group_3, text="Y1")
        label4.grid(row=6, column=0)
        y1_entry = tk.Entry(group_3, width=10)
        y1_entry.grid(row=6, column=1)
        label5 = tk.Label(group_3, text="X2")
        label5.grid(row=5, column=3)
        x2_entry = tk.Entry(group_3, width=10)
        x2_entry.grid(row=5, column=4)
        label6 = tk.Label(group_3, text="Y2")
        label6.grid(row=6, column=3)
        y2_entry = tk.Entry(group_3, width=10)
        y2_entry.grid(row=6, column=4)

        group_4 = tk.LabelFrame(self, padx=125, pady=10,
                                text="4. Select the folder's path")
        group_4.pack(padx=10, pady=5)

        button5 = ttk.Button(group_4, text="Browse", command=LoadFolder)
        button5.pack()

        group_5 = tk.LabelFrame(self, padx=48, pady=10,
                                text="5. Enter the respective values")
        group_5.pack(padx=10, pady=5)

        label9 = tk.Label(group_5, text="Interval between photos (min)")
        label9.grid(row=8, column=0)
        interval_entry = tk.Entry(group_5, width=10)
        interval_entry.grid(row=8, column=1)
        label10 = tk.Label(group_5, text='Total monitoring time (min)')
        label10.grid(row=9, column=0)
        ttotal_entry = tk.Entry(group_5, width=10)
        ttotal_entry.grid(row=9,column=1)

        button5 = ttk.Button(self, text="Next", command=Next_frame)
        button5.pack(pady=40, padx=10)

f_auto = Figure(figsize=(2,2), dpi=100)
a_auto = f_auto.add_subplot(111)
Axis_y=[1]
def animate_auto(i):
    try:
        global global_photos_folder
        txt_file = os.path.join(global_photos_folder[-2] + "\\", 'report.txt')
        file = txt_file
        file1 = open(file, "r")
        for i in range(3):
            file1.readline()
        time_initial = []
        Red = []
        Green = []
        Blue = []
        counter = 0
        while counter == 0:
            try:
                term = file1.readline().split()
                time_initial.append((float(term[0])))
                Red.append((float(term[1])))
                Green.append((float(term[2])))
                Blue.append((float(term[3])))
            except IndexError:
                counter = 1
        if len(time_initial) != len(Red):
            time_initial.pop()

        a_auto.clear()
        if int(Axis_y[-1]) == 1:
            a_auto.plot(time_initial,Red, 'ro')
            a_auto.plot(time_initial, Green, 'go')
            a_auto.plot(time_initial, Blue, 'bo')
        if int(Axis_y[-1]) == 2:
            a_auto.plot(time_initial,Red, 'ro')
        if int(Axis_y[-1]) == 3:
            a_auto.plot(time_initial,Green, 'go')
        if int(Axis_y[-1]) == 4:
            a_auto.plot(time_initial,Blue, 'bo')
        #plt.legend(title='Time (min)', bbox_to_anchor=(0.5, -0.05), loc='upper left', frameon=False)

    except:
        pass

class ThirdPage_Automatizated(tk.Frame):
    def __init__(self, parent, controller):
        counter = []
        initial_time = [0]

        def Process():
            if len(counter)==0:
                initial_time.append(time.time())
                print(initial_time)
            global global_process
            excluded, photos_interval, ttotal_photos, photos_number, x1, y1, x2, y2, txt_file, x_axis, Intensity_r, Intensity_g, Intensity_b, time_initial, x1_counter, y1_counter = global_process
            global global_input_interval
            photos_interval = float(global_input_interval[-2]) * 60
            ttotal_photos = float(global_input_interval[-1]) * 60
            photos_number = int((float(ttotal_photos) / float(photos_interval)) + 1)

            # In case a network error occurs, the following lines should solve the problem
            ret = False
            while ret == False:
                cam = cv2.VideoCapture(IP_adress[-1] + '//video')
                ret, frame = cam.read()
                if ret == False:
                    print("Conection Error")
            if not ret:
                print("Fatal Error")

            now = datetime.datetime.now()
            now2 = now.strftime("%Y-%m-%d %H.%M.%S")
            img_name = global_photos_folder[-1] + ("\\"+now2+".png")
            cv2.imwrite(img_name, frame)
            actual_initial_time = time.time() - initial_time[-1]
            selected_folder = global_photos_folder[-1]
            folder_last_file = (os.listdir(selected_folder)[-1])
            try:
                img = Image.open(selected_folder + '\\' + folder_last_file)
            except OSError:
                folder_last_file = (os.listdir(selected_folder)[-2])
                img = Image.open(selected_folder + '\\' + folder_last_file)
            ary = np.array(img)
            actual_initial_time = (float(time.time()) - float(initial_time[-1]))/60
            x_axis.append(actual_initial_time)

            r, g, b = np.split(ary, 3, axis=2)

            for i in range(3):
                y1 = y1_counter
                if i == 0:
                    channel_r = []
                    while y1 <= y2:
                        while x1 <= x2:
                            channel_r.append(r[y1, x1])
                            x1 += 1
                        y1 += 1
                        x1 = x1_counter
                    pixels_mean_r = np.mean(channel_r)
                    Intensity_r.append(pixels_mean_r)
                if i == 1:
                    channel_g = []
                    while y1 <= y2:
                        while x1 <= x2:
                            channel_g.append(g[y1, x1])
                            x1 += 1
                        y1 += 1
                        x1 = x1_counter
                    pixels_mean_g = np.mean(channel_g)
                    Intensity_g.append(pixels_mean_g)
                if i == 2:
                    channel_b = []
                    while y1 <= y2:
                        while x1 <= x2:
                            channel_b.append(b[y1, x1])
                            x1 += 1
                        y1 += 1
                        x1 = x1_counter
                    pixels_mean_b = np.mean(channel_b)
                    Intensity_b.append(pixels_mean_b)
            with open(txt_file, 'a') as f:
                f.write(str(x_axis[-1]) + '\t')
                f.write(str(Intensity_r[-1]) + '\t')
                f.write(str(Intensity_g[-1]) + '\t')
                f.write(str(Intensity_b[-1]) + '\n')

            if len (counter) < (photos_number-1):
                actual_initial_time = time.time() - initial_time[-1]
                interval = (float((int(len(counter))+1)*(float(photos_interval))) - float(actual_initial_time))*1000
                print(int(len(counter))+1,float(photos_interval),float(actual_initial_time))
                counter.append('a')
                print(interval)
                self.after(int(interval), Process)
            print(x_axis, Intensity_r)


        tk.Frame.__init__(self, parent)
        button1 = ttk.Button(self, text="Home Page", command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10)
        button4 = tk.Button(self, height=2, width=15, text="Start Kinetics", font=12, command=Process)
        button4.pack(pady=20)

        def RGB_graph():
            global Axis_y
            Axis_y.append(1)
        def Red_graph():
            global Axis_y
            Axis_y.append(2)
        def Green_graph():
            global Axis_y
            Axis_y.append(3)
        def Blue_graph():
            global Axis_y
            Axis_y.append(4)

        which_fit = []
        def zero_button():
            which_fit.append(0)
            Fitting()
        def first_button():
            which_fit.append(1)
            Fitting()
        def second_button():
            which_fit.append(2)
            Fitting()

        def Fitting():
            order = (which_fit[-1])
            def zeroth_order(x, k, Ai):
                return Ai - k * x
            def first_order(x, k, Ai, Af):
                return Af + (Ai - Af) * np.exp(-k * x)
            def second_order(x, k, Ai, Af):
                #return Ai / (1 + Ai * k * x)
                if Ai > Af:
                    return 1 / ((1 / (Ai - Af)) + k * x) + Af
                if Af > Ai:
                    return Af - 1 / ((1 / (Af - Ai)) + k * x)

            global global_photos_folder
            txt_file = os.path.join(global_photos_folder[-2] + "\\", 'report.txt')
            file = txt_file
            file1 = open(file, "r")
            for i in range(3):
                file1.readline()
            time_initial = []
            Red = []
            Green = []
            Blue = []
            counter = 0
            while counter == 0:
                try:
                    term = file1.readline().split()
                    time_initial.append((float(term[0])))
                    Red.append((float(term[1])))
                    Green.append((float(term[2])))
                    Blue.append((float(term[3])))
                except IndexError:
                    counter = 1
            if len(time_initial) != len(Red):
                time_initial.pop()
            xData = np.asarray(time_initial)
            if int(Axis_y[-1]) == 2:
                yData = np.asarray(Red)
                dot = 'ro'
                legend_color = 'Red'
            if int(Axis_y[-1]) == 3:
                yData = np.asarray(Green)
                dot = 'go'
                legend_color = 'Green'
            if int(Axis_y[-1]) == 4:
                yData = np.asarray(Blue)
                dot = 'bo'
                legend_color = 'Blue'
            if order == 0:
                initialGuess = [0.01, yData[0]]
                popt, pcov = curve_fit(zeroth_order, xData, yData, initialGuess)
                residuals = yData - zeroth_order(xData, *popt)
                ss_res = np.sum(residuals ** 2)
                ss_tot = np.sum((yData - np.mean(yData)) ** 2)
                r2 = 1 - (ss_res / ss_tot)
                # Plot experimental data points
                plt.plot(xData, yData, dot, label='Data')
                plt.plot([], [], ' ', label='0$^{th}$ Order Fit:')
                # x values for the fitted function
                xFit = np.arange(0.0, xData[-1],0.1)
                # Plot the fitted function
                k, ai = str("{:.4E}".format(float(popt[0]))), str("{:.4f}".format(float(popt[1])))
                plt.plot(xFit, zeroth_order(xFit, *popt), 'k', label='Parameters:\nk='+k+'\n[A]\u2080='+ai)
                plt.plot([], [], ' ', label='R-Square:\n' + str("%.4f" % r2))
                plt.xlabel('Time (min)')
                plt.ylabel(legend_color+' Channel Intensity')
                plt.subplots_adjust(right=0.75)
                plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5))
                plt.show()
                xData = []
                yData = []

            if order == 1:
                initialGuess = [0.01, yData[0], yData[-1]]
                popt, pcov = curve_fit(first_order, xData, yData, initialGuess)
                residuals = yData - first_order(xData, *popt)
                ss_res = np.sum(residuals ** 2)
                ss_tot = np.sum((yData - np.mean(yData)) ** 2)
                r2 = 1 - (ss_res / ss_tot)
                # Plot experimental data points
                plt.plot(xData, yData, dot, label='Data')
                plt.plot([], [], ' ', label='1$^{st}$ Order Fit')
                # x values for the fitted function
                xFit = np.arange(0.0, xData[-1],0.1)
                # Plot the fitted function
                k, ai, af = str("{:.4E}".format(float(popt[0]))), str("{:.4f}".format(float(popt[1]))),str("{:.4f}".format(float(popt[2])))
                plt.plot(xFit, first_order(xFit, *popt), 'k',
                         label='Parameters:\nk='+k+'\n[A]\u2080='+ai+'\n[A]f='+af)
                plt.plot([], [], ' ', label='R-Square:\n' + str("%.4f" % r2))
                plt.xlabel('Time (min)')
                plt.ylabel(legend_color+' Channel Intensity')
                plt.subplots_adjust(right=0.75)
                plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5))
                plt.show()
                xData = []
                yData = []
            if order == 2:
                initialGuess = [0.01, yData[0], yData[-1]]
                popt, pcov = curve_fit(second_order, xData, yData, initialGuess,bounds=((0, 0, 0), (10, 255, 255)))
                residuals = yData - second_order(xData, *popt)
                ss_res = np.sum(residuals ** 2)
                ss_tot = np.sum((yData - np.mean(yData)) ** 2)
                r2 = 1 - (ss_res / ss_tot)
                # Plot experimental data points
                plt.plot(xData, yData, dot, label='Data')
                plt.plot([], [], ' ', label='2$^{nd}$ Order Fit:')
                # x values for the fitted function
                xFit = np.arange(0.0, xData[-1],0.1)
                # Plot the fitted function
                k, ai, af = str("{:.4E}".format(float(popt[0]))), str("{:.4f}".format(float(popt[1]))),str("{:.4f}".format(float(popt[2])))
                plt.plot(xFit, second_order(xFit, *popt), 'k', label='Parameters:\nk='+k+'\n[A]\u2080='+ai+'\n[A]f='+af)
                plt.plot([], [], ' ', label='R-Square:\n' + str("%.4f" % r2))
                plt.xlabel('Time (min)')
                plt.ylabel(legend_color+' Channel Intensity')
                plt.subplots_adjust(right=0.75)
                plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5))
                plt.show()
                xData = []
                yData = []

        def open_report ():
            import subprocess
            global global_photos_folder
            text_file = os.path.join(global_photos_folder[-2] + "\\", 'report.txt')
            report_file = text_file
            try:
                subprocess.Popen(["notepad", report_file])
            except:
                pass

        group_1 = tk.LabelFrame(self, padx=15, pady=10,
                                text="Show graph")
        group_1.pack(padx=10, pady=5)

        button5 = ttk.Button(group_1, text='RGB', command = RGB_graph)
        button5.grid(row=0,column=0)
        button6 = ttk.Button(group_1, text='Channel R', command=Red_graph)
        button6.grid(row=0,column=1)
        button7 = ttk.Button(group_1, text='Channel G', command=Green_graph)
        button7.grid(row=0,column=2)
        button8 = ttk.Button(group_1, text='Channel B', command=Blue_graph)
        button8.grid(row=0,column=3)

        group_00 = tk.LabelFrame(self, padx=15, pady=10, borderwidth=0)
        group_00.pack(padx=10, pady=5)

        group_4 = tk.LabelFrame(group_00, padx=15, pady=10, text='Fit curve')
        group_4.grid(row=0, column=0)
        button9 = ttk.Button(group_4, text='Zero order', command=zero_button)
        button9.grid(row=0, column=0)
        button10 = ttk.Button(group_4, text='First order', command=first_button)
        button10.grid(row=0, column=1)
        button11 = ttk.Button(group_4, text='Second order', command=second_button)
        button11.grid(row=0, column=2)

        group_11 = tk.LabelFrame(group_00, padx=15, pady=10,
                                 text="Text Report")
        group_11.grid(row=0, column=1)
        button21 = ttk.Button(group_11, text="Open", command=open_report)
        button21.pack()



        canvas = FigureCanvasTkAgg(f_auto, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # a.clear()
        #ani = animation.FuncAnimation(f, Red_graph, 1000)
        label_end = tk.Label(self, bg='white', text="Time (min)", font=12)
        label_end.pack()

class MainPage_Manual(tk.Frame):
    def __init__(self, parent, controller):
        def Create_file():
            global global_input_interval

            global global_photos_coordinates
            x1 = int(global_photos_coordinates[-4])
            y1 = int(global_photos_coordinates[-3])
            x2 = int(global_photos_coordinates[-2])
            y2 = int(global_photos_coordinates[-1])

            global global_photos_folder
            txt_file = os.path.join(global_photos_folder[-2] + "\\", 'report.txt')
            with open(txt_file, "w") as f:
                f.write(str('X') + '\t')
                f.write(str('Intensity') + '\t')
                f.write(str('Intensity') + '\t')
                f.write(str('Intensity') + '\n')
                f.write('\t')
                f.write('\t')
                f.write('\t')
                f.write('\n')
                f.write('\t')
                f.write(str('Red Intensity') + '\t')
                f.write(str('Green Intensity') + '\t')
                f.write(str('Blue Intensity') + '\n')
            x_axis = []
            Intensity_r = []
            Intensity_g = []
            Intensity_b = []
            time_initial = 0
            x1_counter = x1
            y1_counter = y1
            global global_process
            global_process.extend([x1,y1,x2,y2,txt_file,x_axis,Intensity_r,Intensity_g,Intensity_b,time_initial,x1_counter,y1_counter])
            controller.show_frame(ThirdPage_Manual)

        def Interval():
            interval = interval_entry.get()
            global global_input_interval
            global_input_interval.extend([interval])
            Create_file()

        def LoadFolder():
            directory = askdirectory()
            now = datetime.datetime.now()
            folder1_created = 'SP '+now.strftime("%Y-%m-%d %H.%M")
            folder2_created = 'Photos'
            #directory_path.set('Folder: '+directory+'/'+folder1_created)
            global global_photos_folder
            global_photos_folder.extend([directory,directory+'//'+folder1_created,directory+'//'+folder1_created+'//'+folder2_created])
            os.makedirs(directory+'//'+folder1_created+'//'+folder2_created)

        def IP():
            a = IP_entry.get()
            global IP_adress
            IP_adress.append('http://' + str(a))

        def Get_frame():
            global IP_adress
            cam = cv2.VideoCapture(str(IP_adress[-1]) + '//video')
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
            img_name = "first_frame.png"
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            cam.release()
            cv2.destroyAllWindows()
            X = []
            Y = []

            def click_event(event, x, y, flags, params):
                # checking for left mouse clicks
                if event == cv2.EVENT_LBUTTONDOWN:
                    X.append(x)
                    Y.append(y)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img, (str(len(X))), (x, y), font,
                                1, (255, 0, 0), 2)
                    if len(X) == 2:
                        start_point = (X[0], Y[0])
                        end_point = (X[1], Y[1])
                        image = cv2.rectangle(img, start_point, end_point, (255, 0, 0), 2)
                    cv2.imshow('image', img)

            if __name__ == "__main__":
                img = cv2.imread('first_frame.png', 1)
                cv2.namedWindow("image", cv2.WINDOW_NORMAL)
                cv2.imshow('image', img)
                cv2.setMouseCallback('image', click_event)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            x1_entry.delete(0, tk.END)
            y1_entry.delete(0, tk.END)
            x2_entry.delete(0, tk.END)
            y2_entry.delete(0, tk.END)
            x1_entry.insert(0, str(X[0]))
            y1_entry.insert(0, str(Y[0]))
            x2_entry.insert(0, str(X[1]))
            y2_entry.insert(0, str(Y[1]))

        def Next_frame():
            global global_photos_coordinates
            x1 = x1_entry.get()
            y1 = y1_entry.get()
            x2 = x2_entry.get()
            y2 = y2_entry.get()
            global_photos_coordinates.extend([x1, y1, x2, y2])
            Interval()

        tk.Frame.__init__(self, parent)
        button1 = ttk.Button(self, text="Home Page", command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10)
        label = tk.Label(self, text="Manual Process", font=LARGE_FONT)
        label.pack(pady=20)

        group_1 = tk.LabelFrame(self, padx=43, pady=10,
                                text="1. Enter Camera's IP")
        group_1.pack(padx=10, pady=5)

        labe2 = Label(group_1, text='http://')
        labe2.grid(row=2, column=0)
        IP_entry = tk.Entry(group_1, width=20)
        IP_entry.grid(row=2, column=1)
        IP_entry.insert(0, '192.168.0.2:8080')
        button4 = ttk.Button(group_1, text="Enter", command=IP)
        button4.grid(row=2, column=2)

        group_2 = tk.LabelFrame(self, padx=115, pady=10,
                                text="2. Select Area")
        group_2.pack(padx=10, pady=5)
        frame_button = ttk.Button(group_2, text='Get Frame', command=Get_frame)
        frame_button.grid(row=3, column=2, pady=10, padx=10)

        group_3 = tk.LabelFrame(self, padx=80, pady=10,
                                text="3. Coordinates")
        group_3.pack(padx=10, pady=5)

        label3 = tk.Label(group_3, text="X1")
        label3.grid(row=5, column=0)
        x1_entry = tk.Entry(group_3, width=10)
        x1_entry.grid(row=5, column=1)
        label4 = tk.Label(group_3, text="Y1")
        label4.grid(row=6, column=0)
        y1_entry = tk.Entry(group_3, width=10)
        y1_entry.grid(row=6, column=1)
        label5 = tk.Label(group_3, text="X2")
        label5.grid(row=5, column=3)
        x2_entry = tk.Entry(group_3, width=10)
        x2_entry.grid(row=5, column=4)
        label6 = tk.Label(group_3, text="Y2")
        label6.grid(row=6, column=3)
        y2_entry = tk.Entry(group_3, width=10)
        y2_entry.grid(row=6, column=4)

        group_4 = tk.LabelFrame(self, padx=125, pady=10,
                                text="4. Select the folder's path")
        group_4.pack(padx=10, pady=5)

        button5 = ttk.Button(group_4, text="Browse", command=LoadFolder)
        button5.pack()

        group_5 = tk.LabelFrame(self, padx=121, pady=10,
                                text="5. Enter value")
        group_5.pack(padx=10, pady=5)

        label9 = tk.Label(group_5, text="\u0394x")
        label9.grid(row=8, column=0)
        interval_entry = tk.Entry(group_5, width=10)
        interval_entry.grid(row=8, column=1)

        button5 = ttk.Button(self, text="Next", command=Next_frame)
        button5.pack(pady=40, padx=10)

f_manu = Figure(figsize=(2,2), dpi=100)
a_manu = f_manu.add_subplot(111)
Axis_y=[1]
def animate_manu(i):
    try:
        global global_photos_folder
        txt_file = os.path.join(global_photos_folder[-2] + "\\", 'report.txt')
        file = txt_file
        file1 = open(file, "r")
        for i in range(3):
            file1.readline()
        time_initial = []
        Red = []
        Green = []
        Blue = []
        counter = 0
        while counter == 0:
            try:
                term = file1.readline().split()
                time_initial.append((float(term[0])))
                Red.append((float(term[1])))
                Green.append((float(term[2])))
                Blue.append((float(term[3])))
            except IndexError:
                counter = 1
        if len(time_initial) != len(Red):
            time_initial.pop()

        a_manu.clear()
        if int(Axis_y[-1]) == 1:
            a_manu.plot(time_initial,Red, 'ro')
            a_manu.plot(time_initial, Green, 'go')
            a_manu.plot(time_initial, Blue, 'bo')
        if int(Axis_y[-1]) == 2:
            a_manu.plot(time_initial,Red, 'ro')
        if int(Axis_y[-1]) == 3:
            a_manu.plot(time_initial,Green, 'go')
        if int(Axis_y[-1]) == 4:
            a_manu.plot(time_initial,Blue, 'bo')
    except:
        pass

class ThirdPage_Manual(tk.Frame):
    def __init__(self, parent, controller):
        def Process():
            global global_input_interval
            photos_interval = int(global_input_interval[-1])

            global global_process
            x1, y1, x2, y2, txt_file, x_axis, Intensity_r, Intensity_g, Intensity_b, time_initial, x1_counter, y1_counter = global_process
            cam = cv2.VideoCapture(IP_adress[-1] + '//video')
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
            now = datetime.datetime.now()
            now2 = now.strftime("%Y-%m-%d %H.%M.%S")
            img_name = global_photos_folder[-1] + ("\\"+now2+".png")
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            selected_folder = global_photos_folder[-1]
            folder_last_file = (os.listdir(selected_folder)[-1])
            try:
                img = Image.open(selected_folder + '\\' + folder_last_file)
            except OSError:
                folder_last_file = (os.listdir(selected_folder)[-2])
                img = Image.open(selected_folder + '\\' + folder_last_file)
            ary = np.array(img)

            global global_counter_manual
            x_axis.append(photos_interval*len(global_counter_manual))
            global_counter_manual.append(['0'])

            r, g, b = np.split(ary, 3, axis=2)

            for i in range(3):
                y1 = y1_counter
                if i == 0:
                    channel_r = []
                    while y1 <= y2:
                        while x1 <= x2:
                            channel_r.append(r[y1, x1])
                            x1 += 1
                        y1 += 1
                        x1 = x1_counter
                    pixels_mean_r = np.mean(channel_r)
                    Intensity_r.append(pixels_mean_r)
                if i == 1:
                    channel_g = []
                    while y1 <= y2:
                        while x1 <= x2:
                            channel_g.append(g[y1, x1])
                            x1 += 1
                        y1 += 1
                        x1 = x1_counter
                    pixels_mean_g = np.mean(channel_g)
                    Intensity_g.append(pixels_mean_g)
                if i == 2:
                    channel_b = []
                    while y1 <= y2:
                        while x1 <= x2:
                            channel_b.append(b[y1, x1])
                            x1 += 1
                        y1 += 1
                        x1 = x1_counter
                    pixels_mean_b = np.mean(channel_b)
                    Intensity_b.append(pixels_mean_b)
            with open(txt_file, 'a') as f:
                f.write(str(x_axis[-1]) + '\t')
                f.write(str(Intensity_r[-1]) + '\t')
                f.write(str(Intensity_g[-1]) + '\t')
                f.write(str(Intensity_b[-1]) + '\n')

            plt.xlabel('Tempo')
            plt.ylabel('Intensity')
            print(x_axis, Intensity_r)

        tk.Frame.__init__(self, parent)
        button1 = ttk.Button(self, text="Home Page", command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10)
        button4 = tk.Button(self, height=2, width=15, text="Take Picture", font=12, command=Process)
        button4.pack(pady=20)

        def RGB_graph():
            global Axis_y
            Axis_y.append(1)
        def Red_graph():
            global Axis_y
            Axis_y.append(2)
        def Green_graph():
            global Axis_y
            Axis_y.append(3)
        def Blue_graph():
            global Axis_y
            Axis_y.append(4)

        which_fit = []
        def zero_button():
            which_fit.append(0)
            Fitting()

        def Fitting():
            # Fitting function
            order = (which_fit[-1])

            def zeroth_order(x, k, Ai):
                return k * x + Ai

            global global_photos_folder
            txt_file = os.path.join(global_photos_folder[-2] + "\\", 'report.txt')
            file = txt_file
            file1 = open(file, "r")
            for i in range(3):
                file1.readline()
            time_initial = []
            Red = []
            Green = []
            Blue = []
            counter = 0
            while counter == 0:
                try:
                    term = file1.readline().split()
                    time_initial.append((float(term[0])))
                    Red.append((float(term[1])))
                    Green.append((float(term[2])))
                    Blue.append((float(term[3])))
                except IndexError:
                    counter = 1
            if len(time_initial) != len(Red):
                time_initial.pop()
            xData = np.asarray(time_initial)
            if int(Axis_y[-1]) == 2:
                yData = np.asarray(Red)
                dot = 'ro'
                legend_color = 'Red'
            if int(Axis_y[-1]) == 3:
                yData = np.asarray(Green)
                dot = 'go'
                legend_color = 'Green'
            if int(Axis_y[-1]) == 4:
                yData = np.asarray(Blue)
                dot = 'bo'
                legend_color = 'Blue'
            if order == 0:
                initialGuess = [0.01, yData[0]]
                popt, pcov = curve_fit(zeroth_order, xData, yData, initialGuess)
                residuals = yData - zeroth_order(xData, *popt)
                ss_res = np.sum(residuals ** 2)
                ss_tot = np.sum((yData - np.mean(yData)) ** 2)
                r2 = 1 - (ss_res / ss_tot)
                # Plot experimental data points
                plt.plot(xData, yData, dot, label='Data')
                plt.plot([], [], ' ', label='Linear Fit:')
                # x values for the fitted function
                xFit = np.arange(0.0, xData[-1],0.1)
                # Plot the fitted function
                k, ai = str("{:.4E}".format(float(popt[0]))), str("{:.4f}".format(float(popt[1])))
                plt.plot(xFit, zeroth_order(xFit, *popt), 'k', label='Equation:\ny = x*'+k+' + '+ai+'\n')
                plt.plot([], [], ' ', label='R-Square:\n' + str("%.4f" % r2))
                plt.xlabel('X')
                plt.ylabel(legend_color+' Channel Intensity')
                plt.subplots_adjust(right=0.75)
                plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5))
                plt.show()
                xData = []
                yData = []

        def open_report ():
            import subprocess
            global global_photos_folder
            text_file = os.path.join(global_photos_folder[-2] + "\\", 'report.txt')
            report_file = text_file
            try:
                subprocess.Popen(["notepad", report_file])
            except:
                pass



        group_1 = tk.LabelFrame(self, padx=15, pady=10,
                                text="Show graph")
        group_1.pack(padx=10, pady=5)

        button5 = ttk.Button(group_1, text='RGB', command=RGB_graph)
        button5.grid(row=0, column=0)
        button6 = ttk.Button(group_1, text='Channel R', command=Red_graph)
        button6.grid(row=0, column=1)
        button7 = ttk.Button(group_1, text='Channel G', command=Green_graph)
        button7.grid(row=0, column=2)
        button8 = ttk.Button(group_1, text='Channel B', command=Blue_graph)
        button8.grid(row=0, column=3)

        group_00 = tk.LabelFrame(self, padx=15, pady=10, borderwidth=0)
        group_00.pack(padx=10, pady=5)

        group_2 = tk.LabelFrame(group_00, padx=15, pady=10, text='Fit data')
        group_2.grid(row=0, column=0)
        button9 = ttk.Button(group_2, text='Linear fit', command=zero_button)
        button9.grid(row=0, column=0)
        group_11 = tk.LabelFrame(group_00, padx=15, pady=10,
                                 text="Text Report")
        group_11.grid(row=0, column=1)
        button21 = ttk.Button(group_11, text="Open", command=open_report)
        button21.pack()


        canvas = FigureCanvasTkAgg(f_manu, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


f_fold = Figure(figsize=(2,2), dpi=100)
a_fold = f_fold.add_subplot(111)
Axis_y=[1]
def animate_fold(i):
    try:
        global global_photos_folder
        folder = global_photos_folder[-1]
        txt = (global_photos_folder[-1] + "\\" + 'report.txt')
        file = txt
        file1 = open(file, "r")
        for i in range(3):
            file1.readline()
        time_initial = []
        Red = []
        Green = []
        Blue = []
        counter = 0
        while counter == 0:
            try:
                term = file1.readline().split()
                time_initial.append((float(term[0])))
                Red.append((float(term[1])))
                Green.append((float(term[2])))
                Blue.append((float(term[3])))
            except IndexError:
                counter = 1
        if len(time_initial) != len(Red):
            time_initial.pop()

        a_fold.clear()
        if int(Axis_y[-1]) == 1:
            a_fold.plot(time_initial,Red, 'ro')
            a_fold.plot(time_initial, Green, 'go')
            a_fold.plot(time_initial, Blue, 'bo')
        if int(Axis_y[-1]) == 2:
            a_fold.plot(time_initial,Red, 'ro')
        if int(Axis_y[-1]) == 3:
            a_fold.plot(time_initial,Green, 'go')
        if int(Axis_y[-1]) == 4:
            a_fold.plot(time_initial,Blue, 'bo')
    except:
        pass
class MainPage_FolderData(tk.Frame):
    path = []
    def __init__(self, parent, controller):
        counter2 = []
        def RGB_analisys():
            global global_photos_folder
            folder = global_photos_folder[-1]
            txt = (global_photos_folder[-1] + "\\"+ 'report.txt')
            photo_number = int(len(counter2))
            os.chdir(folder)
            global global_photos_coordinates
            x1 = int(global_photos_coordinates[-4])
            y1 = int(global_photos_coordinates[-3])
            x2 = int(global_photos_coordinates[-2])
            y2 = int(global_photos_coordinates[-1])
            x1_counter = x1
            y1_counter = y1
            # Gerador do eixo x
            global global_input_interval
            interval_time_initial = float(global_input_interval[-1])

            counter = 0
            Intensity_r = []
            Intensity_g = []
            Intensity_b = []

            no_file = 0
            try:
                images = (os.listdir(folder)[photo_number])
                img = Image.open(images)
                ary = np.array(img)

                # A array se divide em outras 3: R, G e B
                r, g, b = np.split(ary, 3, axis=2)

                for i in range(3):
                    y1 = y1_counter
                    if i == 0:
                        channel_r = []
                        while y1 <= y2:
                            while x1 <= x2:
                                channel_r.append(r[y1, x1])
                                x1 += 1
                            y1 += 1
                            x1 = x1_counter
                        pixels_mean_r = np.mean(channel_r)
                        Intensity_r.append(pixels_mean_r)
                    if i == 1:
                        channel_g = []
                        while y1 <= y2:
                            while x1 <= x2:
                                channel_g.append(g[y1, x1])
                                x1 += 1
                            y1 += 1
                            x1 = x1_counter
                        pixels_mean_g = np.mean(channel_g)
                        Intensity_g.append(pixels_mean_g)
                    if i == 2:
                        channel_b = []
                        while y1 <= y2:
                            while x1 <= x2:
                                channel_b.append(b[y1, x1])
                                x1 += 1
                            y1 += 1
                            x1 = x1_counter
                        pixels_mean_b = np.mean(channel_b)
                        Intensity_b.append(pixels_mean_b)
            except OSError:
                counter += 1
                no_file = 1
            if no_file == 0:
                with open(txt, 'a') as f:
                    try:
                        #for i in range((int(len(os.listdir(folder)))) - counter):
                        f.write(str(interval_time_initial * (photo_number)) + '\t')
                        f.write(str(Intensity_r[-1]) + '\t')
                        f.write(str(Intensity_g[-1]) + '\t')
                        f.write(str(Intensity_b[-1]) + '\n')
                    except IndexError:
                        pass
            counter2.append(0)
            if len(counter2)<len(os.listdir(folder)):
                self.after(100, RGB_analisys)

        def Create_file():
            global global_input_interval

            global global_photos_coordinates
            x1 = int(global_photos_coordinates[-4])
            y1 = int(global_photos_coordinates[-3])
            x2 = int(global_photos_coordinates[-2])
            y2 = int(global_photos_coordinates[-1])

            global global_photos_folder
            txt_file = os.path.join(global_photos_folder[-1] + "\\", 'report.txt')
            with open(txt_file, "w") as f:
                f.write(str('Time') + '\t')
                f.write(str('Intensity') + '\t')
                f.write(str('Intensity') + '\t')
                f.write(str('Intensity') + '\n')
                f.write(str('min') + '\t')
                f.write('\t')
                f.write('\t')
                f.write('\n')
                f.write('\t')
                f.write(str('Red Intensity') + '\t')
                f.write(str('Green Intensity') + '\t')
                f.write(str('Blue Intensity') + '\n')
            x_axis = []
            Intensity_r = []
            Intensity_g = []
            Intensity_b = []
            time_initial = 0
            x1_counter = x1
            y1_counter = y1
            global global_process
            global_process.extend([x1,y1,x2,y2,txt_file,x_axis,Intensity_r,Intensity_g,Intensity_b,time_initial,x1_counter,y1_counter])
            RGB_analisys()
        def CoordinatesCV(path_folder, path_file):
            X = []
            Y = []
            def click_event(event, x, y, flags, params):
                if event == cv2.EVENT_LBUTTONDOWN:
                    X.append(x)
                    Y.append(y)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img, (str(len(X))), (x, y), font,
                                1, (255, 0, 0), 2)
                    if len(X) == 2:
                        start_point = (X[0], Y[0])
                        end_point = (X[1], Y[1])
                        image = cv2.rectangle(img, start_point, end_point, (255, 0, 0), 2)
                    cv2.imshow('image', img)

            if __name__ == "__main__":
                img = cv2.imread(path_file, 1)
                cv2.namedWindow("image", cv2.WINDOW_NORMAL)
                cv2.imshow('image', img)
                cv2.setMouseCallback('image', click_event)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            global global_photos_coordinates
            x1 = X[0]
            y1 = Y[0]
            x2 = X[1]
            y2 = Y[1]
            global_photos_coordinates.extend([x1, y1, x2, y2])
            Create_file()
        def Interval():
            a = interval_entry.get()

            global global_input_interval
            global_input_interval.extend([a])

            global global_photos_folder
            path_folder = global_photos_folder[-1]
            file = ((os.listdir(global_photos_folder[-1])[0]))
            path_file = path_folder + '/' + file
            CoordinatesCV(path_folder, path_file)
        def LoadFolder():
            folder_name = askdirectory()
            global global_photos_folder
            global_photos_folder.append(folder_name)



        def RGB_graph():
            global Axis_y
            Axis_y.append(1)
        def Red_graph():
            global Axis_y
            Axis_y.append(2)
        def Green_graph():
            global Axis_y
            Axis_y.append(3)
        def Blue_graph():
            global Axis_y
            Axis_y.append(4)

        which_fit = []

        def zero_button():
            which_fit.append(0)
            Fitting()

        def first_button():
            which_fit.append(1)
            Fitting()

        def second_button():
            which_fit.append(2)
            Fitting()

        def Fitting():
            # Fitting function
            order = (which_fit[-1])

            def zeroth_order(x, k, Ai):
                return Ai - k * x

            def first_order(x, k, Ai, Af):
                return Af + (Ai - Af) * np.exp(-k * x)

            def second_order(x, k, Ai, Af):
                #return Ai / (1 + Ai * k * x)
                if Ai > Af:
                    return 1 / ((1 / (Ai - Af)) + k * x) + Af
                if Af > Ai:
                    return Af - 1 / ((1 / (Af - Ai)) + k * x)

            global global_photos_folder
            folder = global_photos_folder[-1]
            txt_file = (global_photos_folder[-1] + "\\" + 'report.txt')
            file = txt_file
            file1 = open(file, "r")
            for i in range(3):
                file1.readline()
            time_initial = []
            Red = []
            Green = []
            Blue = []
            counter = 0
            while counter == 0:
                try:
                    term = file1.readline().split()
                    time_initial.append((float(term[0])))
                    Red.append((float(term[1])))
                    Green.append((float(term[2])))
                    Blue.append((float(term[3])))
                except IndexError:
                    counter = 1
            if len(time_initial) != len(Red):
                time_initial.pop()
            xData = np.asarray(time_initial)
            if int(Axis_y[-1]) == 2:
                yData = np.asarray(Red)
                dot = 'ro'
                legend_color = 'Red'
            if int(Axis_y[-1]) == 3:
                yData = np.asarray(Green)
                dot = 'go'
                legend_color = 'Green'
            if int(Axis_y[-1]) == 4:
                yData = np.asarray(Blue)
                dot = 'bo'
                legend_color = 'Blue'
            if order == 0:
                initialGuess = [0.01, yData[0]]
                popt, pcov = curve_fit(zeroth_order, xData, yData, initialGuess)
                residuals = yData - zeroth_order(xData, *popt)
                ss_res = np.sum(residuals ** 2)
                ss_tot = np.sum((yData - np.mean(yData)) ** 2)
                r2 = 1 - (ss_res / ss_tot)
                # Plot experimental data points
                plt.plot(xData, yData, dot, label='Data')
                plt.plot([], [], ' ', label='0$^{th}$ Order Fit:')
                # x values for the fitted function
                xFit = np.arange(0.0, xData[-1],0.1)
                # Plot the fitted function
                k, ai = str("{:.4E}".format(float(popt[0]))), str("{:.4f}".format(float(popt[1])))
                plt.plot(xFit, zeroth_order(xFit, *popt), 'k', label='Parameters:\nk='+k+'\n[A]\u2080='+ai)
                plt.plot([], [], ' ', label='R-Square:\n' + str("%.4f" % r2))
                plt.xlabel('Time (min)')
                plt.ylabel(legend_color+' Channel Intensity')
                plt.subplots_adjust(right=0.75)
                plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5))
                plt.show()
                xData = []
                yData = []

            if order == 1:
                initialGuess = [0.01, yData[0], yData[-1]]
                popt, pcov = curve_fit(first_order, xData, yData, initialGuess)
                residuals = yData - first_order(xData, *popt)
                ss_res = np.sum(residuals ** 2)
                ss_tot = np.sum((yData - np.mean(yData)) ** 2)
                r2 = 1 - (ss_res / ss_tot)
                # Plot experimental data points
                plt.plot(xData, yData, dot, label='Data')
                plt.plot([], [], ' ', label='1$^{st}$ Order Fit')
                # x values for the fitted function
                xFit = np.arange(0.0, xData[-1],0.1)
                # Plot the fitted function
                k, ai,af = str("{:.4E}".format(float(popt[0]))), str("{:.4f}".format(float(popt[1]))),str("{:.4f}".format(float(popt[2])))
                plt.plot(xFit, first_order(xFit, *popt), 'k',
                         label='Parameters:\nk='+k+'\n[A]\u2080='+ai+'\n[A]f='+af)
                plt.plot([], [], ' ', label='R-Square:\n' + str("%.4f" % r2))
                plt.xlabel('Time (min)')
                plt.ylabel(legend_color+' Channel Intensity')
                plt.subplots_adjust(right=0.75)
                plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5))
                plt.show()
                xData = []
                yData = []
            if order == 2:
                initialGuess = [0.01, yData[0], yData[-1]]
                popt, pcov = curve_fit(second_order, xData, yData, initialGuess,bounds=((0, 0, 0), (10, 255, 255)))
                residuals = yData - second_order(xData, *popt)
                ss_res = np.sum(residuals ** 2)
                ss_tot = np.sum((yData - np.mean(yData)) ** 2)
                r2 = 1 - (ss_res / ss_tot)
                # Plot experimental data points
                plt.plot(xData, yData, dot, label='Data')
                plt.plot([], [], ' ', label='2$^{nd}$ Order Fit:')
                # x values for the fitted function
                xFit = np.arange(0.0, xData[-1],0.1)
                # Plot the fitted function
                k, ai,af = str("{:.4E}".format(float(popt[0]))), str("{:.4f}".format(float(popt[1]))),str("{:.4f}".format(float(popt[2])))
                plt.plot(xFit, second_order(xFit, *popt), 'k', label='Parameters:\nk='+k+'\n[A]\u2080='+ai+'\n[A]f='+af)
                plt.plot([], [], ' ', label='R-Square:\n' + str("%.4f" % r2))
                plt.xlabel('Time (min)')
                plt.ylabel(legend_color+' Channel Intensity')
                plt.subplots_adjust(right=0.75)
                plt.legend(loc='upper left', bbox_to_anchor=(1, 0.5))
                plt.show()
                xData = []
                yData = []

        def open_report ():
            import subprocess
            global global_photos_folder
            text_file = os.path.join(global_photos_folder[-1] + "\\", 'report.txt')
            report_file = text_file
            try:
                subprocess.Popen(["notepad", report_file])
            except:
                pass

        tk.Frame.__init__(self, parent)

        button1 = ttk.Button(self, text="Home Page", command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10)

        group_0 = tk.LabelFrame(self, padx=15, pady=10, borderwidth=0)
        group_0.pack(padx=10, pady=5)

        group_1 = tk.LabelFrame(group_0, padx=15, pady=10,
                                text="Choose Folder")
        group_1.grid(row=0, column=0)
        button2 = ttk.Button(group_1, text="Browse", command=LoadFolder)
        button2.pack()

        group_2 = tk.LabelFrame(group_0, padx=15, pady=10,
                                text="Enter time interval between photos")
        group_2.grid(row=0, column=1)
        label2 = Label(group_2, text='Value(min)')
        label2.grid(row=0, column=0)
        interval_entry = tk.Entry(group_2, text=" ", width=10)
        interval_entry.grid(row=0, column=1)
        button4 = ttk.Button(group_2, text="Enter", command=Interval)
        button4.grid(row=0, column=2)

        group_3 = tk.LabelFrame(self, padx=15, pady=10,
                                text="Show graph")
        group_3.pack(padx=10, pady=5)

        button5 = ttk.Button(group_3, text='RGB', command=RGB_graph)
        button5.grid(row=0, column=0)
        button6 = ttk.Button(group_3, text='Channel R', command=Red_graph)
        button6.grid(row=0, column=1)
        button7 = ttk.Button(group_3, text='Channel G', command=Green_graph)
        button7.grid(row=0, column=2)
        button8 = ttk.Button(group_3, text='Channel B', command=Blue_graph)
        button8.grid(row=0, column=3)

        group_00 = tk.LabelFrame(self, padx=15, pady=10, borderwidth=0)
        group_00.pack(padx=10, pady=5)

        group_4 = tk.LabelFrame(group_00, padx=15, pady=10, text='Press to fit curve')
        group_4.grid(row=0, column=0)
        button9 = ttk.Button(group_4, text='Zero order', command=zero_button)
        button9.grid(row=0, column=0)
        button10 = ttk.Button(group_4, text='First order', command=first_button)
        button10.grid(row=0, column=1)
        button11 = ttk.Button(group_4, text='Second order', command=second_button)
        button11.grid(row=0, column=2)

        group_11 = tk.LabelFrame(group_00, padx=15, pady=10,
                                 text="Text Report")
        group_11.grid(row=0, column=1)
        button21 = ttk.Button(group_11, text="Open", command=open_report)
        button21.pack()



        canvas = FigureCanvasTkAgg(f_fold, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        label_end = tk.Label(self,bg='white', text="Time (min)", font = 12)
        label_end.pack()

class Help(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Help Section", font=LARGE_FONT)
        label.pack(pady=20, padx=10)

        def popup_general():
            popup_general = tk.Tk()
            popup_general.wm_title("General Help")

            label = ttk.Label(popup_general, text="Welcome!", font=LARGE_FONT)
            label.grid(row=0, column=0)

            text = tk.Text(popup_general, font='times', wrap=tk.WORD, relief=tk.SUNKEN, height=30, width=60)
            with open("text_general.txt", 'r') as f:
                text.insert(tk.INSERT, f.read())
            text.grid(row=1, column=0, sticky='ew')
            scrollbar = ttk.Scrollbar(popup_general, orient='vertical', command=text.yview)
            scrollbar.grid(row=1, column=1, sticky='ns')
            text['yscrollcommand'] = scrollbar.set

            B1 = ttk.Button(popup_general, text="Close", command=popup_general.destroy)
            B1.grid(row=2, column=0)
            popup_general.mainloop()
        def popup_auto():
            popup_auto = tk.Tk()
            popup_auto.wm_title("Automatized Process Help")
            label = ttk.Label(popup_auto, font=LARGE_FONT)
            label.grid(row=0, column=0)

            text = tk.Text(popup_auto, font='times', wrap=tk.WORD, relief=tk.SUNKEN, height=30, width=60)
            with open("text_auto.txt", 'r') as f:
                text.insert(tk.INSERT, f.read())
            text.grid(row=1, column=0, sticky='ew')
            scrollbar = ttk.Scrollbar(popup_auto, orient='vertical', command=text.yview)
            scrollbar.grid(row=1, column=1, sticky='ns')
            text['yscrollcommand'] = scrollbar.set

            B1 = ttk.Button(popup_auto, text="Close", command=popup_auto.destroy)
            B1.grid(row=2, column=0)
            popup_auto.mainloop()
        def popup_manual():
            popup_manual = tk.Tk()
            popup_manual.wm_title("Manual Process Help")
            label = ttk.Label(popup_manual, font=LARGE_FONT)
            label.grid(row=0, column=0)

            text = tk.Text(popup_manual, font='times', wrap=tk.WORD, relief=tk.SUNKEN, height=30, width=60)
            with open("text_manual.txt", 'r') as f:
                text.insert(tk.INSERT, f.read())
            text.grid(row=1, column=0, sticky='ew')
            scrollbar = ttk.Scrollbar(popup_manual, orient='vertical', command=text.yview)
            scrollbar.grid(row=1, column=1, sticky='ns')
            text['yscrollcommand'] = scrollbar.set

            B1 = ttk.Button(popup_manual, text="Close", command=popup_manual.destroy)
            B1.grid(row=2, column=0)
            popup_manual.mainloop()
        def popup_folderdata():
            popup_folderdata = tk.Tk()
            popup_folderdata.wm_title("Photo Set Process Help")
            label = ttk.Label(popup_folderdata, font=LARGE_FONT)
            label.grid(row=0, column=0,sticky='nsew')

            text = tk.Text(popup_folderdata, font='times', wrap=tk.WORD, relief=tk.SUNKEN, height=30, width=60)
            with open("text_folderdata.txt", 'r') as f:
                text.insert(tk.INSERT, f.read())
            text.grid(row=1, column=0, sticky='nsew')
            scrollbar = ttk.Scrollbar(popup_folderdata, orient='vertical', command=text.yview)
            scrollbar.grid(row=1, column=1, sticky='nsew')
            text['yscrollcommand'] = scrollbar.set

            B1 = ttk.Button(popup_folderdata, text="Close", command=popup_folderdata.destroy)
            B1.grid(row=2, column=0)
            popup_folderdata.mainloop()


        button1 = ttk.Button(self, width=30, text="General Help",
                             command=popup_general)
        button1.pack(pady=10, padx=10)

        button1 = ttk.Button(self, width=30, text="Automatized Process Help",
                             command= popup_auto)
        button1.pack(pady=10, padx=10)

        button4 = ttk.Button(self, width=30, text='Manual Process Help',
                             command= popup_manual)
        button4.pack(pady=10, padx=10)

        button2 = ttk.Button(self, width=30, text="Photo Set Process Help",
                             command= popup_folderdata)
        button2.pack(pady=10, padx=10)





        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10, padx=10)


        def go_to_github():
            webbrowser.open('https://github.com/LACFI')
        def go_to_lacfiwebpage():
            webbrowser.open('http://www.inct-catalise.com.br/lacfi/index_EN.html')
        def go_to_raphaellwebpage():
            webbrowser.open('http://www.raphmoreira.com')

        group_end = tk.LabelFrame(self, padx=15, pady=10,
                                text="Visit Us")
        group_end.pack(padx=10, pady=5, side=tk.BOTTOM)
        button5 = ttk.Button(group_end, text='GitHub', command=go_to_github)
        button5.grid(row=0, column=0)
        button6 = ttk.Button(group_end, text='Lacfi WebPage', command=go_to_lacfiwebpage)
        button6.grid(row=0, column=1)
        button7 = ttk.Button(group_end, text='Raphaell WebPage', command=go_to_raphaellwebpage)
        button7.grid(row=0, column=2)


app = SmartAPP()
ani_auto = animation.FuncAnimation(f_auto, animate_auto, interval=1000)
ani_manu = animation.FuncAnimation(f_manu, animate_manu, interval=1000)
ani_fold = animation.FuncAnimation(f_fold, animate_fold, interval=1000)
app.geometry("500x700")

app.mainloop()