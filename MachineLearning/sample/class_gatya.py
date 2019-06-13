import random

PATH = "class.txt"
N = 20
with open(PATH) as f:
    l = [s.strip() for s in f.readlines()]

print(random.sample(l,N))
