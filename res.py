def dds(lst):
    result = 0
    for i in range(len(lst)):
        if i % 2 == 0:
            result += lst[i]
        else:
            result -= lst[i]
        result *= 2
    return result
num = [1,2,3,4,5]
output = dds(num)
print(output)