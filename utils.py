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

def printChart(data):
    import matplotlib.pyplot as plt

    #create figure    
    plt.figure()

    #define width of candlestick elements
    width = .4
    width2 = .05

    #define up and down prices
    up = data[data.close>=data.open]
    down = data[data.close<data.open]

    #define colors to use
    col1 = 'green'
    col2 = 'red'


    #plot up prices
    plt.bar(up.index,up.close-up.open,width,bottom=up.open,color=col1)
    plt.bar(up.index,up.high-up.close,width2,bottom=up.close,color=col1)
    plt.bar(up.index,up.low-up.open,width2,bottom=up.open,color=col1)


    #plot down prices
    plt.bar(down.index,down.close-down.open,width,bottom=down.open,color=col2)
    plt.bar(down.index,down.high-down.open,width2,bottom=down.open,color=col2)
    plt.bar(down.index,down.low-down.close,width2,bottom=down.close,color=col2)


    #rotate x-axis tick labels
    plt.xticks(rotation=45, ha='right')

    #display candlestick chart
    plt.show()
