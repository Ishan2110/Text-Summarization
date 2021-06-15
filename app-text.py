from flask import Flask, render_template,request,jsonify, make_response
import numpy as np
import pandas as pd
import nltk
nltk.download('punkt') # one time execution
import re

from nltk.tokenize import sent_tokenize

app = Flask(__name__)

def get_content(str,lines):
    output = ''
    sentences = []
    
    sentences.append(sent_tokenize(str))
    
    # print(sentences)
    
    sentences = [y for x in sentences for y in x] # flatten list
    
    # Extract word vectors
    
    word_embeddings = {}
    f = open('glove.6B.100d.txt', encoding='utf-8')
    
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f.close()
    
    # remove punctuations, numbers and special characters
    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
    
    # make alphabets lowercase
     
    clean_sentences = [s.lower() for s in clean_sentences]
    
    nltk.download('stopwords')
    
    from nltk.corpus import stopwords
    stop_words = stopwords.words('english')
    
    # function to remove stopwords
     
    def remove_stopwords(sen):
        sen_new = " ".join([i for i in sen if i not in stop_words])
        return sen_new
        
    # remove stopwords from the sentences
     
    clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]
    
    # Extract word vectors
    
    word_embeddings = {}
    f = open('glove.6B.100d.txt', encoding='utf-8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f.close()
    
    sentence_vectors = []
    
    for i in clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
        else:
            v = np.zeros((100,))
        sentence_vectors.append(v)
        
    # similarity matrix
    
    sim_mat = np.zeros([len(sentences), len(sentences)])
    
    from sklearn.metrics.pairwise import cosine_similarity
    
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]
                
    import networkx as nx
    
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)
    
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    
    for i in range(int(lines)):
        output+=(ranked_sentences[i][1])

    return output


@app.route("/")

def test():
    return render_template("files.html")

def func():
    return "Task completed"

@app.route("/text-op", methods = ["POST"])

def create_entry():
    req = request.get_json()
    print(req)

    name = req["name"]
    lines = req["message"]
    # print(name)

    stri = (name)
    lines = (lines)

    url_content = get_content(stri,lines)

    res=make_response(jsonify({"message": url_content}),200)

    return res

if __name__ == "__main__":
    app.run(debug=True)