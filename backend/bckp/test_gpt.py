import os
import openai


with open('backend/api.key', 'r') as file:
    api_key = file.readline().strip()  # Read the first line

openai.api_key = api_key

completion = openai.ChatCompletion.create(
model="gpt-3.5-turbo", 
messages=[{"role": "user", "content": "Tell me about AGI in 5 bullet points"}]
)
#print(completion)
ans = completion["choices"][0]["message"]["content"]

print(ans)
