import multiprocessing

import numpy as np

from dng import DNG


def test_decode():
    input_file = np.zeros(3000, dtype=np.intc)

    pool = multiprocessing.Pool()
    tasks = []

    for i in range(10):
        task = pool.apply_async(thread, (i, input_file))
        tasks.append(task)

    pool.close()
    pool.join()

    for task in tasks:
        print(task.get())


def thread(i, input_file):
    dng = DNG(input_file)
    return i, dng.image


if __name__ == '__main__':
    test_decode()
