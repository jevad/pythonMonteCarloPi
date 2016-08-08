import random
import sys

def calc_pi(end_range):
    total = 0;
    under = 0;
    for i in range(0, end_range):
        total = total + 1;
        x = random.random();
        y = random.random();
        if ((x * x) + (y * y)) <= 1:
            under = under + 1;
    
    return (4 * under)/total

if __name__ == "__main__":
    count = int(sys.argv[1]) if (sys.argv and 2 <= len(sys.argv)) else 1000000
    print("PI:", calc_pi(count))
    