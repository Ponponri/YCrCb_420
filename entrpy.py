import math


def factorial(n):
    if(n == 1):
        return 1
    else:
        return factorial(n-1) * n

sum = 0.0
l = 0.97
k = 40
n = 50000
for i in range(1,k+1,1):
    f = factorial(i)
    tmp = (math.exp(-1*l)*(l**i) / f )*(math.log(f/(math.exp(-1*l)*(l**i))))
    sum = sum + tmp

print(f'entropy:{sum}')

print(f'huffman code:{math.ceil(n*sum/math.log(2))} <= b <= {math.floor(n*sum/math.log(2) + n)}')
print(f'arithmatic code:{math.ceil(n*sum/math.log(2))} <= b <= {math.floor(n*sum/math.log(2) + 2)}')

