from flask import Flask, render_template, url_for, request, jsonify
import tensorflow as tf
import requests
import json
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.util import ngrams
from pprint import pprint
import string



url2 = "https://api.themoviedb.org/3/authentication"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YjM4ZDNlOWNmNjAzZTljYzY4ZTM2YWI3ODg0OWRhYSIsInN1YiI6IjY0ODIzZGQ5ZTI3MjYwMDBlOGJmNzk3MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lW2CItRpoOW6BlwgnWw-Bqq_qXAkhhgai5NqgGz1voM"
}
response = requests.get(url2, headers=headers)

model = tf.saved_model.load('C:/Users/suhas/MovieReview')

lem = WordNetLemmatizer()
stopwords = stopwords.words("english")
newstopwords = [',', '.', '-', '!', 's', 'movie', 'film', "n't", 'like', 'one', 'way', 'much', '?', 'another', 'would', 'ca', 'made'
                , 'every', 'even', 'really', 'back', "'s", '*', *string.punctuation, 'thing'
                , 'scene', 'film', 'scene', 'year', 'time', 'http', 'https', 'www', 'could' 
                , 'always', 'start', 'see', 'become', 'becomes', 'get', 'man', '1', '2', '3', '4', '5', '6'
                , 'still', 'give', 'lot', 'screen', 'say', 'never', 'actually']
stopwords.extend(newstopwords)

def normalize(text):
    tokens = word_tokenize(text)
    filtered = [word for word in tokens if word.lower() not in stopwords]
    lemmatized = [lem.lemmatize(word) for word in filtered]
    sentence = " ".join(lemmatized)
    return sentence

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('movieReviewHTML.html')

