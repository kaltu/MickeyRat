# encoding=utf-8
from crawler_api import crawler
from crawler_api import mongodb
import jieba
import jieba.posseg as pseg
# import math
from os import path
# import operator


# 計算tf_idf
def get_tf_idf(str_list: list)->dict:

    with mongodb.Mongodb() as db:

        tf_idf = db.search_any("record", "the標題", "tf_idf_dict")
        if tf_idf:
            tf_idf_dict = tf_idf[0]
        else:
            tf_idf_dict = {"the標題": "tf_idf_dict"}

        x = len(tf_idf_dict)
        for word in str_list:
            if word not in tf_idf_dict:
                tf_idf_dict[word] = x
                x += 1

        crawler.json_write("tf_idf_dict.txt", tf_idf_dict)

        db.db["record"].remove({"the標題": "tf_idf_dict"})
        db.insert_one("record", tf_idf_dict)

        return tf_idf_dict


# 結疤分詞，string 為一篇文章內容
def get_jie_ba(string: str)->dict:

    jieba.load_userdict(path.join('nlp', 'dict.txt'))        # 一般辭典
    jieba.load_userdict(path.join('nlp', 'movie_list.txt'))  # 電影辭典

    pseg_words = pseg.cut(string)

    word = []
    flag = []

    for one_word in pseg_words:
        if '.' in one_word.word:
            changed_word = one_word.word.replace('.', '*')
        else:
            changed_word = one_word.word
        word.append(changed_word)
        flag.append(one_word.flag)

    ans = {"segments": word, "pos": flag}

    return ans
