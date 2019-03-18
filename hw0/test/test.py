
def add(x, y):
    return x+y

def multi(x, y):
    return x*y

def fold(lis, seed, func):
    count = seed 
    for l in lis:
        count = func(l, count)
    return count 

if __name__ == "__main__":
    lis = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print fold(lis, 0, add)
    print fold(lis, 1, multi)