@app.route('/process', methods=['POST'])
def process():
    data = str(request.get_json())
    url = "https://api.themoviedb.org/3/search/movie?query=" + data
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YjM4ZDNlOWNmNjAzZTljYzY4ZTM2YWI3ODg0OWRhYSIsInN1YiI6IjY0ODIzZGQ5ZTI3MjYwMDBlOGJmNzk3MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lW2CItRpoOW6BlwgnWw-Bqq_qXAkhhgai5NqgGz1voM"
    }

    response = requests.get(url, headers=headers).json()
    results = response['results']
    movie = ""

    try:
        movie = results[0]
    except IndexError:
        allMovieInformation = {'dataAvailable': 'none'}
        return allMovieInformation
    
    popularity = movie['popularity']
    stars = round(movie['vote_average'], 2)
    totalVotes = movie['vote_count']
    id = str(movie['id'])

    url = "https://api.themoviedb.org/3/movie/" + id + "/reviews?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YjM4ZDNlOWNmNjAzZTljYzY4ZTM2YWI3ODg0OWRhYSIsInN1YiI6IjY0ODIzZGQ5ZTI3MjYwMDBlOGJmNzk3MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lW2CItRpoOW6BlwgnWw-Bqq_qXAkhhgai5NqgGz1voM"
        }
    
    reviews = requests.get(url, headers=headers).json()
    totalPages = reviews['total_pages']
    numberofReviews = reviews['total_results']

    url = "https://api.themoviedb.org/3/movie/" + id + "/recommendations?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YjM4ZDNlOWNmNjAzZTljYzY4ZTM2YWI3ODg0OWRhYSIsInN1YiI6IjY0ODIzZGQ5ZTI3MjYwMDBlOGJmNzk3MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lW2CItRpoOW6BlwgnWw-Bqq_qXAkhhgai5NqgGz1voM"
    }
    response = requests.get(url, headers=headers).json()
    responseRec = response['results']
    recTitles = []

    url = "https://api.themoviedb.org/3/movie/" + id +"/keywords"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YjM4ZDNlOWNmNjAzZTljYzY4ZTM2YWI3ODg0OWRhYSIsInN1YiI6IjY0ODIzZGQ5ZTI3MjYwMDBlOGJmNzk3MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lW2CItRpoOW6BlwgnWw-Bqq_qXAkhhgai5NqgGz1voM"
    }
    response = requests.get(url, headers=headers).json()
    responseKey = response['keywords']
    keywords = []

    i = 0
    for entry in responseKey:
        keywords.append(string.capwords(entry['name']))
        if(i < 5):
            try:
                recTitles.append(responseRec[i]['title'])
                i = i + 1
            except IndexError:
                break
    if (len(recTitles) == 0):
        recTitles = "Sorry, no similar movies available"
    else:
        recTitles = ', '.join(recTitles)

    if (len(keywords) == 0):
        keywords = "Sorry, no keywords available"
    else:
        keywords = ', '.join(keywords)

    if (numberofReviews == 0):
        allMovieInformation = {
            'popularity': popularity,
            'stars': stars,
            'totalVotes': totalVotes,
            'dataAvailable': 'limited',
            'recommendations': recTitles,
            'keywords': keywords
        }
        return allMovieInformation

    normalizedList = []
    ratings = []
    corpus = []
    totalPagesforLoop = totalPages + 1

    for pageNumber in range(1, totalPagesforLoop):
        url = "https://api.themoviedb.org/3/movie/" + id + "/reviews?language=en-US&page=" + str(pageNumber)
        headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YjM4ZDNlOWNmNjAzZTljYzY4ZTM2YWI3ODg0OWRhYSIsInN1YiI6IjY0ODIzZGQ5ZTI3MjYwMDBlOGJmNzk3MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lW2CItRpoOW6BlwgnWw-Bqq_qXAkhhgai5NqgGz1voM"
        }
        reviews = requests.get(url, headers=headers).json()
        reviewsData = reviews['results']

        for review in reviewsData:
            details = review['author_details']
            rating = details['rating']
            normReview = normalize(review['content'])
            normalizedList.append(normReview)
            if (str(rating) != 'None'):
                ratings.append(rating)
        
    ratingLength = len(ratings)
    averageRating = ""
    if(np.isnan(np.average(np.array(ratings)))):
        averageRating = "Sorry, no average rating available"
    else:
        averageRating = round(np.average(np.array(ratings)), 2)

    normalizedPredReviews = np.array(model(normalizedList))
    average = round(np.average(normalizedPredReviews), 2)
    normalizedPredReviews = normalizedPredReviews.tolist()
    normalizedPredReviews = [item[0] for item in normalizedPredReviews]
    sentiments = {"positive": 0, "negative": 0}
    for item in normalizedPredReviews:
        if (item < 0.5):
            negnum = sentiments["negative"] + 1
            sentiments.update({"negative": negnum})
        else:
            posnum = sentiments["positive"] + 1
            sentiments.update({"positive": posnum})

    for normReviews in normalizedList:
        words = str(normReviews).split()
        words = [w for w in words if w not in stopwords and w.isalnum()]
        corpus.extend(words)
    
    freq = Counter(corpus).most_common(10)

    bigrams = ngrams(corpus, 2)
    bigramsFreqTuples = Counter(bigrams)
    bigramsFreq = {}
    for key in bigramsFreqTuples:
        newKey = str(key[0] + " " + key[1])
        bigramsFreq[str(newKey)] = bigramsFreqTuples[key]
        
    bigramsFreq = Counter(bigramsFreq).most_common(10)
 
    allMovieInformation = {'popularity': popularity,
                           'stars': stars,
                           'totalVotes': totalVotes,
                           'numberofReviews': numberofReviews,
                           'averageRating': str(averageRating),
                           'ratingLength': ratingLength,
                           'averageReview': str(average),
                           'sentiments': json.dumps(sentiments),
                           'bigrams': json.dumps(bigramsFreq),
                           'freq': json.dumps(freq),
                           'dataAvailable': 'full',
                           'recommendations': recTitles,
                           'keywords': keywords
                           }
    print("All Movie Information")
    pprint(allMovieInformation)
    return allMovieInformation

if __name__ == "__main__":
    app.run(debug=True)
