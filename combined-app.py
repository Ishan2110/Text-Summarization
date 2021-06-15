from flask import Flask, render_template,request,jsonify, make_response
import requests
import os
import PyPDF2
import numpy as np
import pandas as pd
import bs4 as bs
import urllib.request
import nltk
nltk.download('punkt') # one time execution
import re

from nltk.tokenize import sent_tokenize

app = Flask(__name__)

def get_wiki(url,lines):
    scraped_data = urllib.request.urlopen(url)
    article = scraped_data.read()
    
    parsed_article = bs.BeautifulSoup(article,'lxml')
    
    paragraphs = parsed_article.find_all('p')
    
    article_text = ""

    for p in paragraphs:
        article_text += p.text
    
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)
    
    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    sentence_list = nltk.sent_tokenize(article_text)
    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    sentence_scores = {}
    
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    
    import heapq
    summary_sentences = heapq.nlargest(int(lines), sentence_scores, key=sentence_scores.get)
    
    summary = ' '.join(summary_sentences)
    return(summary)


def get_text(str,lines):
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

def extract_text():
    text = ''
    count=0

    stx=""
    d = "./uploads"

    for path in os.listdir(d):
        full_path = os.path.join(d, path)
        if os.path.isfile(full_path):
            stx=full_path
            # print(full_path)
            # print(type(full_path))
            break

    a=PyPDF2.PdfFileReader(stx)
    # a=PyPDF2.PdfFileReader("./uploads/Get_Started_With_Smallpdf.pdf")
    count=a.getNumPages()
    # print(count)
    # print(a.documentInfo)
    # print(a.getPage(0).extractText())
    for i in range(count):
        pageObj = a.getPage(i)
        text += pageObj.extractText()
    # print(text)
    return text

    
@app.route("/")

def test():
    return render_template("files.html")

def func():
    return "Task completed"

@app.route("/create", methods = ["POST"])

def create_entry():
    req = request.get_json()
    # print(req)

    name = req["name"]
    lines = req["message"]
    # print(name)

    url = (name)
    lines = (lines)

    url_content = get_wiki(url,lines)

    res=make_response(jsonify({"message": url_content}),200)

    return res

@app.route("/text-op", methods = ["POST"])

def create_entry12():
    req = request.get_json()
    # print(req)

    name = req["name"]
    lines = req["message"]
    # print(name)

    stri = (name)
    lines = (lines)

    url_content = get_text(stri,lines)

    res=make_response(jsonify({"message": url_content}),200)

    return res

@app.route("/uploadajax", methods = ["POST"])

def hello():
    file=request.files["file"]
    # print(file)
    file.save(os.path.join("uploads", file.filename))
    return get_text(extract_text(), 4)

if __name__ == "__main__":
    app.run(debug=True)