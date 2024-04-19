# Insertion Sort

"""
Our first algorithm, insertion sort, solves the sorting problem
"""


def insertion_sort(lst: list, n: int):
    """
    Input: A sequence of n numbers {a₁, a₂, ..., }
    Output: A permutation (reordering) {a′₁, a′₂, ..., a′ₙ} of the input sequence such that
            a′₁ ≤ a′₂ ≤ ... ≤ a′ₙ
    """

    """
    The numbers to be sorted are also known as 'keys'. Although the problem is conceptually about sorting a sequence, the 
    input comes in the form of an array with n elements. When we want to sort numbers it's often because they are the keys 
    associated with other data, which we call 'satellite data'. Together a key and satellite data form a record.
    """

    """      INSERTION SORT EXPLAINED    
    It is an efficient algorithm for sorting a small number of elements. Insertion sort works the way you might sort a 
    hand of playing cards. Start with an empty left hand and the cards in a pile, and insert it into the correct 
    position in by comparing it with each of the cards already in your left hand, starting at the right and moving left.
    As soon as you see a card in your left hand whose value is less than or equal to the card you're holding in your 
    right hand, insert the card that you're holding in your right hand just to the right of this card in your left hand.
    If all the cards in your left hand have values greater than the card in your right hand, then place this card as 
    the leftmost card in your left hand. At all times, the cards  held in your left hand are sorted, and these cards 
    were originally the top cards of the pile on the table.
    """

    for i in range(n):  # i represents the current card being inserted into the hand
        key = lst[i]
        # Insert lst[i] into the sorted subarray lst[1:key-1]
        j = i - 1
        while j >= 0 and lst[j] > key:  # Running through the subarray lst[:j]
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = key


lst = [5, 2, 4, 6, 1, 3]
insertion_sort(lst, len(lst))
print(lst)

def exercise2x1s4(seq, n):
    for i in enumerate(seq):
        if i[1] == n:
            return i[0]
    return None

print(exercise2x1s4(lst, 4))

# An exercise 2.1-5 looks like:
'''
ₙ₋₁               ₙ₋₁
Σ a[i] * 2^i  +  Σ b[i] * 2^i  
ᶦ⁼⁰               ᶦ⁼⁰
'''

def exercise2x1s5(a, b, n):
    c = [0]
    for i in range(1, n):
        c[0] += a[-i] * 2**(i-1)
        c[0] += b[-i] * 2**(i-1)
    return c

print(exercise2x1s5([1, 0, 1, 0, 1], [1, 0, 1, 1, 1], 6))

# ----------------------------------------------------------------------------------------------------------------------

# Analyzing algorithms

"""
Analyzing an algorithm has come to mean predicting the resources that the algorithm requires. You might consider 
resources such as memory, communication bandwidth, or energy consumption. Most often, however, you'll want to measure 
computational time. If you analyze several candidate algorithms for a problem, you can identify the most efficient one.

Before you can analyze an algorithm, you need a model of the technology that it runs on, including the resources of that
technology, with the understanding that algorithms are implemented as computer programs, 'random-access machine' (RAM) 
model of computation as the implementation technology, with the understanding that algorithms are implemented as 
computer programs. In the RAM model, instructions execute one after another, with no concurrent operations. The RAM model
assumes that each instruction takes the same amount of time as any other instruction and that each data access - using 
the value of a variable or sorting into a variable.

The data types in RAM model are integer, floating point (for storing real-number approximations), and character. Real 
computers do not usually have a separate data type for the boolean values TRUE and FALSE. Instead, they often test 
whether an integer value is 0 (FALSE) or nonzero (TRUE). We also assume that each word of data has a limit on the number
of bits. For example, when working with inputs of size n, we typically assume that integers are represented by c log₂n
bits for some constant c ≥ 1. We require c ≥ 1 so that each word cna hold the value of n, enabling us to index the 
individual input elements, amd we restrict c to be a constant so that the word size does not grow arbitrarily.
"""

"""
The 'running time' of an algorithm on a particular input is the number of instructions and data accesses executed.
Basically, it's the sum of running times for ach statement executed. A statement that takes cₖ steps to execute and 
executes m times contributes cₖm to the total running time. 
"""

# Let's analyze the insertion sort

'''
For each i = 2, 3, ..., n, let tᵢ denote the number of times the while loop test in line 5 is executed for the value of i.
When a for or while loop exists in the usual way-because the test in the loop header comes up FALSE - the test is 
executed one time more than the loop body
'''



