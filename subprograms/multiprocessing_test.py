from multiprocessing import Pool
def worker(x):
    return x*x

if __name__ == '__main__':
    # запускаем 4 рабочих процесса
    with Pool() as pool:
        it = pool.imap_unordered(worker, [2,4,6,8,10,12])
        # использование встроенной функции next()
        for i in it:
            print(i)