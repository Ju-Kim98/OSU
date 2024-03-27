#CS325 HW2
#JuHyun Kim

import sys
import time

# Usage when run from the command line: python max_subarray_homework2.py <filename>.
# Example usage:                        python max_subarray_homework2.py num_array_500.txt

file_name = sys.argv[1]

f = open(file_name, "r")
A = [int(num) for num in f.readline().strip().split(" ")]
f.close()


def max_subarray_simplification_delegation(A, left=None, right=None):
    if not A:
        return 0
    
    if left is None and right is None:
        left, right = 0, len(A)-1
    
    if right==left:
        return A[left]
     
    mid = (left + right) //2
  
    leftMax = float("-inf")
    temp_sum = 0
    for i in range(mid, left-1,-1):
        temp_sum =+ A[i]
        if temp_sum > leftMax:
            leftMax = temp_sum
           
    rightMax = float("-inf")
    temp_sum = 0    
    for i in range(mid+1, right+1):
        temp_sum += A[i]
        if temp_sum >rightMax:
            rightMax = temp_sum
   
    maxLeftRight = max(max_subarray_simplification_delegation(A, left, mid), 
                       max_subarray_simplification_delegation(A, mid+1, right))
    
    return max(maxLeftRight, leftMax, rightMax)
  
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

for alg in [max_subarray_simplification_delegation]:
    print(file_name, time_alg(alg, A))