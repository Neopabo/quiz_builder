from pathlib import Path
import json
from random import shuffle

#importing config
with open('configuration.txt', 'r') as file:
    config = json.load(file)

#listing files
docs = [doc for doc in Path(config["User_output"]).iterdir() if doc.is_file()] 

#reading files 
questionaire = []
for doc in docs:
    with open(doc) as file:
        questionaire.extend( json.load(file)['questions'] )

#run quiz
score = 0
count = len(questionaire)
for item in questionaire:
    #load questionaire item
    question = item['question']
    answer_choices = item['answer_choices']
    correct_answer = item['correct_answer']
    
    #set up answer choices
    choices = {}
    shuffle(answer_choices)
    a,b,c,d = choices['a'],choices['b'],choices['c'],choices['d'] = answer_choices
    
    print(f'{question}\n    a. {a}\n    b. {b}\n    c. {c}\n    d. {d}')
    while True:
        chosen_answer = input().lower()
        if chosen_answer in ['a','b','c','d']:
            break
        else:
            print('Invalid input. Try again.')
    if choices[chosen_answer] == correct_answer:
        score += 1
        print('Correct.\n')
    else:
        print(f'Incorrect. The correct answer was [{correct_answer}]\n')
        
print(f'Final score: {score}/{count} - {score/count*100:.0f}%')