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










