import os
import numpy as np
import json
from models.baseline.data_preprocess import tokenize, term_frequency, get_corpus
from models.baseline.model_training import create_model

def predict_neg_pos(review):
    model = create_model()
    model_name = sorted(os.listdir("./models/baseline/checkpoints/"))[-1]
    model.load_weights('./models/baseline/checkpoints/' + model_name)

    token = tokenize(review)
    with open('./models/baseline/data/train_docs.json') as train:
        train_docs = json.load(train)
    text = get_corpus(train_docs)

    selected_words = [word[0] for word in text.vocab().most_common(10000)]
    term = term_frequency(token, selected_words)
    data = np.expand_dims(np.asarray(term).astype("float32"), axis=0)
    score = float(model.predict(data))
    if(score > 0.5):
        return 1
        print("[{}]는 {:.2f}% 확률로 긍정 리뷰이지 않을까 추측해봅니다.^^\n".format(review, score * 100))
    else:
        return 0
        print("[{}]는 {:.2f}% 확률로 부정 리뷰이지 않을까 추측해봅니다.^^;\n".format(review, (1 - score) * 100))

if __name__ == '__main__':
    rev = ["올해 최고의 영화! 세 번 넘게 봐도 질리지가 않네요.",
            "배경 음악이 영화의 분위기랑 너무 안 맞았습니다. 몰입에 방해가 됩니다.",
            "주연배우 때문에 봤어요"
            ]

    for review in rev:
        predict_neg_pos(review)