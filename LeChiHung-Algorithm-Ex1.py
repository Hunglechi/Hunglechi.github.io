def sumInteger(n):
    S = 0
    sum = 0
    dem = -1
    for i in range(1, n + 1):
        sum = sum + i
        S = S + (-1) ** (i + 1) / sum
    return S


while True:
    try:
        n = int(input("Enter a positive integer number: "))
        if n < 0:
            raise Exception
        result = sumInteger(n)
        print(f"The sum of function is: ")
        print(result)
        break
    except ValueError:
        print("The number must be a positive number.")
    except Exception:
        print("The number must be positive...................")
