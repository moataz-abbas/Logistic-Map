import tkinter as tk
import concurrent.futures
import time
from multiprocessing import freeze_support, cpu_count

import matplotlib.pyplot as plt
import numpy as np

# global paramenters

cores = cpu_count()

p = 0

u = 1.0  # upper border of the graph
d = 0.0  # lower border of the graph

m = 1000  # no. of iteration before we reach a stable terminal pattern of numbers to be sample for the graph
sample = 500  # terminal sample pattern
ab = np.zeros((cores, 2))


def assign():
    global a, b, steps, p, s, u, d
    a = float(num_a.get())
    b = float(num_b.get())
    steps = (b - a) / cores
    p = float(num_p.get())  # power of the degree of steps between a and b
    s = 10 ** (-p)  # the degree of steps between a and b
    u = float(num_u.get())
    d = float(num_d.get())


def divid_proc():
    global ab
    for i in range(cores):
        ab[i, 0] = a + (steps * i)
        ab[i, 1] = a + (steps * (i + 1))


def logmap(args,s,u,d):
    ai = args[0]  # lowest growth rate starting point
    bi = args[1]  # largest growth rate end point
    
    x = np.zeros(m)  # the array of the solutions for every growth rate (r)
    x[0] = 0.4  # starting point of the growth array, 
                    #   any number between 0 to 1, will ultimately reach the same convergence

    r_range_i = np.arange(ai, bi, s)  # x-axis of the graph

    gi = np.zeros((r_range_i.size, sample))  # y-axis matrix

    j = 0  # iterator

    for r in r_range_i:
        for i in range(0, m - 1):
            x[i + 1] = r * x[i] * (1 - x[i])

        for k in range((m - sample), m):  # the zoom function
            if x[k] <= d or x[k] >= u:
                x[k] = float('nan')

        gi[j, :] = x[range((m - sample), m)]
        j = j + 1
    return gi, r_range_i


def play():
    
    assign()
    divid_proc()
    l = 0
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=cores) as executor:

        futures = {executor.submit(logmap, ab[i],s,u,d) for i in range(cores)}

        for fut in concurrent.futures.as_completed(futures):
            if l == 0:
                [g, r_range] = fut.result()
            else:
                [gt, r_range_t] = fut.result()
                g = np.concatenate((g, gt), axis=0)
                r_range = np.concatenate((r_range, r_range_t), axis=0)

            l = l + 1
    
    preplot = time.perf_counter()
    plt.plot(r_range, g, ',')
    #plt.show(block=False)
    finish = time.perf_counter()
    # total time taken
    t1.set(round(preplot - start, 2))
    t2.set(round(finish - preplot, 2))
    t3.set(round(finish - start, 2))
    plt.savefig('images\\logmap1', dpi=4000)           
    


def guilm():
    master = tk.Tk()
    global num_a, num_b, num_p, num_u, num_d, t1, t2, t3
    
    master.title ("Welcome to mizoTek Logestic Map")
    master.geometry('300x250')
    
    lbl = tk.Label(master, text = "Please enter the", font=("Arial Bold", 12))
    lbl.grid(column = 0, row=0)
    
    lbl2 = tk.Label(master, text = "desired values:", font=("Arial Bold", 12))
    lbl2.grid(column = 1, row=0)

    num_a = tk.StringVar()
    num_b = tk.StringVar()
    num_p = tk.StringVar()
    num_u = tk.StringVar()
    num_d = tk.StringVar()
    t1 = tk.StringVar()
    t2 = tk.StringVar()
    t3 = tk.StringVar()

    

    tk.Label(master, text = "First num:").grid(row=1, column=0)
    tk.Label(master, text = "End num:").grid(row=2, column=0)
    tk.Label(master, text = "Degree:").grid(row=3, column=0)
    tk.Label(master, text = "Upper Limit:").grid(row=4, column=0)
    tk.Label(master, text = "Lower limit:").grid(row=5, column=0)
    
    num_a = tk.Entry(master)
    num_b = tk.Entry(master)
    num_p = tk.Entry(master)
    num_u = tk.Entry(master)
    num_d = tk.Entry(master)
    
    num_a.insert(10, 3.4)
    num_b.insert(10, 4.0)
    num_p.insert(10, 4)
    num_u.insert(10, 1.0)
    num_d.insert(10, 0.0)
    
    num_a.grid(row=1,column=1)
    num_b.grid(row=2,column=1)
    num_p.grid(row=3,column=1)
    num_u.grid(row=4,column=1)
    num_d.grid(row=5,column=1)
    
    run_button = tk.Button(master, text = "RUN", command = play)
    run_button.grid(row=6,column=1)
    
    tk.Label(master, text = "Logestic map: (s)").grid(row=7, column=0)
    tk.Entry(master, textvariable = t1).grid(row=7,column=1)

    tk.Label(master, text = "Plotting: (s)").grid(row=8, column=0)
    tk.Entry(master, textvariable = t2).grid(row=8,column=1)
    
    tk.Label(master, text = "Total time: (s)").grid(row=9, column=0)
    tk.Entry(master, textvariable = t3).grid(row=9,column=1)
    
    master.mainloop()


if __name__ == '__main__':
    
    freeze_support()
    guilm()
    

