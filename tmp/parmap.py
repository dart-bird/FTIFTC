import parmap
from multiprocessing import Manager



def a(x, d):
    d.append(x)


if __name__ == "__main__":
    num_cores = 4
    manager = Manager()
    d = manager.list()
    input_list = range(0, 10)
    parmap.map(a, input_list, d, pm_pbar=True, pm_processes=num_cores)
    print(d)