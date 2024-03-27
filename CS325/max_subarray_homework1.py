#CS325 HW1
#JuHyun Kim

import sys
import time

# Usage when run from the command line: python max_subarray_homework1.py <filename>.
# Example usage:                        python max_subarray_homework1.py num_array_500.txt

file_name = sys.argv[1]

f = open(file_name, "r")
A = [int(num) for num in f.readline().strip().split(" ")]
f.close()

def max_subarray_enumeration(A):

    max_sum_enum = float("-inf")
    n=len(A)
    for i in range(n-1):
        for j in range(i,n-1):
            temp_sum =0
            for k in range(i,j):
             temp_sum += A[k]
            if temp_sum > max_sum_enum:
                max_sum_enum = temp_sum
                
    return max_sum_enum
    
def max_subarray_iteration(A):
    
    max_sum_itr = float("-inf")
    n=len(A)
    for i in range(n-1):
        cur_sum = 0
        for j in range(i,n-1):
            cur_sum += A[j]
            if cur_sum > max_sum_itr:
                max_sum_itr = cur_sum

    return max_sum_itr

def time_alg(alg, A):
    """
    Runs an algorithm for the maximum subarray problem on a test array and times how long it takes.
    
    Parameters:
        alg: An algorithm for the maximum subarray problem.
        A: A list (array) of n >= 1 integers.
    
    Returns:
        A pair consisting of the value of alg(A) and the time needed to execute alg(A) in milliseconds.
    """

    start_time = time.monotonic_ns() // (10 ** 6) # The start time in milliseconds.
    max_subarray_val = alg(A)
    end_time   = time.monotonic_ns() // (10 ** 6) # The end time in milliseconds.
    return max_subarray_val, end_time - start_time

for alg in [max_subarray_enumeration, max_subarray_iteration]:
    print(file_name, time_alg(alg, A))
