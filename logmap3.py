import tkinter as tk
import concurrent.futures
import time
from multiprocessing import freeze_support, cpu_count

import matplotlib.pyplot as plt
import numpy as np


def assign(num_a, num_b, num_p, num_u, num_d):
    a = float(num_a.get())
    b = float(num_b.get())
    steps = (b - a) / cores
    p = float(num_p.get())  # power of the degree of steps between a and b
    s = 10 ** (-p)  # the degree of steps between a and b
    u = float(num_u.get())
    d = float(num_d.get())
    return a, b, steps, p, s, u, d


def divid_proc(a, steps, cores, ab):
    for i in range(cores):
        ab[i, 0] = a + (steps * i)
        ab[i, 1] = a + (steps * (i + 1))
    return ab

def logmap(args,s,u,d):
    ai = args[0]  # lowest growth rate starting point
    bi = args[1]  # largest growth rate end point
    
    x = np.zeros(m)  # the array of the solutions for every growth rate (r)
    x[0] = 0.4  # starting point of the growth array, any number between 0 to 1, will ultimately reach the same convergence

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
    
    
def play(cores, m, sample, ab, num_a, num_b, num_p, num_u, num_d, t1, t2, t3):
    a, b, steps, p, s, u, d=assign(num_a, num_b, num_p, num_u, num_d)
    ab= divid_proc(a, steps, cores, ab)
    start = time.perf_counter()
    for i in range(cores):
        res= logmap(ab[i], s, u, d)
        if i == 0:
            [g, r_range] = res
        else:
            [gt, r_range_t] = res
            g = np.concatenate((g, gt), axis=0)
            r_range = np.concatenate((r_range, r_range_t), axis=0)
            
    preplot = time.perf_counter()
    plt.plot(r_range, g, ',')
    finish = time.perf_counter()
    # total time taken
    t1.set(round(preplot - start, 2))
    t2.set(round(finish - preplot, 2))
    t3.set(round(finish - start, 2))
    plt.savefig('images\\logmap.png', dpi=600)
    


def guilm(cores, m, sample, ab):
    master = tk.Tk()
    master.title ("Welcome to ABBASMD. Logestic Map")
    master.geometry('300x400')
    
    lbl = tk.Label(master, text = "Welcome to ABBASMD. Logestic Map\nPlease enter the desired values:", font=('Arial Bold', 10))
    lbl.grid(row=0, columnspan=2, ipady=10)
        
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
    
    run_button = tk.Button(master, text = "RUN", command = lambda : play(cores, m, sample, ab, num_a, num_b, num_p, num_u, num_d, t1, t2, t3))
    run_button.grid(row=6,column=1)
    
    tk.Label(master, text = "Logestic map: (s)").grid(row=7, column=0)
    tk.Entry(master, textvariable = t1).grid(row=7,column=1)

    tk.Label(master, text = "Plotting: (s)").grid(row=8, column=0)
    tk.Entry(master, textvariable = t2).grid(row=8,column=1)
    
    tk.Label(master, text = "Total time: (s)").grid(row=9, column=0)
    tk.Entry(master, textvariable = t3).grid(row=9,column=1)
    
    master.mainloop()
    
    
if __name__ == '__main__':
    cores = 4
    m = 1000  # no. of iteration before we reach a stable terminal pattern of numbers to be sample for the graph
    sample = 500  # terminal sample pattern
    ab = np.zeros((cores, 2))
    guilm(cores, m, sample, ab)
    
    