from flask import Flask
from flask import request as recieved_request
import json
import time
# from requests import request

import os
import openai



with open('backend/api.key', 'r') as file:
    api_key = file.readline().strip()  # Read the first line

openai.api_key = api_key


NOT_RELEVANT = "NOT_RELEVANT"

app = Flask(__name__)

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



@app.route('/test', methods=['GET'])
def test():
    # data = recieved_request.json

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": "Tell me about AGI in 5 bullet points"}]
    )
    #print(completion)
    ans = completion["choices"][0]["message"]["content"]

    return ans, 200




if __name__ == '__main__':
    app.run()