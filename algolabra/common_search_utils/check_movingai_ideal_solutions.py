# bucket 4, 3rd scenario
# 4	Boston_0_512.map	512	512	352	438	346	423	17.48528137
# (352, 438) => (346, 423) : (17.48528137)
from decimal import Decimal

diag = Decimal(2).sqrt()
# x_delta = 6
# y_delta = 15
# 6 diag + 9 straight
print(f"{Decimal(2).sqrt() * 6 + 9}")

# bucket 5, 3rd scenario
# 512	512	279	25	297	13	22.97056274
# (279, 25) => (297, 13) : (22.97056274)
x_delta = 18
y_delta = 12
print(f"{12 * Decimal(2).sqrt() + 6}")

# 3	6	116	56	133.71067810
# x_delta = 113
# y_delta = 50
print(50 * diag + 63)

# 133.71067810 vs 133.71067811_86547524400844362

# 1.414213562373095048801688724
diag1 = Decimal('1.41421356')
print(50 * diag1 + 63)
# 133.71067800
diag2 = Decimal('1.414213562')
print(50 * diag2 + 63)
# 133.710678100
diag3 = Decimal('1.4142135623')
print(50 * diag3 + 63)
# 133.7106781150

# let's check this
# Boston_0_512.map	512	512	231	450	393	407	179.81118317
# (231, 450), (393, 407)
# x_delta = 162
# y_delta = 43
print(43 * diag1 + 119)
print(43 * diag2 + 119)
print(43 * diag3 + 119)