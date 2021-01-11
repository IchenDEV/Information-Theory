def encode(string):
    dictionary = {chr(i): i for i in range(1, 127)}
    last = 256#新的编码重第256位开始
    p = ""
    result = []
    for c in string:
        pc = p + c
        if pc in dictionary:
            p = pc
        else:
            result.append(dictionary[p])
            dictionary[pc] = last
            last += 1
            p = c
    if p != '':
        result.append(dictionary[p])
    return result

def decode(result):
    #译码
    dictionary2 = {i: chr(i) for i in range(1, 127)}  #反向导入ASC码入字典2
    last2 = 256

    result2 = []
    p = result.pop(0)
    result2.append(dictionary2[p])

    for c in result:  #因为编码1删除了，所以c从第二个编码开始
        if c in dictionary2:
            entry = dictionary2[c]
        result2.append(entry)   #将编码译出的字符存入译码数组中
        dictionary2[last2] = dictionary2[p] + entry[0]   #将前后两个码译出的字符组成新的字符存入字典2中
        last2 += 1
        p = c
    return ''.join(result2)



#LZW编码
string =input('请输入需要压缩的字符串：')
enc=encode(string)
print('压缩后的编码为：',enc)
print('译码结果为：',decode(enc))
