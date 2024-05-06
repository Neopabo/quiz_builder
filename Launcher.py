from pathlib import Path
from openai import OpenAI
import json
import os

"""       
# Backlog---
    - Add a way to count tokens prior to sending - context length issue
    - Improve the docs system (measure current_len + next_file_len. If too long, cut the prompts)
    - Add all OpenAI configs to config file for full customization
	- Change temp.txt to logs.txt, save objects as json for each query, instead of a counter
"""

#importing config
with open('configuration.txt', 'r') as file:
    config = json.load(file)


#listing files
docs = [doc for doc in Path(config["User_input"]).iterdir() if doc.is_file()]

#reading files
for doc in docs:
	with open(doc) as file:
		content = file.read()

	#openai api
	client = OpenAI(api_key = config["api_key"])
	completion = client.chat.completions.create(
	  model="gpt-3.5-turbo",
	  response_format={ "type": "json_object" },
	  messages=[
	    {"role": "system", "content": config["sys_proompt"]},
	    {"role": "user", "content": content}
	]
	)
	completion = completion.choices[0].message.content
	
	#temp file read (write_counter)
	if os.path.exists('temp.txt') == False:
		with open('temp.txt', 'w') as file:
			file.write('0')
			write_counter = 0
	else:
		with open('temp.txt', 'r') as file:
			write_counter = int(file.read())
	
	#output write
	output_location = config["User_output"] + '/' + 'Questionaire_' + str(write_counter) + '.txt'
	with open(output_location, 'w') as file:
		file.write(completion)
	
	#update write_counter
	write_counter+=1
	with open('temp.txt', 'w') as file:
		file.write(str(write_counter))
