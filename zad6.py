def func6(a: list, b:list) -> list:
    a.extend(b)
    a= list(set(a))
    for i in range(len(a)):
        a[i] = a[i] ** 3
    return a

print(func6([1, 2, 3], [3, 4, 5]))
