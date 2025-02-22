

def control_swap(control, a, b):
    """Меняет a и b местами, если control равен 1."""
    return (b, a) if control == 1 else (a, b)


def sort_binary_sequence(arr):
    """Сортирует бинарный массив с использованием CONTROL-SWAP."""
    n = len(arr)
    swapped = True
    while swapped:
        swapped = False
        for i in range(n - 1):
            # Применяем CONTROL-SWAP к текущему и следующему элементу
            # control = arr[i], целевые биты = arr[i], arr[i+1]
            new_a, new_b = control_swap(arr[i], arr[i], arr[i+1])
            if new_a != arr[i] or new_b != arr[i+1]:
                arr[i], arr[i+1] = new_a, new_b
                swapped = True
    return arr


# Примеры использования
test_cases = [
    [1, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [1, 1, 0, 0, 1],
    [0, 0, 0],
    [1, 1, 1]
]

for sequence in test_cases:
    sorted_seq = sort_binary_sequence(sequence.copy())
    print(f"Исходная: {sequence}, Отсортированная: {sorted_seq}")
