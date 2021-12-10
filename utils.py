def max(list):
    max = list[0]
    for l in list:
        if l > max:
            max = l
    return max

def min(list):
    min = list[0]
    for l in list:
        if l < min:
            min = l
    return min