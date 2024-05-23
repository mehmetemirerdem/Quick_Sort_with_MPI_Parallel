from mpi4py import MPI
import numpy as np
import time

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def parallel_quicksort(arr, comm):
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        # Diziyi yaklaşık olarak eşit parçalara böl
        chunks = np.array_split(arr, size)
    else:
        chunks = None

    # Parçaları tüm süreçlere dağıt (scatter)
    local_chunk = comm.scatter(chunks, root=0)

    # Her süreç kendi yerel parçasını sıralar
    local_sorted = quicksort(local_chunk)

    # Sıralanmış parçaları kök süreçte toplar (gather)
    gathered_sorted_chunks = comm.gather(local_sorted, root=0)

    if rank == 0:
        # Sıralanmış parçaları birleştir
        sorted_arr = []
        for chunk in gathered_sorted_chunks:
            sorted_arr.extend(chunk)
        return quicksort(sorted_arr)
    return None

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # Sıralanacak diziyi sadece kök süreçte başlat
    if rank == 0:
        arr = np.random.randint(0, 1000, size=10000)
        print("Sıralanmamış dizi:", arr)
    else:
        arr = None

    # Zaman ölçümü yap
    comm.barrier()  # Tüm süreçlerin zamanlayıcıyı başlatmadan önce senkronize olmasını sağlar
    start_time = time.time()

    # Paralel quicksort işlemini gerçekleştir
    sorted_arr = parallel_quicksort(arr, comm)

    comm.barrier()  # Tüm süreçlerin zamanlayıcıyı durdurmadan önce senkronize olmasını sağlar
    end_time = time.time()

    # Kök süreçte sıralanmış diziyi ve zaman maliyetini yazdır
    if rank == 0:
        print("Sıralanmış dizi:", sorted_arr)
        print(f"Zaman maliyeti: {end_time - start_time:.4f} saniye")

if __name__ == "__main__":
    main()
