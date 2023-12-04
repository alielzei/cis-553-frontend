from flask import Flask
from flask import request as recieved_request
import json
import time
# from requests import request
from flask_cors import CORS

import urllib.parse
import os
import openai
import re


from serpapi import GoogleSearch


api_key = None
# Check if api key is in env
if 'OPENAI_API_KEY' in os.environ:
    api_key = os.environ['OPENAI_API_KEY']
    print(f"found OPENAI API KEY: {api_key} in env")

# If not, check if api key is in file
if not api_key:
    with open('backend/api.key', 'r') as file:
        api_key = file.readline().strip()  # Read the first line

openai.api_key = api_key

serpapi_apikey = "0e7dbfbcc1a20145c678bca44458f6a785f8815510167755a047443d8b3f88e9"


NOT_RELEVANT = "NOT_RELEVANT"

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Hello World!"


@app.route('/', methods=['POST'])
def prompt():
    recieved_data = recieved_request.json
    question = recieved_data['question']
    # This is needed for showtimes location
    location = (recieved_data['city'], recieved_data['state'])

    resp = dict()

    resp['time'] = time.time()

    ans = "Error"
    # filter out non-showtimes question
    if check_if_showtimes_needed(question):
        # showtimes question
        ans_showtimes = answer_showtimes_question(question, location)
        ans_suggestion = []
    else:
        # not showtimes question
        ans_showtimes = []
        ans_suggestion = answer_suggestion_question(question)

    ans = {
            "suggestions": ans_suggestion,
            "showtimes": ans_showtimes
         }

    js = json.dumps(ans, indent=4)
    return js, 200


def answer_suggestion_question(question):
    """
    Function to answer a question about movie suggestions
    """
    
    prompt_template = """You are going to be asked a question, between two sequences %^& question goes here %^& .
    If the question is indeed about movies, then output a list of movies. Attempt to answer the question, responding with ONLY a list of movies, most relevant to the question.
    Dont give introdution, or preface list of movies with anything or say anything after movie list.
    The list should be formatted as following:
    <movie_start> movie name > year released > main actors > short description <movie_end>
    <movie_start> movie name > year released > main actors > short description <movie_end>
    """

    prompt = prompt_template + f"%^& {question} %^& "

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": prompt}]
    )
    #print(completion)
    ans = completion["choices"][0]["message"]["content"]

    if ans == NOT_RELEVANT:
        # TO-DO: 
        # return error message
        return "Not relevant request", 200

    movie_list = list()

    try:
        raw_list = ans.split("<movie_start>")[1:]
        for raw_movie in raw_list:
            split_raw_mov_tmp = raw_movie.split("<movie_end>")[0]
            split_raw_mov = split_raw_mov_tmp.split(" > ")
            # TO-DO:
            # sptrip spaces and newlines from each elem, just in case
            d = {
                "name":  split_raw_mov[0],
                "year":  split_raw_mov[1],
                "actors":  split_raw_mov[2],
                "desc":  split_raw_mov[3],
            }
            movie_list.append(d)
    except Exception as error:
        # TO-DO:
        # cannot parse the selected form
        # return appropriate error page
        raise error
        
    return movie_list


def answer_showtimes_question(question, location):
    """
    Function to answer showtimes-based question
    """

    # We need to get a list of movies currently running in theaters
    current_movies = get_list_currently_running_movies(location)

    concise_movies = [{"name": m['name'], "details": m['extensions'], "id": _id }  for _id, m in enumerate(current_movies)]
    
    prompt = f"""Can you take a look at this list of movies and tell me which of the movies best addresses this question: '{question}' \n
    Answer only with the ids of the movies and separated by newline characters. If none of the movies work, then asnwer with a blank \n""" + str(concise_movies)

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": prompt}]
    )
    movie_ids_raw = completion["choices"][0]["message"]["content"]

    pattern = r'\d+'
    # if not bool(re.fullmatch(pattern, movie_ids_raw)):
    #     raise AttributeError('LLM did not return good ids for the movies')

    matches = re.findall(pattern, movie_ids_raw)
    movie_ids = [int(num.strip()) for num in matches]

    # movie_ids = [int(num) for num in movie_ids_raw.split('\n')]
    pre_showtime_movies = [current_movies[_id] for _id in movie_ids]

    ready_movies = get_showtimes_for_movies(pre_showtime_movies, location)

    return ready_movies


def check_if_showtimes_needed(question):

    prompt = """Can you check whether the question in quotations mentions something to do with theaters\
      or movies in theaters? Answer only 'yes' or 'no' and nothing else.\n""" + question

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": prompt}]
    )

    ans = completion["choices"][0]["message"]["content"]
    
    #reg_ex to parse 'yes' or 'no'
    return bool(re.search(r'yes(?!.*no)', ans.lower()))


def get_list_currently_running_movies(location=("Ann Arbor", "Michigan")):
    # We are searching only for US movies locations for stability of showtimes search
    params = {
    "q": "movie showtimes",
    "location": f"{location[0]}, {location[1]}, United States",
    "hl": "en",
    "gl": "us",
    "api_key": serpapi_apikey
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    print("RESULTS:", results)
    movies = results['knowledge_graph']['movies_playing']
    # short_showtimes = [{"name": m['name'], "details": m['extensions'] }  for m in raw_movies]
    return movies


def get_showtimes_for_movies(movies, location):
    """
    Find showtimes for selected movies
    If cant find showtimes, then returns empty object for that movie
    """

    return_struct = []

    i = 0
    for mov in movies:
        if i > 5: break
        return_struct.append({
            'movie_name': mov['name'],
            'details': mov['extensions'],
            'showtimes': get_one_movie_showtime(mov, location)
        })

        i += 1

    return return_struct


def get_one_movie_showtime(movie, location):
    """
    Functin retrieve just one movie
    Fist char >> string.find('&q=') + 3
    Last char >> string.find('&sa=')
    """

    link_str = movie['link']
    try:
        raw_keywords = link_str[link_str.find('&q=') + 3 :link_str.find('&sa=')]
        raw_keywords = urllib.parse.unquote(raw_keywords)
        keywords = raw_keywords.replace("+", " ")
    except:
        raise AttributeError("Failed to get movie link from current movies!")

    params = {
    "q": keywords,
    "location": f"{location[0]}, {location[1]}, United States",
    "hl": "en",
    "gl": "us",
    "api_key": serpapi_apikey
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    # For simplicity we are doing only the first availible day, either today or tomorrow,
    # whichever day has showtimes
    # We are simplifying UX requirment of seeing the day of the showing, since only 
    # future showtimes are going to be shown and users would deduce which day it is by themselves.
    try:
        raw_showtimes = results['showtimes'][0]['theaters']
        # grabbing standard showings only
        showtimes = [{'name': mov['name'], 'distance': mov['distance'], 'times': mov['showing'][0]['time']} for mov in raw_showtimes]

        # grab only 3 movie theaters for simplicity
        cut_showtimes = showtimes[:3]

    except:
        print (f"ERROR: Bad keywords {keywords} resulted in json without showtimes")
        cut_showtimes = []

    return cut_showtimes



if __name__ == '__main__':
    app.run()