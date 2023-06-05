import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
import time
from Bio import SeqIO
from mpi4py import MPI

def read_fasta(file_name):
    sequences = []
    for record in SeqIO.parse(file_name, "fna"):
        sequences.append(str(record.seq))
    return "".join(sequences)

def draw_dotplot(matriz, fig_name):
    plt.figure(figsize=(10,10))
    plt.imshow(matriz, cmap="Greys", aspect="auto")
    plt.xlabel("Secuencia 1")
    plt.ylabel("Secuencia 2")
    plt.savefig(fig_name)
    plt.show()

def dotplot_secuencia(sequence1, sequence2):
    dotplot = np.empty((len(sequence1), len(sequence2)))
    for i in range(len(sequence1)):
        for j in range(len(sequence2)):
            if sequence1[i] == sequence2[j]:
                if i == j:
                    dotplot[i,j] = 1
                else:
                    dotplot[i,j] = 0.7
            else:
                dotplot[i,j] = 0
    return dotplot

def worker_multiprocessing(args):
    i, sequence1, sequence2 = args
    dotplot = []
    for j in range(len(sequence2)):
        if sequence1[i] == sequence2[j]:
            if i == j:
                dotplot.append(1)
            else:
                dotplot.append(0.7)
        else:
            dotplot.append(0)
    return dotplot

def parallel_multiprocessing_dotplot(sequence1, sequence2, threads=mp.cpu_count()):
    with mp.Pool(processes=threads) as pool:
        dotplot = pool.map(worker_multiprocessing, [(i, sequence1, sequence2) for i in range(len(sequence1))])
    return dotplot

def dotplot_multiprocessing(sequence1, sequence2, threads=mp.cpu_count()):
    dotplot = np.array(parallel_multiprocessing_dotplot(sequence1, sequence2, threads))
    return dotplot

def save_results_to_file(results, file_name = "archivos/results.txt"):
    with open(file_name, "w") as file:
        for result in results:
            file.write(str(result) + "\n")

def acceleration(times):
    return [times[0]/i for i in times]

def efficiency(accelerations, num_threads):
    return [accelerations[i]/num_threads[i] for i in range(len(num_threads))]

def draw_graphic_multiprocessing(times, accelerations, efficiencies, num_threads):
    plt.figure(figsize=(10,10))
    plt.subplot(1,2,1)
    plt.plot(num_threads, times)
    plt.xlabel("Número de procesadores")
    plt.ylabel("Tiempo")
    plt.subplot(1,2,2)
    plt.plot(num_threads, accelerations)
    plt.plot(num_threads, efficiencies)
    plt.xlabel("Número de procesadores")
    plt.ylabel("Aceleración y Eficiencia")
    plt.legend(["Aceleración", "Eficiencia"])
    plt.savefig("archivos/graficasMultiprocessing.png")

def main():
    ## Definir los comandos
    usage = "usage: mpirun -np <threads> python3 G-SAIP.py -q file.fasta ... [options]"


    start_secuencial = time.time()
    results_print = []

    ## Tiempo de ejecución secuencial
    results_print.append(f"Tiempo de ejecución secuencial: {time.time() - start_secuencial}")

    ## Tiempos de ejecución multiprocessing
    num_threads = [1, 2, 4, 8]
    times_multiprocessing = []
    for num_thread in num_threads:
        start_time = time.time()
        dotplot_multiprocessing(sequence1, sequence2, num_thread)
        times_multiprocessing.append(time.time() - start_time)
        results_print.append(f"Tiempo de ejecución multiprocessing con {num_thread} hilos: {time.time() - start_time}")
    
    ## Graficar dotplot secuencial
    draw_dotplot(dotplot_secuencia(sequence1, sequence2), "archivos/secuencial.png")

    ## Graficar dotplot multiprocessing
    draw_dotplot(dotplot_multiprocessing(sequence1, sequence2), "archivos/multiprocessing.png")
    
    ## Aceleración
    accelerations = acceleration(times_multiprocessing)
    for i in range(len(accelerations)):
        results_print.append(f"Aceleración con {num_threads[i]} hilos: {accelerations[i]}")
    
    ## Eficiencia
    efficiencies = efficiency(accelerations, num_threads)
    for i in range(len(efficiencies)):
        results_print.append(f"Eficiencia con {num_threads[i]} hilos: {efficiencies[i]}")
    
    ## Guardar resultados en archivo
    save_results_to_file(results_print)

    ## Graficar tiempos, aceleraciones y eficiencias
    draw_graphic_multiprocessing(times_multiprocessing, accelerations, efficiencies, num_threads)

if __name__ == "__main__":
    main()



    




