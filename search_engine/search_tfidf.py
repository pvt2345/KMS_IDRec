import pickle
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocess.preprocess import process_text
import pandas as pd

# path =
class SearchTfIdf:
    path = os.path.join(os.path.dirname(__file__),'tfidfvectorizer.pkl')

    def __init__(self, path_tfidfvectorizer=None):
        if not os.path.exists(self.path):
            self.tfidfvectorizer = TfidfVectorizer(ngram_range=[1,3])
        else:
            self.tfidfvectorizer = pickle.load(open(self.path, 'rb'))

    def fit(self, Tokens):
        data = [item['tokens'] for item in Tokens]
        tfidf_matrix = self.tfidfvectorizer.fit_transform(data)
        pickle.dump(tfidf_matrix, open('train.txt', 'wb'))
        pickle.dump(self.tfidfvectorizer,open(self.path,'wb'))

    def search(self, document_search, Tokens,print_data = False):
        document_search = process_text(document_search)
        # matrix = pickle.load(open('train.txt', 'rb'))
        document_raw = [doc['tokens'] for doc in Tokens]
        matrix = self.tfidfvectorizer.transform(document_raw)
        vecto_search = self.tfidfvectorizer.transform([document_search])
        scores = cosine_similarity(vecto_search, matrix)[0]
        results = []
        for doc,score in zip(Tokens,scores):
            results.append(
            {
                'reference': doc.get('reference'),
                'title': doc.get('tieu_de','').split('|')[-1],
                'content': doc.get('content'),
                'score': score,
                'index': ''
            })
        if print_data:
            table = pd.DataFrame.from_records(results)
            print(table)
            print("\n Best matching Result : \n", table[table.score == max(scores)])
        return results

searchtfidf = SearchTfIdf()
if __name__ == '__main__':
    from database.mysql_utils import DataAccess

    _da = DataAccess()
    Tokens = _da.GetTokens()
    a = SearchTfIdf()
    a.fit(Tokens)
    a.search('danh mục hàng tiêu dùng phục vụ xác định thời hạn', Tokens)



