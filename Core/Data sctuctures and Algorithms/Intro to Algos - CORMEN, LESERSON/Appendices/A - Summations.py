# ----------------------------------------------------------------------------------------------------------------------
#                                                 SUMMATIONS
# ----------------------------------------------------------------------------------------------------------------------

# Summation formulas and properties


"""
Given a sequence a₁, a₂, ..., aₙ of numbers, where n is a non-negative integer, the finite sum a₁ + a₂ + ... + aₙ can be 
expressed as:
ₙ - Last value of k
Σ  aₖ  - Formula for the terms
ᵏ⁼¹ - First value of k
The value of a finite series is always well-defined, and the order in which its terms are added does not matter.
Given an infinite sequence a₁, a₂, ... . of numbers, we can write their infinite sum a₁ + a₂ + ... as:
∞
Σ aₖ
ᵏ⁼¹
which means:
            ₙ
lim n -> ∞  Σ aₖ
            ᵏ⁼¹
If the limit does not exist, the series 'diverges', and otherwise 'converges'. The terms of a convergent series cannot 
always be added in any order. You can, however, rearrange the terms of an absolutely convergent series, that is, a series
∞                           ∞
Σ aₖ   for which the series Σ |aₖ| also converges
ᵏ⁼¹                        ᵏ⁼¹


"""

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
n = len(a)
c = 3
Σ = 0
k = 1
for i in range(k-1, n):
    Σ += c*a[i] + b[i]
print(Σ)

# ₙ
# Σ (3aₖ + bₖ)
# ᵏ⁼¹

# ----------------------------------------------------------------------------------------------------------------------

# Linearity

"""
For any real number c and any finite sequences a₁, a₂, ..., aₙ and b₁, b₂, ..., bₙ
ₙ             ₙ         ₙ
Σ (caₖ+bₖ) = cΣ caₖ  +  Σ bₖ
ᵏ⁼¹          ᵏ⁼¹      ᵏ⁼¹
"""

# ----------------------------------------------------------------------------------------------------------------------

# Arithmetic Series

"""
The summation
ₙ                             n(n + 1)
Σ k = 1 + 2 + ... + n      = ---------
ᵏ⁼¹                              2

A general arithmetic series includes an additive constant a ≥ 0 and a constant coefficient b > 0 in each term, but has 
the same total asymptotically
ₙ
Σ (a + bk)
ᵏ⁼¹
"""

# ----------------------------------------------------------------------------------------------------------------------

# Sums of squares and cubes

"""
ₙ           n(n + 1)(2n + 1)
Σ k²     = ----------------- 
ᵏ⁼¹               6
ₙ           n²(n+1)²
Σ k³     = ----------
ᵏ⁼¹            4
"""






















