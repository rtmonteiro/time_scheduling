from typing import Any
from scheduling.models.matrix import Matrix

from typing import TypeVar

T = TypeVar("T")


def is_all_zeros(lst: list[Any]):
    """Returns True if all elements of the list are 0"""
    return all(element == -1 for element in lst)

def insert_into_slice(lst: list[T], start: int, size: int, value: T):
    """Inserts the value into the slice of the list"""

    for i in range(start, start + size):
        lst[i] = value

def is_element_absent(matrix: Matrix, element: int):
    """Returns True if the element is not present in the matrix"""
    return not any(element in row for row in matrix)

def find_subarray(main_array: list[T], sub_array: list[T]):
    """Returns the index of the subarray in the main array"""

    sub_len = len(sub_array)
    for i in range(len(main_array)):
        if main_array[i:i+sub_len] == sub_array:
            return i
    return -1

def search_subarray_in_matrix(matrix: Matrix, sub_array: list[int]):
    """Returns the index of the subarray in the matrix"""
    for row_index, row in enumerate(matrix):
        index = find_subarray(row, sub_array)
        if index != -1:
            return row_index, index
    return -1, -1
