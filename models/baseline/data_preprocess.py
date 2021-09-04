from os import sep
from konlpy.tag import Okt
import json
import os 
import nltk
import matplotlib.pyplot as plt
import matplotlib as mpl
import warnings
import numpy as np

okt = Okt()

def read_data(filename):
    with open(filename, 'r') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        # txt 파일의 헤더(id document label)는 제외하기
        data = data[1:]
    return data

def tokenize(doc):
    # norm은 정규화, stem은 stem으로 표시
    return ['/'.join(word) for word in okt.pos(doc, norm=True, stem=True)]



def tagged_json(train_data, test_data):
    # 태깅이 오래 걸리기 때문에 json파일로 결과를 저장한다
    if os.path.isfile('./data/train_docs.json'):
        print('already have json')
        with open('./data/train_docs.json') as train:
            train_docs = json.load(train)
        with open("./data/test_docs.json") as test:
            test_docs = json.load(test)

    else:
        print("start making json")

        train_docs = [(tokenize(row[1]), row[2]) for row in train_data]
        test_docs = [(tokenize(row[1]), row[2]) for row in test_data]
        
        # save as json
        with open('./data/train_docs.json', 'w', encoding='utf-8') as make_file:
            json.dump(train_docs, make_file, ensure_ascii=False, indent='\t')
        with open('./data/test_docs.json', 'w', encoding='utf-8') as make_file:
            json.dump(test_docs, make_file, ensure_ascii=False, indent='\t')

    return train_docs, test_docs

def term_frequency(doc, selected_words):
    return [doc.count(word) for word in selected_words]

def get_corpus(train_docs):
    tokens = [n for doc in train_docs for n in doc[0]]
    return nltk.Text(tokens, name="NMSC")
    
########################################################################################

if __name__ == "__main__":
    print('start program')
    train_data = read_data('../nsmc/ratings_train.txt')
    test_data = read_data('../nsmc/ratings_test.txt')

    train_docs, test_docs = tagged_json(train_data, test_data) # save as json to save time
    print("json done!")

    tokens = [n for doc in train_docs for n in doc[0]]
    text = get_corpus(train_docs)
    print(len(text.tokens))
    print(len(set(text.tokens)))
    print(text.vocab().most_common(10))


    # plotting top 50 frequent words
    mpl.rcParams['font.size'] = 12
    warnings.filterwarnings('ignore')
    plt.figure(figsize=(20,16))
    text.plot(50)
    plt.savefig('./figure/most_common_10.png')


    selected_words = [word[0] for word in text.vocab().most_common(10000)]
    train_X = [term_frequency(d, selected_words) for d, _ in train_docs]
    test_X = [term_frequency(d, selected_words) for d, _ in test_docs]
    train_y = [c for _, c in train_docs]
    test_y = [c for _, c in test_docs]

    X_train = np.asarray(train_X).astype('float32')
    X_test = np.asarray(test_X).astype('float32')

    y_train = np.asarray(train_y).astype('float32')
    y_test = np.asarray(test_y).astype('float32')

    np.save('./data/X_train', X_train)
    np.save('./data/X_test', X_test)
    np.save("./data/y_train", y_train)
    np.save("./data/y_test", y_test)