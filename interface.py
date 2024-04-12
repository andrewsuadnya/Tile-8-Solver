# Import library tkinter (Tkinter) untuk membuat GUI
import tkinter as tk
import tkinter.ttk as ttk  # Modul tambahan untuk elemen GUI yang lebih canggih
from tkinter import messagebox, simpledialog  # Modul untuk menampilkan pesan dan dialog sederhana

# Import modul main yang mungkin berisi logika untuk menyelesaikan puzzle
import main

# Inisialisasi variabel global yang akan digunakan di seluruh program
algorithm = None
initialState = None
statepointer = cost = counter = depth = 0
runtime = 0.0
path = []

# Definisi kelas InterfaceApp yang akan mengatur tampilan GUI
class InterfaceApp:

    # =============================================================================================================== #
    ###     Build the GUI     ###

    # Inisialisasi objek InterfaceApp
    def __init__(self, master=None):

        # Inisialisasi variabel yang diperlukan untuk update GUI secara asinkron
        self._job = None

        # Membuat frame utama dari GUI dengan dimensi 800x550
        self.appFrame = ttk.Frame(master)
        self.appFrame.configure(height=550, width=800)
        self.appFrame.pack(side="top")

        # Label utama untuk judul aplikasi
        self.mainlabel = ttk.Label(self.appFrame)
        self.mainlabel.configure(
            anchor="center", font="{Forte} 55 {bold}", foreground="#000000", justify="center", text='Tile-8-Solver')
        self.mainlabel.place(anchor="center", x=300, y=50)

        # Tombol navigasi mundur (back)
        self.backbutton = ttk.Button(self.appFrame)
        self.img_backicon = tk.PhotoImage(file="icon/back-icon.png")
        self.backbutton.configure(cursor="hand2", image=self.img_backicon)
        self.backbutton.place(anchor="center", height=80, width=80, x=250, y=500)
        self.backbutton.bind("<ButtonPress>", self.prevSequence)

        # Tombol navigasi maju (next)
        self.nextbutton = ttk.Button(self.appFrame)
        self.img_nexticon = tk.PhotoImage(file="icon/next-icon.png")
        self.nextbutton.configure(cursor="hand2", image=self.img_nexticon)
        self.nextbutton.place(anchor="center", height=80, width=80, x=350, y=500)
        self.nextbutton.bind("<ButtonPress>", self.nextSequence)

        # Tombol navigasi cepat maju (fast forward)
        self.fastforwardbutton = ttk.Button(self.appFrame)
        self.img_fastforwardicon = tk.PhotoImage(file="icon/fast-forward-icon.png")
        self.fastforwardbutton.configure(cursor="hand2", image=self.img_fastforwardicon)
        self.fastforwardbutton.place(anchor="center", height=80, width=80, x=450, y=500)
        self.fastforwardbutton.bind("<ButtonPress>", self.fastForward)

        # Tombol navigasi cepat mundur (fast backward)
        self.fastbackwardbutton = ttk.Button(self.appFrame)
        self.img_fastbackwardicon = tk.PhotoImage(file="icon/fast-backward-icon.png")
        self.fastbackwardbutton.configure(cursor="hand2", image=self.img_fastbackwardicon)
        self.fastbackwardbutton.place(anchor="center", height=80, width=80, x=150, y=500)
        self.fastbackwardbutton.bind("<ButtonPress>", self.fastBackward)

        # Tombol untuk menghentikan fast forward
        self.stopbutton = ttk.Button(self.appFrame)
        self.img_stopicon = tk.PhotoImage(file="icon/stop.png")
        self.stopbutton.configure(cursor="hand2", image=self.img_stopicon, state='disabled')
        self.stopbutton.place(anchor="center", height=80, width=80, x=550, y=500)
        self.stopbutton.bind("<ButtonPress>", self.stopFastForward)

        # Tombol untuk mereset hitungan langkah
        self.resetbutton = ttk.Button(self.appFrame)
        self.img_reseticon = tk.PhotoImage(file="icon/reset-icon.png")
        self.resetbutton.configure(cursor="hand2", image=self.img_reseticon, state='disabled')
        self.resetbutton.place(anchor="center", height=80, width=80, x=50, y=500)
        self.resetbutton.bind("<ButtonPress>", self.resetStepCounter)

        # Label untuk menampilkan hitungan langkah
        self.stepCount = ttk.Label(self.appFrame)
        self.stepCount.configure(anchor="center", background="#d6d6d6",
                                 font="{@Malgun Gothic Semilight} 12 {}", justify="center", text='0 / 0')
        self.stepCount.place(anchor="center", width=200, x=300, y=440)

        # Tombol untuk memulai pemecahan puzzle
        self.solvebutton = ttk.Button(self.appFrame)
        self.img_solveicon = tk.PhotoImage(file="icon/solve-icon.png")
        self.solvebutton.configure(cursor="hand2", text='Solve', image=self.img_solveicon, compound="top")
        self.solvebutton.place(anchor="s", height=150, width=150, x=700, y=200)
        self.solvebutton.bind("<ButtonPress>", self.solve)

        # Objek untuk menampilkan animasi loading (GIF)
        self.gif_loading = tk.Label(self.appFrame)

        # Dropdown menu untuk memilih algoritma pencarian
        self.algorithmbox = ttk.Combobox(self.appFrame)
        self.algorithmbox.configure(cursor="hand2", state="readonly",
                                    values=('BFS', 'DFS', 'A*'))
        self.algorithmbox.place(anchor="center", height=30, width=150, x=700, y=230)
        self.algorithmbox.bind("<<ComboboxSelected>>", self.selectAlgorithm)

        # Label untuk menunjukkan teks "Search Algorithm:"
        self.algolabel = ttk.Label(self.appFrame)
        self.algolabel.configure(anchor="center", text='Search Algorithm:')
        self.algolabel.place(anchor="center", x=570, y=230)

        # Kotak untuk menampilkan analisis atau informasi tambahan
        self.analysisbox = ttk.Label(self.appFrame)
        self.analysisbox.configure(anchor="center", text='', background="#d6d6d6", borderwidth=3, relief="sunken")
        self.analysisbox.place(anchor="center", width=150, height=210, x=700, y=400)

        # Kotak 3x3 untuk menampilkan angka-angka puzzle
        self.cell0 = ttk.Label(self.appFrame)
        self.cell0.configure(anchor="center", background="#FFFFFF", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text=' ')
        self.cell0.place(anchor="center", height=100, width=100, x=200, y=150)

        self.cell1 = ttk.Label(self.appFrame)
        self.cell1.configure(anchor="center", background="#FFFFFF", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='1')
        self.cell1.place(anchor="center", height=100, width=100, x=300, y=150)

        self.cell2 = ttk.Label(self.appFrame)
        self.cell2.configure(anchor="center", background="#FFFFFF", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='2')
        self.cell2.place(anchor="center", height=100, width=100, x=400, y=150)

        self.cell3 = ttk.Label(self.appFrame)
        self.cell3.configure(anchor="center", background="#FFFFFF", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='3')
        self.cell3.place(anchor="center", height=100, width=100, x=200, y=250)

        self.cell4 = ttk.Label(self.appFrame)
        self.cell4.configure(anchor="center", background="#FFFFFF", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='4')
        self.cell4.place(anchor="center", height=100, width=100, x=300, y=250)

        self.cell5 = ttk.Label(self.appFrame)
        self.cell5.configure(anchor="center", background="#FFFFFF", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='5')
        self.cell5.place(anchor="center", height=100, width=100, x=400, y=250)

        self.cell6 = ttk.Label(self.appFrame)
        self.cell6.configure(anchor="center", background="#FFFFFF", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='6')
        self.cell6.place(anchor="center", height=100, width=100, x=200, y=350)

        self.cell7 = ttk.Label(self.appFrame)
        self.cell7.configure(anchor="center", background="#FFFFFF", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='7')
        self.cell7.place(anchor="center", height=100, width=100, x=300, y=350)

        self.cell8 = ttk.Label(self.appFrame)
        self.cell8.configure(anchor="center", background="#FFFFFF", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='8')
        self.cell8.place(anchor="center", height=100, width=100, x=400, y=350)

        # Tombol untuk memasukkan initial state puzzle
        self.enterstatebutton = ttk.Button(self.appFrame)
        self.img_inputicon = tk.PhotoImage(file="icon/input-icon.png")
        self.enterstatebutton.configure(
            cursor="hand2", text='Enter initial state', image=self.img_inputicon, compound="left")
        self.enterstatebutton.place(anchor="n", width=150, x=700, y=250)
        self.enterstatebutton.bind("<ButtonPress>", self.enterInitialState)

        # Mendefinisikan mainwindow sebagai appFrame
        self.mainwindow = self.appFrame

        # Membuat list objek GIF untuk animasi loading
        self.gif = [tk.PhotoImage(file='icon/loading.gif', format='gif -index %i' % i) for i in range(10)]

    # Fungsi untuk menjalankan program dan menampilkan GUI
    def run(self):
        """
        Menjalankan program, menampilkan GUI
        """
        app.displayStateOnGrid('000000000')
        app.gif_loading.place_forget()
        self.refreshFrame()
        self.mainwindow.after(0, app.refreshGIF, 0)
        self.mainwindow.mainloop()


    # =============================================================================================================== #
    ###     Widget Methods     ###

    @staticmethod
    def refreshGIF(ind):
        # Fungsi untuk memperbarui loading gif agar menampilkan frame berikutnya
        frame = app.gif[ind]
        ind = (ind + 1) % 10
        app.gif_loading.configure(image=frame)
        app.appFrame.after(50, app.refreshGIF, ind)

    def prevSequence(self, event=None):
        # Menampilkan keadaan sebelumnya pada grid
        global statepointer
        if statepointer > 0:
            self.stopFastForward()
            statepointer -= 1
            self.refreshFrame()

    def nextSequence(self, event=None):
        # Menampilkan keadaan berikutnya pada grid
        global statepointer
        if statepointer < len(path) - 1:
            self.stopFastForward()
            statepointer += 1
            self.refreshFrame()

    def solve(self, event=None):
        # Menyelesaikan puzzle dengan initialState dan algoritma tertentu, memberikan respons kepada pengguna
        global algorithm, initialState
        app.gif_loading.place(x=600, y=125, anchor="s")
        if self.readyToSolve():
            msg = 'Algorithm: ' + str(algorithm) + '\nInitial State = ' + str(initialState)
            messagebox.showinfo('Confirm', msg)
            self.resetGrid()
            self.solveState()
            if len(path) == 0:
                messagebox.showinfo('Unsolvable!', 'The state you entered is unsolvable')
                self.displaySearchAnalysis(True)
            else:
                self.refreshFrame()
        else:
            solvingerror = 'Cannot solve.\n' \
                           'Algorithm in use: ' + str(algorithm) + '\n' \
                                                                   'Initial State   : ' + str(initialState)
            messagebox.showerror('Cannot Solve', solvingerror)
        app.gif_loading.place_forget()

    def enterInitialState(self, event=None):
        # Meminta pengguna memasukkan initial state, memvalidasi, dan menampilkan pesan kesalahan jika tidak valid
        global initialState, statepointer
        inputState = simpledialog.askstring('Initial State Entry', 'Please enter your initial state')
        if inputState is not None:
            if self.validateState(inputState):
                initialState = inputState
                self.reset()
                app.displayStateOnGrid(initialState)
            else:
                messagebox.showerror('Input Error', 'Invalid initial state')

    def selectAlgorithm(self, event=None):
        # Mengaitkan algoritma yang dipilih ke variabel global 'algorithm'
        global algorithm
        try:
            choice = self.algorithmbox.selection_get()
            self.reset()
            algorithm = choice
        except:
            pass

    def fastForward(self, event=None):
        # Menampilkan keadaan berikutnya secara cepat hingga mencapai goal state atau dihentikan
        global statepointer
        self.stopFastForward()
        if statepointer < cost:
            app.stopbutton.configure(state='enabled')
            statepointer += 1
            self.refreshFrame()
            ms = 100
            if 100 < cost <= 1000:
                ms = 20
            if cost > 1000:
                ms = 1
            app._job = app.stepCount.after(ms, self.fastForward)
        else:
            self.stopFastForward()

    def fastBackward(self, event=None):
        # Menampilkan keadaan sebelumnya secara cepat hingga mencapai goal state atau dihentikan
        global statepointer
        self.stopFastForward()
        if statepointer > 0:
            app.stopbutton.configure(state='enabled')
            statepointer -= 1
            ms = 50
            if cost > 1000:
                ms = 1
            app._job = app.stepCount.after(ms, self.fastBackward)
        else:
            self.stopFastForward()
        self.refreshFrame()

    @staticmethod
    def stopFastForward(event=None):
        # Menghentikan fast-forward/backward
        if app._job is not None:
            app.stopbutton.configure(state='disabled')
            app.stepCount.after_cancel(app._job)
            app._job = None

    def resetStepCounter(self, event=None):
        # Mereset grid ke initial state dan step counter ke 0
        global statepointer
        if statepointer > 0:
            self.stopFastForward()
            statepointer = 0
            self.refreshFrame()



    # =============================================================================================================== #
    ###     Helper Functions     ###

    def displaySearchAnalysis(self, force_display=False):
        # Menampilkan analisis dari algoritma pencarian setelah dijalankan.
        if self.solved() or force_display is True:
            # Membuat teks analisis berdasarkan variabel global seperti algoritma, initialState, nodes expanded, dsb.
            analytics = 'Analysis of ' + str(algorithm) + \
                        '\ninitial state = ' + str(initialState)
            if force_display:
                analytics += '\n< UNSOLVABLE >'
            analytics += '\n-------------------------------' \
                         '\n' + 'Nodes expanded: \n' + str(counter) + \
                         '\n' + 'Search depth: \n' + str(depth) + \
                         '\n' + 'Search cost: \n' + str(cost) + \
                         '\n' + 'Running Time: \n' + str(runtime) + ' s'
        else:
            analytics = ''
        app.analysisbox.configure(text=analytics)

    def displayStateOnGrid(self, state):
        # Menampilkan keadaan input pada grid
        if not self.validateState(state):
            state = '000000000'
        # Mengatur teks pada masing-masing sel grid sesuai dengan digit dari state.
        self.cell0.configure(text=self.adjustDigit(state[0]))
        self.cell1.configure(text=self.adjustDigit(state[1]))
        self.cell2.configure(text=self.adjustDigit(state[2]))
        self.cell3.configure(text=self.adjustDigit(state[3]))
        self.cell4.configure(text=self.adjustDigit(state[4]))
        self.cell5.configure(text=self.adjustDigit(state[5]))
        self.cell6.configure(text=self.adjustDigit(state[6]))
        self.cell7.configure(text=self.adjustDigit(state[7]))
        self.cell8.configure(text=self.adjustDigit(state[8]))

    @staticmethod
    def readyToSolve():
        # Memeriksa apakah keadaan saat ini siap untuk dipecahkan dengan memeriksa apakah variabel global 'initialState' dan
        # 'algorithm' tidak None
        return initialState is not None and algorithm is not None

    @staticmethod
    def solved():
        # Memeriksa apakah ada solusi yang terdaftar dalam variabel global
        return len(path) > 0

    @staticmethod
    def solveState():
        # Menyelesaikan teka-teki dengan 'initialState' dan 'algorithm' yang dipilih. Mengasumsikan keadaan saat ini siap untuk dipecahkan.
        global path, cost, counter, depth, runtime
        if str(algorithm) == 'BFS':
            main.BFS(initialState)
            path, cost, counter, depth, runtime = \
                main.bfs_path, main.bfs_cost, main.bfs_counter, main.bfs_depth, main.time_bfs
        elif str(algorithm) == 'DFS':
            main.DFS(initialState)
            path, cost, counter, depth, runtime = \
                main.dfs_path, main.dfs_cost, main.dfs_counter, main.dfs_depth, main.time_dfs
        elif str(algorithm) == 'A*':
            main.AStarSearch_manhattan(initialState)
            path, cost, counter, depth, runtime = \
                main.manhattan_path, main.manhattan_cost, main.manhattan_counter, main.manhattan_depth, main.time_manhattan


    def resetGrid(self):
        # Mereset grid dan step counter ke keadaan awal
        global statepointer
        statepointer = 0
        self.refreshFrame()
        app.stepCount.configure(text=self.getStepCountString())

    def reset(self):
        # Mereset variabel global dan frame GUI. Menghapus solusi yang terdaftar saat ini
        global path, cost, counter, runtime
        cost = counter = 0
        runtime = 0.0
        path = []
        self.resetGrid()
        app.analysisbox.configure(text='')

    @staticmethod
    def getStepCountString():
        # Mengembalikan representasi string dari jumlah langkah yang akan ditampilkan pada step counter
        return str(statepointer) + ' / ' + str(cost)

    @staticmethod
    def refreshFrame():
        # Memperbarui frame dengan semua komponennya: grid, counter, tombol, dll.
        if cost > 0:
            state = main.getStringRepresentation(path[statepointer])
            app.displayStateOnGrid(state)
            app.stepCount.configure(text=app.getStepCountString())
            app.displaySearchAnalysis()
        if statepointer == 0:
            app.resetbutton.configure(state='disabled')
            app.backbutton.configure(state='disabled')
            app.fastbackwardbutton.configure(state='disabled')
        else:
            app.resetbutton.configure(state='enabled')
            app.backbutton.configure(state='enabled')
            app.fastbackwardbutton.configure(state='enabled')

        if cost == 0 or statepointer == cost:
            app.fastforwardbutton.configure(state='disabled')
            app.nextbutton.configure(state='disabled')
        else:
            app.fastforwardbutton.configure(state='enabled')
            app.nextbutton.configure(state='enabled')

    @staticmethod
    def validateState(inputState):
        # Memvalidasi state yang diberikan
        seen = []
        if inputState is None or len(inputState) != 9 or not inputState.isnumeric():
            return False
        for dig in inputState:
            if dig in seen or dig == '9':
                return False
            seen.append(dig)
        return True

    @staticmethod
    def adjustDigit(dig):
        # Mengonversi nol menjadi sel kosong. Selain itu, mengembalikan digit sebagaimana adanya.
        if dig == '0':
            return ' '
        return dig


if __name__ == "__main__":
    global app
    root = tk.Tk()
    root.title('Tile-8-Solver')
    app = InterfaceApp(root)
    app.run()
