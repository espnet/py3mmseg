#coding:utf-8
from collections import defaultdict
from __init__ import seg_txt
from word2 import WORD2

SMALLCHAR = set(
('很', '则', '该', '次', '给', '又', '里', '号', '着', '名', '可', '更', '由', '下', '至', '或', '多', '大', '新', '并', '让', '她', '已', '向', '其', '股', '点', '们', '所', '会', '要', '于', '前', '来', '万', '比', '只', '及', '地', '队', '个', '不', '说', '第', '元', '人', '一', '分', '被', '我', '这', '到', '都', '从', '等', '时', '以', '上', '后', '就', '将', '而', '还', '他', '但', '对', '也', '与', '为', '中', '年', '月', '日', '有', '和', '是', '在', '了', '的', )
)

STOPWORD = set("的了是在有而以但一我你他它个啊这")

def seg_txt2(txt):
    for i in seg_txt(txt):
        i = i.lower()
        if len(i) > 3:
            yield i
        else:
            i = i.decode("utf-8","ignore")
            if len(i) == 1:
                if "一" <= i <= "龥" and i not in STOPWORD:
                    yield i
            else:
                yield i

def seg_txt_2_dict(txt):
    result = defaultdict(int)
    for word in seg_txt_search(txt):
        result[word] += 1
    return result

def word_len2(s):
    tmp = [u""]
    for i in s:
        if "一" <= i <= "龥" and i not in STOPWORD:
            tmp[-1] += i
        elif tmp[-1]:
            tmp.append(u"")
    result = []
    tmp_word = []
    for y in tmp:
        if y:
            for i in xrange(len(y)-1):
                w = y[i:i+2]
                if w in WORD2:
                  #  if len(tmp) >= 2:
                    result.extend(tmp_word)
                    result.append(w)
                    tmp_word = []
                else:
                    tmp_word.append(w)
            #if len(tmp_word) >= 2:
            result.extend(tmp_word)
            if len(y) <= 5:
                result.append(y)
    return result

def seg_title_search(txt):
    result = []
    buffer = []
    for word in seg_txt(txt):
        word = word.decode("utf-8", "ignore")

        if len(word) == 1:
            buffer.append(word)
        else:
            for i in buffer:
                result.append(i)
            if len(buffer) > 1:
                result.extend(word_len2("".join(buffer)))
            buffer = []
            if len(word) <= 16:
                word = word.lower()
                utf8_word = word.encode("utf-8", "ignore")
                if utf8_word.isalnum():
                    result.append(word)
                else:
                    for i in word:
                        result.append(i)
                    if len(word) <= 2:
                        result.append(utf8_word)
                    else:
                        result.extend(word_len2(word))

    if len(buffer) > 1:
        result.extend(word_len2("".join(buffer)))
    elif buffer:
        if "一" <= buffer[0] <= "龥":
            if buffer[0] not in SMALLCHAR:
                result.append(buffer[0])


    result = [i.encode("utf-8", "ignore") if type(i) is unicode else i for i in result]
#    txt = txt.decode("utf-8", "ignore")

    return result

def seg_keyword_search(txt):
    return  sorted(seg_title_search(txt),key=lambda x:-len(x))

def seg_txt_search(txt):
    result = []
    buffer = []
    def _():
        if len(buffer) > 1:
            result.extend(word_len2("".join(buffer)))
        elif buffer:
            if "一" <= buffer[0] <= "龥":
                if buffer[0] not in SMALLCHAR:
                    result.append(buffer[0])

    for word in seg_txt(txt):
        word = word.decode("utf-8", "ignore")
        if len(word) == 1:
            buffer.append(word)
        else:
            _()
            buffer = []
            if len(word) <= 16:
                word = word.lower()
                utf8_word = word.encode("utf-8", "ignore")
                if utf8_word.isalnum():
                    result.append(word)
                elif len(word) <= 2:
                    result.append(utf8_word)
                else:
                    result.extend(word_len2(word))

    _()

    result = [i.encode("utf-8", "ignore") if type(i) is str else i for i in result]

    return result



if __name__ == "__main__":
    for i in word_len2("是：张无忌"):
        print(i)
