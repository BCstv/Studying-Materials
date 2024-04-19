"""
← (Left Arrow) - ASCII: 2190
→ (Right Arrow) - ASCII: 2192
↔ (Left Right Arrow) - ASCII: 2194
≡ (Identical To) - ASCII: 2261
≠ (Not Equal To) - ASCII: 2260
≤ (Less Than or Equal To) - ASCII: 2264
≥ (Greater Than or Equal To) - ASCII: 2265
∞ (Infinity) - ASCII: 221E
∈ (Element of) - ASCII: 2208
∉ (Not an Element of) - ASCII: 2209
∑ (Summation) - ASCII: 2211
∏ (Product) - ASCII: 220F
√ (Square Root) - ASCII: 221A
∙ (Bullet) - ASCII: 2219
∘ (Ring Operator) - ASCII: 2218
∩ (Intersection) - ASCII: 2229
∪ (Union) - ASCII: 222A
∉ (Not an Element of with slash) - ASCII: 2209
∅ (Empty Set) - ASCII: 2205
⊆ (Subset of or Equal To) - ASCII: 2286
⊇ (Superset of or Equal To) - ASCII: 2287
⊂ (Proper Subset of) - ASCII: 2282
⊃ (Proper Superset of) - ASCII: 2283
⊄ (Not a Subset of) - ASCII: 2284
⊅ (Not a Superset of) - ASCII: 2285
⊕ (Exclusive Or) - ASCII: 2295
⊗ (Tensor Product) - ASCII: 2297
⊥ (Perpendicular) - ASCII: 22A5
∥ (Parallel) - ASCII: 2225
∣ (Divides) - ASCII: 2223
∤ (Does Not Divide) - ASCII: 2224
⋅ (Dot Operator) - ASCII: 22C5
∋ (Contains As Member) - ASCII: 220B
∍ (Element of with Long Horizontal Stroke) - ASCII: 220D
∎ (End of Proof) - ASCII: 220E
⊕ (XOR) - ASCII: 2295
Θ (Theta) - ASCII: 920
O (Big O) - ASCII: 79
Ω (Big Omega) - ASCII: 937
o (Small O) - ASCII: 111
⌀ (Empty Set) - ASCII: 8960
⟶ (Long Right Arrow) - ASCII: 10230
∝ (Proportional to) - ASCII: 8733
∃ (There exists) - ASCII: 8707
∀ (For all) - ASCII: 8704
∇ (Nabla) - ASCII: 8711
Σ (Capital Sigma) - ASCII: 931
μ (Mu) - ASCII: 956
λ (Lambda) - ASCII: 955
ε (Epsilon) - ASCII: 949
δ (Delta) - ASCII: 948
η (Eta) - ASCII: 951
θ (Theta) - ASCII: 952
ω (Omega) - ASCII: 969
∉̸ (Not an Element of with Slash) - ASCII: 8953
∧ (Logical AND) - ASCII: 8743
∨ (Logical OR) - ASCII: 8744
→ (Right Arrow) - ASCII: 8594
← (Left Arrow) - ASCII: 8592
↔ (Left Right Arrow) - ASCII: 8596
↦ (Right Arrow with Tail) - ASCII: 8614
↣ (Right Arrow with Hook) - ASCII: 8615
↝ (Rightwards Squiggle Arrow) - ASCII: 8617
⤵ (Downwards Arrow with Tip Leftwards) - ASCII: 10549
↑ (Up Arrow) - ASCII: 8593
↓ (Down Arrow) - ASCII: 8595
⇔ (Double Right Left Arrow) - ASCII: 8660
⋅ (Dot Operator) - ASCII: 8901

₀
₁
₂
₃
₄
₅
₆
₇
₈
₉
ₙ

⁰
¹
²
³
⁴
⁵
⁶
⁷
⁸
⁹
ⁿ

"""
# ----------------------------------------------------------------------------------------------------------------------

# Algorithm

# An algorithm - any well-designed computational procedure that takes some value, or set of values, as input and
# produces some value, or set of values, as output in a finite amount of time. An algorithm is thus a sequence of
# computational steps that transform the input into the output

# A computational problem - the statement of the problem specifies in general terms the desired input/output
# relationship for problem instances, typically of arbitrarily large size.

# Suppose you have to sort a sequence of numbers into monotonically increasing order.
# Here is how we define the sorting problem:
# Input: A sequence of numbers {a₁, a₂, ..., aₙ}
# Output: A permutation (reordering) {a₁́, a₂́, ..., aₙ́ } of the input sequence such that a₁́ ≤ a₂́ ≤ ... ≤ aₙ́

# Thus, given the input sequence {31, 41, 59, 26, 41, 58}, a correct sorting algorithm returns as output the sequence
# {26, 31, 41, 41, 58, 59}

# An instance - an input sequence of the sorting problem. It needed to compute a solution to the problem

# An algorithm for a computational problem is correct if, for every problem instance provided as input, it
# halts - finishes its computing in finite time - and outputs the correct solution to the problem instance

# A correct algorithm solves the given computational problem

# Incorrect algorithms sometimes may be useful if you can control their error rate

# ----------------------------------------------------------------------------------------------------------------------

# Data Structures

# A data structure is a way to store and organize sata in order to facilitate access and modifications. Using the
# appropriate data structure or structures is an important part of algorithm design.

# No single data structure works well for all purposes, and so you should know the strengths and limitations of several of them

# For each function f(n) and time t in the following table, determine the largest size n of a problem that cna be solved
# in time t, assuming that the algorithm to solve the problem takes f(n) microseconds

"""
 _________________________________________________________________________________________________________
| Time          | 1 second | 1 minute | 1 hour   | 1 day     | 1 month    | 1 year        | 1 century     |
|---------------|----------|----------|----------|-----------|------------|---------------|---------------|
| log(n)        | 10^6     | 6*10^7   | 3.6*10^9 | 8.64*10^10| 2.63*10^12 | 3.15*10^13    | 3.15*10^15    |
| sqrt(n)       | 10^12    | 3.6*10^15| 1.3*10^19| 7.46*10^21| 6.94*10^24 | 9.86*10^26    | 9.86*10^30    |
| n             | 10^6     | 3.6*10^7 | 3.6*10^9 | 8.64*10^10| 2.63*10^12 | 3.15*10^13    | 3.15*10^15    |
| nlog(n)       | 62746    | 2.8*10^6 | 1.3*10^8 | 5.3*10^9  | 1.8*10^11  | 2.5*10^12     | 2.8*10^14     |
| n^2           | 1000     | 60000    | 3600000  | 1.5*10^8  | 1.6*10^10  | 1.8*10^12     | 1.8*10^16     |
| n^3           | 100      | 3912     | 153847   | 4420*10^3 | 4420*10^3  | 4420*10^3     | 4420*10^3     |
| 2^n           | 19       | 25       | 31       | 36        | 41         | 45            | 55            |
| n!            | 9        | 11       | 12       | 13        | 15         | 16            | 20            |
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""