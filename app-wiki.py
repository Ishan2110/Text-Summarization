from flask import Flask, render_template,request,jsonify, make_response
import requests
import numpy as np
import bs4 as bs
import urllib.request
import re
import nltk

app = Flask(__name__)

def get_content(url,lines):
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

@app.route("/")

def test():
    return render_template("files.html")

def func():
    return "Task completed"

@app.route("/create", methods = ["POST"])

def create_entry():
    req = request.get_json()
    print(req)

    name = req["name"]
    lines = req["message"]
    print(name)

    url = (name)
    lines = (lines)

    url_content = get_content(url,lines)

    res=make_response(jsonify({"message": url_content}),200)

    return res

if __name__ == "__main__":
    app.run(debug=True)