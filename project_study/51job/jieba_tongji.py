import pandas as pd
import jieba
from collections import Counter
from pprint import pprint


class TongJi():
    def __init__(self):
        data = pd.read_csv(open('data.csv', encoding='gbk'), sep=',')
        self.__data_info = data["info"].copy()

        self.__output = open('res_dep.txt', 'w', encoding='gbk')
        with open('new.txt', 'w', encoding='gbk'):
            pass

    def __substitute(self, r):
        r = r.replace('1', '')
        r = r.replace('2', '')
        r = r.replace('3', '')
        r = r.replace('4', '')
        r = r.replace('5', '')
        r = r.replace('6', '')
        r = r.replace('7', '')
        r = r.replace('8', '')
        r = r.replace('9', '')
        r = r.replace('0', '')
        r = r.replace('nan', '')
        r = r.replace('的', '')
        r = r.replace('、', '')
        r = r.replace('，', '')
        r = r.replace('：', '')
        r = r.replace('；', '')
        r = r.replace('。', '')
        r = r.replace('.', '')
        r = r.replace('）', '')
        r = r.replace('（', '')
        r = r.replace('/', '')
        r = r.replace('-', '')
        r = r.replace(' ', '')
        return r

    def run(self):
        print('[INFO]清洗数据．．．')
        for row in self.__data_info.iteritems():
            r = str(row[1])
            with open('new.txt', 'a+', encoding='gbk')as f:
                f.write(r + '\n')

        print('[INFO]读取数据．．．')
        stop_list = []
        with open('new.txt', 'r', encoding='gbk')as f:
            for line in f.readlines():
                stop_list.append(line.replace('\n', ''))

        w = []
        print('[INFO]数据分词．．．')
        for index, row in self.__data_info.iteritems():
            words = jieba.cut(str(row))
            for word in words:
                # print(word)
                word = self.__substitute(word)
                if word == '':
                    continue
                if word not in stop_list:
                    self.__output.write(word + ' ')
                    w.append(word)
                else:
                    print(word)
            self.__output.write('\n')
        self.__output.close()

        print('[INFO]数据统计．．．')
        corpus = pd.DataFrame(w, columns=['word'])
        corpus['cnt'] = 1

        g = corpus.groupby(['word']).agg({'cnt': 'count'}).sort_values('cnt', ascending=False)
        print('[SUCCESS]展示成果．．．')
        print(g.head(20))

        # counter = Counter(w)

        # 打印前二十高频词
        # pprint(counter.most_common(20))