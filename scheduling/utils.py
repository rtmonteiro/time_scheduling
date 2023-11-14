def is_all_zeros(lst):
    return all(element == -1 for element in lst)

def insert_into_slice(lst, start, size, value):
    for i in range(start, start + size):
        lst[i] = value
