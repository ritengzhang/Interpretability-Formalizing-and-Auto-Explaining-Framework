import openai
from openai import OpenAI
import pandas as pd
import json
import re
import numpy as np
import os

OPENAI_API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXX' #you have to provided your own openai api key

# Global variable for the model
MODEL = "gpt-4o"
GEN_TEMPERTURE = 0.0




csv_path = './methods/saved method/saved_methods_test.csv'
df_loaded = pd.read_csv(csv_path)

# Convert the DataFrame to JSON
json_data = df_loaded.to_json(orient='records')

# Stringify the JSON data
json_string = json.dumps(json.loads(json_data), indent=4)

print(json_string)




class Chart_Prob_Chat:
    def __init__(self, df_string, model, api_key):
        self.client = openai.OpenAI(api_key=api_key)
        self.df_describtion = "This is a jsonified csv file containing charactersitics of inteprretability methods in deep learning area. :\n"
        self.model = model
        self.df_string = df_string




        self.conversation_history = []

        self.confirm_query = "Are you satisfied with the current method picked? (Y/N): "
        self.intial_assistant_request = "Please describe the method you wish to use, or the goal of your explaination"
        self.assistant_request = "You can provide other information: "
        self.assistant_request = self.intial_assistant_request

        self.first_run = True
        self.log_conversation('system', self.df_describtion+self.df_string)

        self.log_conversation('system', "\nTask description: " + "You are a chat bot that suggestion methods mentioned in the csv to users based on the users' reqeusts. ")
        self.log_conversation('assistant', "\n"+self.intial_assistant_request)

    def log_conversation(self, role, content):
        self.conversation_history.append({'role': role, 'content': content})

    def generate(self, system_request, user_request):
        if system_request:
            self.log_conversation('assistant', system_request)
        if user_request:
            self.log_conversation('user', user_request)

        # Call the AI model to suggest visualization based on the data_json
        response = self.client.chat.completions.create(
            messages=self.conversation_history,
            model=self.model,
            temperature=GEN_TEMPERTURE
        )

        # Get the model's response and log it
        visualization_response = response.choices[0].message.content.strip()
        self.log_conversation('system', visualization_response)
        return visualization_response

    def confirm(self):
        if self.first_run:

          return False
        user_confirm = input(self.confirm_query)
        return user_confirm.upper() == "Y"

    def execute(self):
        while not self.confirm():
            self.first_run = False
            user_request = input(self.assistant_request)
            bot_output = self.generate(system_request=self.assistant_request, user_request=user_request)
            print(bot_output)
            self.assistant_request = self.assistant_request
            print("\n")

    def print_methods_with_probs(self, response):
        print("xxxxxxx")
        print(response)
        for func, prob in response.items():
            if prob > 0.1:
                print(f"Function: {func}, Probability: {prob}")

    def print_conversation(self):
        for entry in self.conversation_history:
            print(f"{entry['role'].capitalize()}: {entry['content']}")





assistant = Chart_Prob_Chat(df_string=json_string, model=MODEL, api_key=OPENAI_API_KEY)
assistant.execute()
print("\n\n\nConversation Log:")
assistant.print_conversation()