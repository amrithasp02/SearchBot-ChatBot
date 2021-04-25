#!/usr/bin/env python
# coding: utf-8

# In[5]:


import sys
get_ipython().system('{sys.executable} -m pip install pyowm')


# In[6]:


#from newspaper import Article
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import numpy as np
import warnings
import wikipedia
import requests
import pyowm

from nltk.chat.util import Chat, reflections


# In[7]:


#Ignore warnings
warnings.filterwarnings('ignore')


# In[8]:


#Download packages from nltk
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)


# In[9]:


sent_tokens = []
def get_wiki(query):
    global sent_tokens
    title = wikipedia.search(query)[0]
    page = wikipedia.page(title)
    corpus = page.content
    text = corpus
    sent_tokens = nltk.sent_tokenize(text)
    return page.content
#Print the corpus/text
#print(corpus)


# In[10]:


#to get live weather report
def weather(c):
    owm = pyowm.OWM('1d1697581060812661ab226e74410ae0')
    # observation = owm.weather_at_place('Bangalore, India')
    observation = owm.weather_at_place(c)
    w = observation.get_weather()
    t = w.get_temperature('celsius')
    return str(t['temp'])


# In[11]:


#Create a dictionary to remove punctuations
remove_punct_dict = dict( ( ord(punct),None) for punct in string.punctuation)
#print(string.punctuation)
#print(remove_punct_dict)


# In[12]:


def LemNormalize(text):
    return nltk.word_tokenize(text.lower().translate(remove_punct_dict))

#Print the tokenization text
#print(LemNormalize(text))


# In[13]:


#Keyword matching

#Greeting Inputs
GREETING_INPUTS = ["hi", "hello", "greetings", "wassup", "howdy", "hey", "hola"]

#Greeting responses
GREETING_RESPONSES = ["hi", "greetings", "hello", "hey", "what's good?", "hey there"]

#Return a random response to the user's greeting
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# In[14]:


#Generate the response
def response(user_response):

    global sent_tokens
    #user response/query
    #user_response = "What is chronic kidney disease?"
    user_response = user_response.lower()
    #print(user_response)

    #set the chatbot response to an empty string
    robo_response = ""

    #append the user response to the sentence list
    sent_tokens.append(user_response)
    #print(sent_tokens)

    #create a TfidfVectorizer object
    TfidfVec = TfidfVectorizer(tokenizer = LemNormalize, stop_words='english')

    #convert the text to a matrix of tf-idf features
    tfidf = TfidfVec.fit_transform(sent_tokens)
    #print(tfidf)

    #get the measure of similarity (similarity scores)
    vals = cosine_similarity(tfidf[-1], tfidf)
    #print(vals)

    #get the index of the most similar sentence/text to the user response
    idx = vals.argsort()[0][-2]

    #reduce the dimensionality of vals which is a list of lists
    flat = vals.flatten()
    flat.sort() #ascending order

    #Get the most similar score to the users response
    score = flat[-2]
    #print(score)

    #if the variable 'score' is 0, then there is no text similar to the user's response
    if score == 0:
        robo_response = robo_response+"I apologise, I don't understand."
    else:
        robo_response = robo_response+sent_tokens[idx]
    
    #remove the user's response from the sentence tokens list
    sent_tokens.remove(user_response)
    
    return robo_response


# In[19]:


flag = True
def start_bot():
    global flag
    print("Hi, I'm Luna. Ask me something to begin a conversation. I will answer your questions regarding absolutely anything! Type 'Search: ', and continue with your topic. Type \"quit\" to leave this chat.")
    
    while flag == True:
        user_response = input()
        user_response = user_response.lower()
        if 'search' in user_response:
            lst = user_response.split()
            lst.remove('search:')
            st = ""
            for i in lst:
                st += i
            wiki_text = get_wiki(st)
            continue
        if user_response != 'quit':
            chat = Chat(pairs, reflections)
            r = chat.converse()
            if r == 'None':
                try:
                    res = response(user_response)
                except:
                    print("Oops! I didn't quite get you there.")
                    continue
                print(res) 
            else:
                print(r)
        else:
            flag = False
            print("Chat with you later!")
        


# In[ ]:






pairs = [
            [
                r"my name is (.*)|i am (.*)",
                ["Hello %1, How are you today?", ]
            ],
            [
                r"what is your name?",
                ["My name is Luna and I'm a chatbot.", ]
            ],
            [
                r"how are you?|how about you?",
                ["I'm doing good\nHow about You ?", ]
            ],
            [
                r"sorry| sorry (.*)",
                ["Its alright", "Its OK, never mind", ]
            ],
            [
                r"(.*)(fine|good)",
                ["Nice to hear that", "Alright :)", ]
            ],
            [
                r"hi|hey|hello|howdy|hey there",
                ["Hello", "Hey there", ]
            ],
            [
                r"(.*)age?| (.*)old (.*)?",
                ["I'm a computer program \nSeriously you are asking me this?", ]

            ],
            [
                r"(.*)(created|made)(.*)?",
                ["Sanjivani created me using Python's NLTK library ", "top secret ;)", ]
            ],
            [
                r"(.*)(location|city) ?",
                ['Bangalore, Karnataka', ]
            ],
            [
                r"(.*)weather?",
                ["The current temperature in Bangalore, India is 31 degrees Celsius.", ]
            ],
            [
                r"how (.*) health(.*)",
                ["I'm a computer program, so I'm always healthy ", ]
            ],
            [
                r"(.*) (sport|game) ?",
                ["I'm not a very sporty person", ]
            ],
            [
                r"who (.*) (moviestar|actor)?",
                ["I like all of them"]
            ],
            [
                r"(.*) food?",
                ["I love computer chips :)", ]
            ],
            [
                r"where are you?", 
                ["Right here", ]
            ],
            [
                r"do you want (.*)?",
                ["I have everything i need in my cloud", ]
            ],
            [ 
                r"why do you like (.*)?",
                ["Just because.",]
            ],
            [
                r"(.*) favourite (.*)?",
                ["Computers don't have a say in that"]
            ],
            [
                r"quit",
                ["Bye, take care. See you soon :) ", "It was nice talking to you. See you soon :)"]
            ]
]




if __name__ == "__main__":
    start_bot()


# In[ ]:




