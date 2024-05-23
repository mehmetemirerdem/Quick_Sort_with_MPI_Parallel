import random
import time

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quicksort(left) + middle + quicksort(right)

# Rastgele 10.000 elemanlı veri kümesi oluşturma
data = [random.randint(0, 1000) for _ in range(10000)]

# Sıralama işlemi öncesi zaman
start_time = time.time()

# QuickSort ile sıralama
sorted_data = quicksort(data)

# Sıralama işlemi sonrası zaman
end_time = time.time()

# Geçen süreyi hesapla
elapsed_time = end_time - start_time

print("İlk 10 eleman (sıralı):", sorted_data[::])
print("Son 10 eleman (sıralı):", sorted_data[::])
print(f"Sıralama işlemi {elapsed_time:.6f} saniye sürdü.")
