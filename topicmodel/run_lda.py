from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
from database.mysql_utils import DataAccess
import pickle
import os
from preprocess.preprocess import clean_doc

path = os.path.dirname(__file__)
model_path = os.path.join(path,'lda_model.pickle')

def find_n_word(topic_keywords_matrix, keyword_set, number_of_words=3):
    n = number_of_words
    word_list = []
    for i in range(topic_keywords_matrix.shape[0]):
        index = topic_keywords_matrix[i].argsort()[-n:][::-1]
        word_for_each_topic = []
        for i in index:
            word_for_each_topic.append(keyword_set[i])
        word_list.append(word_for_each_topic)
    return word_list


def run_lda(n_topic, n_word):
    # vn_segment_word = load_database ???
    data = DataAccess().get_documents()
    # content = [clean_doc(d['content']) for d in data]
    # vn_segment_word = ['a_b a_b b_a b_a', 'd_c c_d c_d d_c', 'b_a a_b b_a', 'c_d c_d d_c d_c c_d']
    vn_segment_word = [clean_doc(d['content']) for d in data]
    tv = TfidfVectorizer(max_df=1.0, min_df=0, max_features=5000)
    X = tv.fit_transform(vn_segment_word)
    lda_model = LatentDirichletAllocation(n_topics=n_topic, max_iter=500, learning_method='batch',n_jobs=-1)
    lda_output = lda_model.fit_transform(X)
    # save document_topic matrix to doc_topic_matrix.pickle
    with open(model_path, 'wb+') as f:
        pickle.dump((lda_model,tv), f, protocol=pickle.HIGHEST_PROTOCOL)
    # find n_word for each topic
    keyword_set = tv.get_feature_names()
    topic_keywords_matrix = np.round(lda_model.components_ / lda_model.components_.sum(axis=1)[:, np.newaxis], 4)
    n_word_list = find_n_word(topic_keywords_matrix, keyword_set, n_word)

    result_list = []
    for i in range(n_topic):
        result_list.append(
            {'topic': 'topic' + str(i), 'words': ", ".join(n_word_list[i]), 'name topic': 'topic {0}'.format(i+1)})
    return result_list


def assigne_name_topic_for_document(doc_topic_matrix, assigned_name_list):
    dominant_topic = np.argmax(doc_topic_matrix, axis=1)
    # print(dominant_topic)
    topic_for_docs = []
    for i in dominant_topic:
        topic_for_docs.append(assigned_name_list[i])
    return topic_for_docs


def btn_ok(topics=[]):
    # topics = [{'topic': 'topic 1', 'words': 'word 1, word 2, word 3,..., word n', 'name topic': 'thuế ab'},
    #           {'topic': 'topic 2', 'words': 'word 1, word 2, word 3,..., word n', 'name topic': 'thuế cd'}]
    # documents = load_database_documents ???
    with open(model_path, 'rb') as f:
        lda_model, tv = pickle.load(f)
    docs = DataAccess().get_documents()
    doc_topic_matrix = lda_model.transform(tv.transform([clean_doc(d['content']) for d in docs]))
    assigned_name_list = []
    for i in range(len(topics)):
        assigned_name_list.append(topics[i]['name topic'])
    a = assigne_name_topic_for_document(doc_topic_matrix, assigned_name_list)

    document_topic_list = []
    for i in range(len(a)):
        document_topic_list.append({'so_van_ban': docs[i]['so_van_ban'], 'trich_yeu_noi_dung': docs[i]['trich_yeu'], 'topic': a[i]})
    return document_topic_list

def main():
    topics = run_lda(10, 10)
    print('\n\ntopic\n\n')
    for topic in topics:
        print(topic)

    doc_topics = btn_ok(topics)
    doc_topics = sorted(doc_topics, key=lambda d: d['topic'])
    print('\n\ndocument\n\n')
    for doc in doc_topics:
        print(doc)

# n_topic = 3 do topics = ... dong thu 52
if __name__ == '__main__':
    # import json
    # data = DataAccess().get_documents()
    # json.dump(data,open('data.json','w',encoding='utf-8'),ensure_ascii=False)

    data = DataAccess().get_documents()[:10]

    # vn_segment_word = ['a_b a_b b_a b_a', 'd_c c_d c_d d_c', 'b_a a_b b_a', 'c_d c_d d_c d_c c_d']
    vn_segment_word = [d['content'] for d in data]
    tv = TfidfVectorizer(max_df=1.0, min_df=0, max_features=5000)
    X = tv.fit_transform(vn_segment_word)
    lda_model = LatentDirichletAllocation(n_topics=2, n_components=10, max_iter=500, learning_method='batch', n_jobs=-1)
    lda_output = lda_model.fit_transform(X)
    print(lda_output)
    print(lda_model.set_params(n_topics = ["topic1","topic2"]))
    print(lda_model.transform(X[:5]))



