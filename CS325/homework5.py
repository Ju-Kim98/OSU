#CS325 HW5
#JuHyun Kim

import sys

def file_contents_letters(file_name):
    """
    Takes a file name as input and returns a string consisting of the file's contents
    with all non-letter characters removed.
    
    Parameters:
        file_name: The name of the file.
    
    Returns:
        A string with the contents of <file_name> but with all non-letter characters removed.
    """

    f = open(file_name, "r")
    file_contents = f.read()
    f.close()
    return "".join([c for c in file_contents if c.isalpha()])
    
def edit_distance(s1, s2, ci = 1, cd = 1, cm = 1):
    """
    Computes the edit distance between two strings, s1 and s2.
    
    Parameters:
        s1: The first string.
        s2: The second string.
        ci: The cost of an insertion (1 by default).
        cd: The cost of a deletion (1 by default).
        cm: The cost of a mutation (1 by default).
    
    Returns:
        The edit distance between s1 and s2.
    """
    # ed :  edit distance matrix
    ed = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)] 

    for i in range(len(s1) + 1):
        ed[i][0] = i * cd
    for j in range(len(s2) + 1):
        ed[0][j] = j * ci

    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            insertion = ed[i][j - 1] + ci
            deletion = ed[i - 1][j] + cd
            mutation = ed[i - 1][j - 1] + (cm if s1[i - 1] != s2[j - 1] else 0)

            ed[i][j] = min(insertion, deletion, mutation  )

    return ed[-1][-1]
    
def lcs(s1, s2):
    """
    Computes the length of the longest common subsequence between two strings, s1 and s2.
    
    Parameters:
        s1: The first string.
        s2: The second string.
    
    Returns:
        The length of the longest common subsequence between s1 and s2.
    """

    Lcs = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    
    # using dynamic programming
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                Lcs[i][j] = Lcs[i - 1][j - 1] + 1
            else:
                Lcs[i][j] = max(Lcs[i - 1][j], m[i][j - 1])
    
    return Lcs[-1][-1]
    
def lcs3(s1, s2, s3):
    """
    Computes the length of the longest common subsequence between three strings: s1, s2, and s3.
    
    Parameters:
        s1: The first string.
        s2: The second string.
        s3: The third string.
    
    Returns:
        The length of the longest common subsequence between s1, s2, and s3.
    """

    l1 = len(s1)
    l2 = len(s2)
    l3 = len(s3)
    
    Lcs3 = [[[0 for k in range(l3+1)] for j in range(l2+1)] for i in range(l1+1)]
    
    # using the recurrence relation
    for i in range(1, l1+1):
        for j in range(1, l2+1):
            for k in range(1, l3+1):
                if s1[i-1] == s2[j-1] == s3[k-1]:
                    Lcs3[i][j][k] = Lcs3[i-1][j-1][k-1] + 1
                else:
                    Lcs3[i][j][k] = max(Lcs3[i-1][j][k], Lcs3[i][j-1][k], Lcs3[i][j][k-1])
    
    return Lcs3[l1][l2][l3]

s1 = file_contents_letters(sys.argv[1])
s2 = file_contents_letters(sys.argv[2])
print(edit_distance(s1, s2), lcs(s1, s2))  # Outcome : (208, 29703) 

# python my_homework.py COVID-RefDec19.txt COVID-OmicronBA1.txt