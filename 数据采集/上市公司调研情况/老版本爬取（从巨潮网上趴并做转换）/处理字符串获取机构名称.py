import re
from 函数目录 import profile as pf

def 对PDF文件的字符串进行预处理(results):
    results = results.strip().strip('。')
    #print(results)
    #print(len(results)/2+0.5,len(results.replace(' ', '')))
    if len(results)/2+0.5 == len(results.replace(' ', '')):
        return ''
    #print(len(results)/2+0.5,len(results.replace(' ', '')))

    需要匹配的字符串 = [ '□', '■','√','其他']
    for element in 需要匹配的字符串:
        element = element.replace(' ', '')
        if element in results:
            return ''
    return results

def 处理表格中的字符串(string):

    returnList = []
    #先做一次分割
    myResultList = [x for x in re.split(";|,|\||\t|、|；|：|：|\n|，|\|", string) if x]

    for element in myResultList:
        element = element.strip().strip('。')

        if 判断字符串是否包含某个字符串组(element):
            #掠过不做操作
            pass
        elif 检查字符串是否含有英文(element):
            if len(element) < 9:
                #忽略这个数据
                #returnList.append(element)
                pass
            else:
                # 加入返回的list
                #print(element)
                returnList.append(element)
                pass
        elif len(element) >= 20:
            #再进行一次分割
            myResultList2 = [x for x in re.split(";|,|\||\t|、|；|：|：|\n|，| |。|", element) if x]
            for element in myResultList2:
                if len(element) > 3:
                    # 加入返回的list
                    returnList.append(element)
                    #print(len(element),element)
                    pass
                else:
                    #print(len(element), element)
                    pass
        elif len(element) == 4 and len(element.split()) == 2:
            #print(len(element.split()[0]),len(element.split()[1]))
            pass
        else:
            # 加入返回的list
            if len(element) > 3:
                # 加入返回的list
                # print(len(element),element)
                returnList.append(element)
                pass
            else:
                # print(len(element), element)
                pass
    return returnList

def 检查字符串是否含有英文(stringIn):
    my_re = re.compile(r'[A-Za-z]',re.S)
    res = re.findall(my_re,stringIn)
    if len(res):
        return True
    else:
        return False

def 判断字符串是否包含某个字符串组(string):
    for element in pf.要去除的字符串组:
        if element in string:
            return True
    return False