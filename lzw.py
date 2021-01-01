#LZW编码
string =input('请输入需要压缩的字符串：')
dictionary = {chr(i): i for i in range(1, 127)}
last = 256#新的编码重第256位开始
p = ""
result1 = []

for c in string:
    pc = p + c
    if pc in dictionary:
        p = pc
    else:
        result1.append(dictionary[p])
        dictionary[pc] = last
        last += 1
        p = c

if p != '':
   result1.append(dictionary[p])
x2 = len(result1)
print('压缩后的编码为：',result1)


#译码
dictionary2 = {i: chr(i) for i in range(1, 127)}  #反向导入ASC码入字典2
last2 = 256

result2 = []
p = result1.pop(0)
result2.append(dictionary2[p])

for c in result1:  #因为编码1删除了，所以c从第二个编码开始
    if c in dictionary2:
        entry = dictionary2[c]
    result2.append(entry)   #将编码译出的字符存入译码数组中
    dictionary2[last2] = dictionary2[p] + entry[0]   #将前后两个码译出的字符组成新的字符存入字典2中
    last2 += 1
    p = c

print('译码结果为：')
print(''.join(result2)) #将译码结果输出为字符串形式
x1 = len(string)  #计算输入的字符串长度
print('字符串长度：',x1)
print('编码后长度：',x2)