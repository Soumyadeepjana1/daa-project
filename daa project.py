import tkinter as tk
from tkinter import ttk
import random

# ---------- Globals ----------
data = []
comparisons = swaps = 0
delay = 150  # slower animation for clarity (ms)

# ---------- UI Drawing ----------
def draw(arr, highlight=[]):
    canvas.delete("all")
    w = 700 / len(arr)
    for i, h in enumerate(arr):
        color = "#00a2ff" if i not in highlight else "#ffcc00"
        canvas.create_rectangle(i*w, 350-h, (i+1)*w, 350, fill=color, outline="#333")
    root.update_idletasks()

def update_status(text):
    status_var.set(text)
    root.update_idletasks()

# ---------- Sorting Algorithms ----------
def bubble_sort():
    global comparisons, swaps
    n = len(data)
    for i in range(n-1):
        for j in range(n-i-1):
            comparisons += 1
            draw(data, [j, j+1])
            update_status(f"Comparing {data[j]} & {data[j+1]} | Swaps: {swaps} | Comparisons: {comparisons}")
            root.after(delay)
            if data[j] > data[j+1]:
                swaps += 1
                data[j], data[j+1] = data[j+1], data[j]
                draw(data, [j, j+1])
                root.after(delay)

def selection_sort():
    global comparisons, swaps
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            comparisons += 1
            draw(data, [min_idx, j])
            update_status(f"Comparing {data[min_idx]} & {data[j]} | Swaps: {swaps} | Comparisons: {comparisons}")
            root.after(delay)
            if data[j] < data[min_idx]:
                min_idx = j
        if min_idx != i:
            swaps += 1
            data[i], data[min_idx] = data[min_idx], data[i]
            draw(data, [i, min_idx])
            root.after(delay)

def insertion_sort():
    global comparisons, swaps
    for i in range(1, len(data)):
        key = data[i]; j = i-1
        while j >= 0 and data[j] > key:
            comparisons += 1
            data[j+1] = data[j]
            swaps += 1
            draw(data, [j, j+1])
            update_status(f"Comparing {data[j]} & {key} | Swaps: {swaps} | Comparisons: {comparisons}")
            root.after(delay)
            j -= 1
        data[j+1] = key

def merge_sort(arr, l=0, r=None):
    global comparisons, swaps
    if r is None: r = len(arr)-1
    if l < r:
        m = (l+r)//2
        merge_sort(arr, l, m)
        merge_sort(arr, m+1, r)
        merge(arr, l, m, r)

def merge(arr, l, m, r):
    global comparisons, swaps
    L, R = arr[l:m+1], arr[m+1:r+1]
    i = j = 0; k = l
    while i < len(L) and j < len(R):
        comparisons += 1
        if L[i] <= R[j]:
            arr[k] = L[i]; i += 1
        else:
            arr[k] = R[j]; j += 1
            swaps += 1
        draw(data, [k]); update_status(f"Merging | Swaps: {swaps} | Comparisons: {comparisons}")
        root.after(delay); k += 1
    while i < len(L): arr[k]=L[i]; i+=1; k+=1; draw(data, [k-1]); root.after(delay)
    while j < len(R): arr[k]=R[j]; j+=1; k+=1; draw(data, [k-1]); root.after(delay)

def quick_sort(arr, low=0, high=None):
    if high is None: high = len(arr)-1
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi-1)
        quick_sort(arr, pi+1, high)

def partition(arr, low, high):
    global comparisons, swaps
    pivot = arr[high]
    i = low-1
    for j in range(low, high):
        comparisons += 1
        if arr[j] < pivot:
            i += 1; arr[i], arr[j] = arr[j], arr[i]; swaps += 1
        draw(data, [i,j,high]); update_status(f"QuickSort | Swaps: {swaps} | Comparisons: {comparisons}")
        root.after(delay)
    arr[i+1], arr[high] = arr[high], arr[i+1]; swaps += 1
    draw(data, [i+1, high]); root.after(delay)
    return i+1

def heap_sort():
    global comparisons, swaps
    n = len(data)
    def heapify(n,i):
        largest=i; l=2*i+1; r=2*i+2
        if l<n: comparisons+=1; draw(data, [i,l]); root.after(delay); 
        if l<n and data[l]>data[largest]: largest=l
        if r<n: comparisons+=1; draw(data, [i,r]); root.after(delay)
        if r<n and data[r]>data[largest]: largest=r
        if largest!=i:
            data[i],data[largest]=data[largest],data[i]; swaps+=1
            draw(data,[i,largest]); root.after(delay)
            heapify(n,largest)
    for i in range(n//2-1,-1,-1): heapify(n,i)
    for i in range(n-1,0,-1): data[0],data[i]=data[i],data[0]; swaps+=1; draw(data,[0,i]); root.after(delay); heapify(i,0)

# ---------- Run Sorting ----------
def start_sort():
    global comparisons, swaps
    comparisons = swaps = 0
    algo = algo_menu.get()
    update_status(f"Running {algo} ...")
    root.update()
    if algo=="Bubble Sort": bubble_sort()
    elif algo=="Selection Sort": selection_sort()
    elif algo=="Insertion Sort": insertion_sort()
    elif algo=="Merge Sort": merge_sort(data)
    elif algo=="Quick Sort": quick_sort(data)
    elif algo=="Heap Sort": heap_sort()
    draw(data)
    update_status(f"Completed Swaps: {swaps} | Comparisons: {comparisons}")

# ---------- Generate Data ----------
def generate():
    global data
    size = int(size_box.get())
    data = [random.randint(20, 300) for _ in range(size)]
    draw(data)
    update_status("Array generated ")

# ---------- UI Setup ----------
root = tk.Tk()
root.title("Sorting Visualizer - Advanced")
root.config(bg="#111")

algo_menu = ttk.Combobox(root, values=["Bubble Sort","Selection Sort","Insertion Sort","Merge Sort","Quick Sort","Heap Sort"], state="readonly", width=20)
algo_menu.current(0); algo_menu.pack(pady=5)

size_box = tk.Spinbox(root, from_=5, to=50, width=5)
size_box.pack(pady=5); size_box.delete(0, tk.END); size_box.insert(0,"25")

tk.Button(root,text="Generate",command=generate,bg="#00ff88",fg="black").pack(pady=4)
tk.Button(root,text="Start Sorting",command=start_sort,bg="#ffaa00",fg="black").pack(pady=2)

canvas = tk.Canvas(root,width=700,height=350,bg="#222")
canvas.pack(pady=10)

status_var = tk.StringVar()
status_bar = tk.Label(root,textvariable=status_var,bg="#111",fg="white",anchor="w")
status_bar.pack(fill=tk.X)

generate()
root.mainloop()
