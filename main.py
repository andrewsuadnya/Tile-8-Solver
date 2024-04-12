# Import library yang diperlukan
import heapq  #Digunakan untuk mengelola struktur data heap queue (antrian prioritas) pada algoritma A*.
import math   #Menyediakan fungsi matematika, digunakan di sini untuk menghitung logaritma basis 10 guna menentukan panjang angka dalam representasi string.
import time   #Memberikan fungsi-fungsi terkait waktu. Digunakan untuk mengukur waktu eksekusi algoritma dan memantau kinerja program.

# Digunakan untuk menentukan perubahan posisi di papan puzzle
dx = [-1, 1, 0, 0]
dy = [0, 0, 1, -1]

# Variabel global yang menyimpan jumlah langkah dan informasi jalur untuk setiap algoritma
dfs_counter = 0
bfs_counter = 0
manhattan_counter = 0

dfs_path = []
bfs_path = []
manhattan_path = []

dfs_cost = 0
bfs_cost = 0
manhattan_cost = 0

dfs_depth = 0
bfs_depth = 0
manhattan_depth = 0

time_dfs = 0
time_bfs = 0
time_manhattan = 0


# Fungsi untuk mendapatkan representasi string dari angka
def getStringRepresentation(x):
    if int(math.log10(x)) + 1 == 9:
        return str(x)
    else:
        return "0" + str(x)


# Fungsi untuk menghasilkan semua kemungkinan langkah yang valid dari suatu keadaan
def getChildren(state):
    children = []
    idx = state.index('0')  # Temukan posisi nol pada puzzle
    i = int(idx / 3)
    j = int(idx % 3)
    for x in range(0, 4):
        nx = i + dx[x]
        ny = j + dy[x]
        nwIdx = int(nx * 3 + ny)
        if checkValid(nx, ny):
            listTemp = list(state)
            listTemp[idx], listTemp[nwIdx] = listTemp[nwIdx], listTemp[idx]
            children.append(''.join(listTemp))
    return children


# Fungsi untuk mendapatkan jalur yang ditempuh menuju keadaan tujuan
def getPath(parentMap, inputState):
    path = []
    temp = 12345678
    while temp != inputState:
        path.append(temp)
        temp = parentMap[temp]
    path.append(inputState)
    path.reverse()
    return path


# Fungsi untuk mencetak jalur menuju keadaan tujuan
def printPath(path):
    for i in path:
        print(getStringRepresentation(i))


# Fungsi untuk memeriksa apakah keadaan tujuan telah tercapai
def goalTest(state):
    if state == 12345678:
        return True
    return False


# Fungsi untuk mengecek apakah puzzle dapat diselesaikan dari keadaan awal
def isSolvable(digit):
    count = 0
    for i in range(0, 9):
        for j in range(i, 9):
            if digit[i] > digit[j] and digit[i] != 9:
                count += 1
    return count % 2 == 0


# Algoritma Breadth-First Search (BFS)
def BFS(inputState):
    start_time = time.time()
    q = []  # Antrian untuk menyimpan keadaan yang akan dieksplorasi
    explored = {}  # Dictionary untuk menyimpan keadaan yang telah dieksplorasi
    parent = {}  # Dictionary untuk menyimpan keadaan induk dari setiap keadaan
    parent_cost = {}  # Dictionary untuk menyimpan jumlah langkah dari keadaan awal ke keadaan saat ini
    integer_state = int(inputState)
    q.append(integer_state)
    cnt = 0
    global bfs_counter
    global bfs_path
    global bfs_cost
    global bfs_depth
    global time_bfs
    bfs_depth = 0
    parent_cost[integer_state] = 0
    while q:
        cnt += 1
        state = q.pop(0)
        explored[state] = 1
        bfs_depth = max(bfs_depth, parent_cost[state])
        if goalTest(state):
            path = getPath(parent, int(inputState))
            bfs_counter = cnt
            bfs_path = path
            bfs_cost = len(path) - 1
            time_bfs = float(time.time() - start_time)
            return 1
        children = getChildren(getStringRepresentation(state))
        for child in children:
            child_int = int(child)
            if child_int not in explored:
                q.append(child_int)
                parent[child_int] = state
                explored[child_int] = 1
                parent_cost[child_int] = 1 + parent_cost[state]
    bfs_path = []
    bfs_cost = 0
    bfs_counter = cnt
    time_bfs = float(time.time() - start_time)
    return 0


