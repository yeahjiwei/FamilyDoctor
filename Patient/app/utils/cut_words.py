"""
结巴分词
"""

import jieba


def cut_words(text):
    new_text = jieba.lcut(text, cut_all=True, HMM=True)
    return new_text


if __name__ == '__main__':
    print(cut_words('皮肤科啊'))