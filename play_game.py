#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re

with open("SMALL_JEOPARDY.json") as f:
    data = json.load(f)

    
def print_cats(data_list):
    """Printing a list of categories available"""
    cats = []
    for dictionary in data_list:
        if dictionary['category'] != None:
            cats.append(dictionary['category'])
    return cats


def get_hint(chosen_dict):
    """Printing a hint for the user if prompted"""
    word_list = re.findall(r'\w+\'?\w+', chosen_dict['answer'])
    len_word_list = len(word_list)

    if len_word_list > 1: # If answer is a sentence, return 1st word only
        return "Here is the first word of the answer: {0}".format(word_list[0])
    else:
        return "Here is the first letter of the answer: {0}".format(chosen_dict['answer'][0])


print("Welcome to My Quiz based on Jeopardy questions!")


def find_ask_question(data_list):
    """Printing available categories, asking question, verifing, printing user score"""
    user_score = None
    hints = 3
    chosen_dict = ""
    data_list = data_list.copy()

    cat_list = print_cats(data_list)
    print("Here is the list of categories to choose from: \n", cat_list)

    while True:
        choice = input("Please press 'i' for category list and choose one: ")
        while choice.upper() not in cat_list:
            if choice == "i":
                print(cat_list)
                choice = input("")
            else:
                choice = input("Invalid category. Please choose your category again. \n ")

        for dictionary in data_list:
            if dictionary['category'] == choice.upper():
                print("Choosing a question from category: {0}".format(choice.lower()))
                chosen_dict = dictionary
                data_list.remove(dictionary)
                break

        if len(chosen_dict) > 1 and chosen_dict != None:
            print("You have one attemp to answer it!\nRemember that you can press 'h' for a hint {0} time(s).".format(hints))
            ask = input(chosen_dict['question'])

            if ask == 'h' or ask == "H":
                if hints > 0:
                    print(get_hint(chosen_dict))
                    hints = hints - 1
                    ask = input("")
                elif hints == 0 or hints < 0:
                    print("You have no more hints left!")
                    ask = input("")

            if ask != chosen_dict['answer']:
                return "You lost!", "The answer was: {0}".format(chosen_dict['answer'])

            elif ask == chosen_dict['answer']:
                score = chosen_dict['value']

                if score != None and user_score is None:
                    user_score = int(score.strip("$").replace(",",""))
                elif score != None and user_score != None:
                    user_score += int(score.strip("$").replace(",","")) # Think to reduce this repetition of the same code!
                else:
                    user_score = 0

                print("Well-done!\nYour won {0} and the total price you won so far is ${1}".format(score, user_score))


print(find_ask_question(data))