"""
def insertion_sort(lst):                                               cost  times
    for i in range(n):                                                  c₁     n
        key = lst[i]                                                    c₂    n-1
        # Insert lst[i] into the sorted subarray lst[1:key-1]           0     n-1
        j = i - 1                                                       c₄    n-1
                                                                              ₙ
        while j >= 0 and lst[j] > key:                                  c₅    Σ tᵢ
                                                                              ᶦ⁼²
                                                                              ₙ
            lst[j + 1] = lst[j]                                         c₆    Σ tᵢ-1
                                                                              ᶦ⁼²
                                                                              ₙ
            j -= 1                                                      c₇    Σ tᵢ-1
                                                                              ᶦ⁼² 
        lst[j + 1] = key                                                c₈    n-1
                                   ₙ         ₙ          ₙ
T(n) = c₁n + c₂(n-1) + c₄(n-1) + c₅Σ tᵢ + c₆Σ tᵢ-1 + c₇Σ tᵢ-1 + c₈(n-1)
                                   ᶦ⁼²       ᶦ⁼²        ᶦ⁼²
                                   
We get rid of c₆ and c₇ because they rely on c₅ which is always false (in this case) because we are counting a best-case scenario

T(n) = c₁n + c₂(n-1) + c₄(n-1) + c₅(n-1) + c₈(n-1) = (c₁ + c₂ + c₄ + c₅ + c₈)n - (c₂ + c₄ + c₅ + c₈)
                                                                  ₙ
We can express (c₁ + c₂ + c₄ + c₅ + c₈)n - (c₂ + c₄ + c₅ + c₈) as Σ(an - b), 
the running time is thus a linear function of n                   ᵏ⁼¹

Now let's find the worst case scenario running time
                                   (n(n+1)   )      (n(n-1))      (n(n-1))
T(n) = c₁n + c₂(n-1) + c₄(n-1) + c₅(------ -1) + c₆ (------) + c₇ (------) + c₈(n-1) = 
                                   (   2     )      (   2  )      (   2  )
  (c₅   c₆   c₇)      (               c₅   c₆   c₇     )
= (-- + -- + --) n² + (c₁ + c₂ + c₄ + -- - -- - -- + c₈) n - (c₂ + c₄ + c₅ + c₈)
  (2    2    2 )      (               2    2    2      )

We can express this worst-case running time as (an² + bn + c),
the running time is thus a quadratic function of n
"""

# ----------------------------------------------------------------------------------------------------------------------

# Worst-case and average-case analysis

# Worst-case
"""
The worst-case gives an upper bound on the running time for any input. If you know it, then you have a guarantee that 
the algorithm never takes any longer. You need not make some educated guess about the running time and hope that it 
never gets much worse. This feature is especially important for real-time computing, in which operations must complete 
by a deadline.
"""

# Average-case
"""
Suppose that you run insertion sort on an array of n randomly chosen numbers. How long does ti take to determine where
in subarray A[:i-1] to insert element A[i]? On average, half the elements in A[:i-1] are less than A[i], and half the 
elements are greater. On average, therefore, A[i] is compared with just half of the subarray A[:i-1], and so A is about 
the half.
"""

# ----------------------------------------------------------------------------------------------------------------------

# Order of growth

"""
We consider only the leading term of a formula (e.g. an²), since the lower-order terms are relatively insignificant for 
large values of n. We also ignore the leading term's constant coefficient, since constant factors are less significant 
than the rate of growth in determing computational efficiency for large inputs. 
Let's suppose that we have n²/100 + 100n + 17 microseconds on an input size n. Although the coefficients of 1/100 for 
the n² term and 100 for the n term differ by four orders of magnitude, the n²/100 dominates the 100n term once n exceeds
10,000/
We write that insertion sort has Θ(n²), which means "roughly proportional when n is large"
"""

# Exercise 2.2-2
def selection_sort(lst):                                                #  cost             times
    for i in range(len(lst)):                                           #   c₀                n
        # Assigning the i-th element and the lowest boundaries          #   c₁                0
        element = lst[i]                                                #   c₂               n-1
        lowest = [0, element]                                           #   c₃               n-1
        # Finding the lowest element in a subarray                      #   c₄                0
                                                                        #                    ₙ
        for j in enumerate(lst[i:]):                                    #   c₅               Σ tᵢ  = (n(n-1)) / 2
                                                                        #                    ᶦ⁼²
                                                                        #                    ₙ
            if j[1] < lowest[1]:                                        #   c₆               Σ tᵢ - 1
                                                                        #                    ᶦ⁼²
                                                                        #                    ₙ
                lowest = j                                              #  c₇                Σ tᵢ - 1
                                                                        #                    ᶦ⁼²
        # Exchanging the lowest and i-th element                        #   c₈                0
        lst[lowest[0]+i] = element                                      #   c₉               n-1
        lst[i] = lowest[1]                                              #   c₁₀              n-1