# Algoritma Depth-First Search (DFS)
def DFS(inputState):
    start_time = time.time()
    stack = []  # Stack untuk menyimpan keadaan yang akan dieksplorasi
    explored = {}  # Dictionary untuk menyimpan keadaan yang telah dieksplorasi
    parent = {}  # Dictionary untuk menyimpan keadaan induk dari setiap keadaan
    parent_cost = {}  # Dictionary untuk menyimpan jumlah langkah dari keadaan awal ke keadaan saat ini
    integer_state = int(inputState)
    parent_cost[integer_state] = 0
    explored[integer_state] = 1
    stack.append(integer_state)
    cnt = 0
    global dfs_counter
    global dfs_path
    global dfs_cost
    global dfs_depth
    global time_dfs
    dfs_depth = 0
    while stack:
        cnt += 1
        state = stack[-1]
        stack.pop()
        dfs_depth = max(dfs_depth, parent_cost[state])
        if goalTest(state):
            path = getPath(parent, int(inputState))
            dfs_counter = cnt
            dfs_path = path
            dfs_cost = len(path) - 1
            time_dfs = float(time.time() - start_time)
            return 1
        children = getChildren(getStringRepresentation(state))
        for child in children:
            child_int = int(child)
            if child_int not in explored:
                stack.append(child_int)
                parent[child_int] = state
                explored[child_int] = 1
                parent_cost[child_int] = 1 + parent_cost[state]
    dfs_path = []
    dfs_cost = 0
    dfs_counter = cnt
    time_dfs = float(time.time() - start_time)
    return 0


# Fungsi untuk memeriksa apakah keadaan valid atau di luar batas
def checkValid(i, j):
    if i >= 3 or i < 0 or j >= 3 or j < 0:
        return 0
    return 1


# Fungsi heuristik menggunakan jarak Manhattan
def getManhattanDistance(state):
    tot = 0
    for i in range(1, 9):
        goalX = int(i / 3)
        goalY = i % 3
        idx = state.index(str(i))
        itemX = int(idx / 3)
        itemY = idx % 3
        tot += (abs(goalX - itemX) + abs(goalY - itemY))
    return tot


# Algoritma A* (A-Star) menggunakan jarak Manhattan sebagai heuristik
def AStarSearch_manhattan(inputState):
    start_time = time.time()
    integer_state = int(inputState)
    heap = []  # Heap untuk menyimpan keadaan yang akan dieksplorasi
    explored = {}  # Dictionary untuk menyimpan keadaan yang telah dieksplorasi
    parent = {}  # Dictionary untuk menyimpan keadaan induk dari setiap keadaan
    cost_map = {}  # Dictionary untuk menyimpan total biaya (heuristik + biaya sejauh ini)
    heapq.heappush(heap, (getManhattanDistance(inputState), integer_state))
    cost_map[integer_state] = getManhattanDistance(inputState)
    heap_map = {}
    heap_map[integer_state] = 1
    global manhattan_counter
    global manhattan_path
    global manhattan_cost
    global manhattan_depth
    global time_manhattan
    manhattan_depth = 0
    while heap:
        node = heapq.heappop(heap)
        state = node[1]
        string_state = getStringRepresentation(state)
        parent_cost = node[0] - getManhattanDistance(string_state)
        if not state in explored:
            manhattan_depth = max(parent_cost, manhattan_depth)
        explored[state] = 1
        if goalTest(state):
            path = getPath(parent, int(inputState))
            manhattan_path = path
            manhattan_counter = (len(explored))
            manhattan_cost = len(path) - 1
            time_manhattan = float(time.time() - start_time)
            return 1
        children = getChildren(string_state)
        for child in children:
            new_cost = getManhattanDistance(child)
            child_int = int(child)
            if child_int not in explored and child not in heap_map:
                heapq.heappush(heap, (parent_cost + new_cost + 1, child_int))
                heap_map[child_int] = 1
                cost_map[child_int] = parent_cost + new_cost + 1
                parent[child_int] = state
            elif child_int in heap_map:
                if (new_cost + parent_cost + 1) < cost_map[child_int]:
                    parent[child_int] = state
                    cost_map[child_int] = new_cost + parent_cost + 1
                    heapq.heappush(heap, (parent_cost + 1 + new_cost, child_int))
    manhattan_cost = 0
    manhattan_path = []
    manhattan_counter = (len(explored))
    time_manhattan = float(time.time() - start_time)
    return 0
