num = int(input("Enter a number: "))

while num > 0:
    n = num % 10
    is_prime = True
    if n < 2:
        is_prime = False
    else:
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                is_prime = False
                break
    if is_prime:
        print(n)
    num = int(num / 10)