lst = [6, 5, 4, 3, 2, 1]
selection_sort(lst)

print(lst)

"""
The worst-case:
                                  n (n + 1)         n (n + 1)           n (n + 1)                                                          c₅n   c₅n²   c₆n   c₆n²       c₇n   c₇n² 
    c₀n + c₂(n-1) + c₃(n-1) + c₅ (----------)  + c₆(--------- - 1) + c₇(--------- - 1 ) + c₉(n-1) + c₁₀(n-1) = c₀n + c₂n - c₂ + c₃n - c₃ + --- + ---- + --- + ---- - 1 + --- + ---- - 1 + c₉n - c₉ + c₁₀n - c₁₀ = 
                                       2                2                 2                                                                 2      2     2      2         2      2
  = n²(c₅ + c₆ + c₇)/2 + (c₅/2 +  c₆/2 + c₇/2 + c₀ + c₂ + c₃ + c₉ + c₁₀)n - (c₂ + c₃ + 2 + c₉ + c₁₀)
  So the expression looks like:
   an² + bn - c, which is f(n²)
The best-case:
                                  n (n + 1)                                                     c₅n   c₅n²
    c₀n + c₂(n-1) + c₃(n-1) + c₅ (---------) + c₉(n-1) + c₁₀(n-1) = c₀n + c₂n - c₂ + c₃n - c₃ + --- + ----  + c₉n - c₉ + c₁₀n - c₁₀ = 
                                      2                                                          2      2
   =  (c₅n²)/2 + (c₀ + c₂ + c₃ + c₉ + c₁₀)n -(c₂ + c₃ + c₉ + c₁₀)
   Which is again:
    an² + bn - c, which is f(n²)
"""

# ----------------------------------------------------------------------------------------------------------------------

# Designing algorithms

"""
There are many algorithm designs(Brute Force, Greedy Algorithms, Divide-and-Conquer, Decrease-and-Conquer, Dynamic 
Programming, Reduction / Transform-and-Conquer, Backtracking and Branch-and-Bound), but here we will focus on Divide-and
-Conquer
"""

# The divide-and-conquer method
"""
Many useful algorithms are recursive in structure: to solve a given problem, they recurse (call themselves) one or more 
times to handle closely related sub-problems. These algorithms typically follow the divide-and-conquer method: they 
break the problem into several sub-problems that are similar to the original problem bit smaller in size, solve the 
sub-problems recursively, and then combine these solutions to create a solution to the original problem.
In the divide-and-conquer method, if the problem is small enough - the base case - you just solve it directly without 
recursing. Otherwise - the recursive case - you perform three characteristic steps:
"""

# 1 - Divide
'''
             the problem into one or more sub-problems that are smaller instances of the same problem
'''
# 2 - Conquer
'''
             the sub-problems by solving them recursively
'''
# - Combine
'''
            the sub-problems' solutions to form a solution to the original problem
'''

# ----------------------------------------------------------------------------------------------------------------------

# The Merge Sort

# Steps:
""" 
'Divide' the subarray A[p:r] to be sorted into two adjacent sub-arrays, each of half the size. To do so, compute the 
midpoint q of A[p:r] (taking the average of p and r), and divide A[p:r] into sub-arrays A[p:q] and A[q + 1:r]

'Conquer' by sorting each of the two sub-arrays A[p:q] and A[q+1:r] recursively using merge sort

'Combine' by merging the two sorted sub-arrays A[p:q] and A[q+1:r] back into A[p:r], producing the sorted answer
"""
"""
The recursion 'bottoms out' - it reaches the base case - when the subarray A[p:r] to be sorted has just 1 element, that 
is, when p equals r. 
"""

n = [4, 3, 6, 5, 1, 2, 7]

def merge_sort(n: list) -> None:
    n_length_by2 = len(lst) // 2
    L = n[:n_length_by2 + 1]
    R = n[n_length_by2:]
    print(L, R)

merge_sort(n)



















