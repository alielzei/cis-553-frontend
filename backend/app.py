from flask import Flask
from flask import request as recieved_request
import json
import time
# from requests import request
from flask_cors import CORS

import os
import openai
import re


from serpapi import GoogleSearch

with open('backend/api.key', 'r') as file:
    api_key = file.readline().strip()  # Read the first line

openai.api_key = api_key


NOT_RELEVANT = "NOT_RELEVANT"

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/prompt', methods=['POST'])
def prompt():
    recieved_data = recieved_request.json
    question = recieved_data['question']

    resp = dict()

    resp['time'] = time.time()


    # prompt_template = f"""You are going to be asked a question, between two sequences %^& <question goes here> %^& .
    # If the question is not asking about movie suggestions, reply strictly just this: '{NOT_RELEVANT}'.
    # If the question is indeed about movies, then output a list of movies. Attempt to answer the question, responding with a list of movies, most relevant to the question.
    # The list should be formatted as following:
    # >>> movie name > year released > main actors > short description
    # >>> movie name > year released > main actors > short description
    # and so on
    # """


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
        
    resp['movie_suggestions'] = movie_list

    js = json.dumps(resp, indent=4)
    return js, 200


@app.route('/showtimes', methods=['POST'])
def showtimes():
    recieved_data = recieved_request.json
    question = recieved_data['question']

    resp = dict()

    resp['time'] = time.time()

    # filter out non-showtimes question
    if not check_if_showtimes_needed(question):
        return "not showtimes question"
    
    current_movies = get_list_current_showtimes()
    
    

    prompt = "Can you take a look at this list of movies and tell me which of the movies best addresses this question: '{question}' Answer only with the names of the movies and nothing else. If none of the movies work, then asnwer with a blank \n" + str(current_movies)

    # prompt = prompt_template + f"%^& {question} %^& "

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": prompt}]
    )
    #print(completion)
    ans = completion["choices"][0]["message"]["content"]

    movie_suggestions = ans

    # movie_list = list()

    # try:
    #     raw_list = ans.split("<movie_start>")[1:]
    #     for raw_movie in raw_list:
    #         split_raw_mov_tmp = raw_movie.split("<movie_end>")[0]
    #         split_raw_mov = split_raw_mov_tmp.split(" > ")
    #         # TO-DO:
    #         # sptrip spaces and newlines from each elem, just in case
    #         d = {
    #             "name":  split_raw_mov[0],
    #             "year":  split_raw_mov[1],
    #             "actors":  split_raw_mov[2],
    #             "desc":  split_raw_mov[3],
    #         }
    #         movie_list.append(d)
    # except Exception as error:
    #     # TO-DO:
    #     # cannot parse the selected form
    #     # return appropriate error page
    #     raise error
        
    # resp['movie_suggestions'] = movie_list

    # js = json.dumps(resp, indent=4)

    
    return movie_suggestions, 200



def get_list_current_showtimes(location="Ann Arbor, Michigan, United States"):
    params = {
    "q": "movie showtimes",
    "location": location,
    "hl": "en",
    "gl": "us",
    "api_key": "0e7dbfbcc1a20145c678bca44458f6a785f8815510167755a047443d8b3f88e9"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    raw_movies = results['knowledge_graph']['movies_playing']
    short_showtimes = [{"name": m['name'], "details": m['extensions'] }  for m in raw_movies]
    return short_showtimes


# def get_current_showtimes(location="Ann Arbor"):

#     params = {
#     "q": "eternals theater",
#     "location": "Austin, Texas, United States",
#     "hl": "en",
#     "gl": "us",
#     "api_key": "0e7dbfbcc1a20145c678bca44458f6a785f8815510167755a047443d8b3f88e9"
#     }

#     search = GoogleSearch(params)
#     results = search.get_dict()
#     showtimes = results["showtimes"]



def check_if_showtimes_needed(question):

    prompt = "Can you check whether the question in quotations mentions something to do with theaters or movies in theaters? Answer only 'yes' or 'no' and nothing else.\n" + question

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": prompt}]
    )
    #print(completion)
    ans = completion["choices"][0]["message"]["content"]
    
    #reg_ex to parse 'yes' or 'no'
    return bool(re.search(r'yes(?!.*no)', ans.lower()))


@app.route('/test', methods=['GET'])
def test():
    # data = recieved_request.json


    q = "Is there a new crime movie in the theaters?"

    current_movie_list =  get_list_current_showtimes()

    prompt = f"Can you take a look at this list of movies and tell me which of the movies best addresses this question: '{q}' Answer only with the names of the movies and nothing else.\n"+str(current_movie_list)


    # completion = openai.ChatCompletion.create(
    # model="gpt-3.5-turbo", 
    # messages=[{"role": "user", "content": "Tell me about AGI in 5 bullet points"}]
    # )
    # #print(completion)
    # ans = completion["choices"][0]["message"]["content"]

    return resp, 200




if __name__ == '__main__':
    app.run()