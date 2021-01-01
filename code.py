import numpy as np
precision = 27  # 精度
whole = 2 ** precision
half = int(whole / 2)
quarter = int(half / 2)
symbolMax = 900  # 序列中整数的最大值
symbolMin = 0  # 序列中整数的最小值
# 计算频率表
symbols = np.arange(symbolMin, symbolMax+1)
frequencyTable = np.vstack([np.ones(len(symbols))/len(symbols), symbols]).T  # 符号频率分布为拉普拉斯分布，使用拉普拉斯分布公式代替计算频率表

# 自适应算术编码中重新计算概率表的函数
def compute_c_d_R(frequencyTable, symbol):
    index = np.argwhere(frequencyTable[:, 1] == symbol)
    frequencyTable[index[0, 0], 0] = frequencyTable[index[0, 0], 0] + 0.1
    c = np.zeros(frequencyTable.shape)
    c[:, 1] = frequencyTable[:, 1]
    c[0, 0] = 0
    for i in range(1, len(frequencyTable)):
        c[i, 0] = frequencyTable[i - 1, 0] + c[i - 1, 0]
    d = np.zeros(c.shape)
    d[:, 1] = c[:, 1]
    d[:, 0] = c[:, 0] + frequencyTable[:, 0]
    c = {c[i, 1]: c[i, 0] for i in range(len(c))}
    d = {d[i, 1]: d[i, 0] for i in range(len(d))}
    return c, d, d[symbols[-1]]

# 自适应算术编码器
def arithmetic_encoder(zigzagArray):
    # 算术编码
    # 设置算术编码参数
    c = np.zeros(frequencyTable.shape)
    c[:, 1] = frequencyTable[:, 1]
    c[0, 0] = 0
    R = np.sum(frequencyTable[:, 0])
    for i in range(1, len(frequencyTable)):
        c[i, 0] = frequencyTable[i - 1, 0] + c[i - 1, 0]
    d = np.zeros(c.shape)
    d[:, 1] = c[:, 1]
    d[:, 0] = c[:, 0] + frequencyTable[:, 0]
    c = {c[i, 1]: c[i, 0] for i in range(len(c))}
    d = {d[i, 1]: d[i, 0] for i in range(len(d))}
    a = int()
    b = int(whole)
    s = int()
    outputString = ''
    length = len(zigzagArray)
    for i in range(length):
        w = b - a
        if w == 0 or w == 1:
            print("precision error")
        b = a + int(w * d[round(zigzagArray[i], 2)] / R)
        a = a + int(w * c[round(zigzagArray[i], 2)] / R)
        c, d, R = compute_c_d_R(frequencyTable, zigzagArray[i])
        while b < half or a > half:
            if b < half:
                outputString += '0' + s * '1'
                s = 0
                a = int(2 * a)
                b = int(2 * b)
            elif a > half:
                outputString += '1' + s * '0'
                s = 0
                a = 2 * int(a - half)
                b = 2 * int(b - half)
        while a > quarter and b < 3 * quarter:
            s = s + 1
            a = 2 * (a - quarter)
            b = 2 * (b - quarter)
    s = s + 1
    if a <= quarter:
        outputString += '0' + s * '1'
    else:
        outputString += '1' + s * '0'
    return outputString


# 自适应解码器
def arithmetic_decoder(inputString, length):
    zigzagArray = np.zeros(length)
    # 设置算术编码参数
    c = np.zeros(frequencyTable.shape)
    c[:, 1] = frequencyTable[:, 1]
    c[0, 0] = 0
    R = np.sum(frequencyTable[:, 0])
    for i in range(1, len(frequencyTable)):
        c[i, 0] = frequencyTable[i - 1, 0] + c[i - 1, 0]
    d = np.zeros(c.shape)
    d[:, 1] = c[:, 1]
    d[:, 0] = c[:, 0] + frequencyTable[:, 0]
    c = {c[i, 1]: c[i, 0] for i in range(len(c))}
    d = {d[i, 1]: d[i, 0] for i in range(len(d))}
    a = int(0)
    b = int(whole)
    M = len(inputString)
    z = 0
    i = 1
    zk = 0
    while i <= precision and i <= M:
        if inputString[i - 1] == '1':
            z = z + 2**(precision - i)
        i += 1
    while zk < length:
        for j in frequencyTable[:, 1]:
            w = b - a
            if w == 0 or w == 1:
                print("precision error")
            b0 = a + int(w * d[j] / R)
            a0 = a + int(w * c[j] / R)
            if a0 <= z < b0:
                zigzagArray[zk] = j
                zk += 1
                a = a0
                b = b0
                c, d, R = compute_c_d_R(frequencyTable, j)
                break
        while b < half or a > half:
            if b < half:
                a = 2 * a
                b = 2 * b
                z = 2 * z
            elif a > half:
                a = 2 * (a - half)
                b = 2 * (b - half)
                z = 2 * (z - half)
            if i <= M and inputString[i - 1] == '1':
                z = z + 1
            i = i + 1
        while a > quarter and b < 3 * quarter:
            a = 2 * (a - quarter)
            b = 2 * (b - quarter)
            z = 2 * (z - quarter)
            if i <= M and inputString[i - 1] == '1':
                z = z + 1
            i = i + 1
    return zigzagArray