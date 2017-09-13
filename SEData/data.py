# Python Package for Web Scraping and Parsing Stack Exchange Questions

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 14:34:08 2017

@author: benps
"""

import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd

#%%
def populate_question_links(url='https://stackexchange.com/questions?pagesize=50'):
    '''Generates a list of URLs pointing to 'hot questions' on the Stack Exchange network. No non-optional arguments.'''
    r = requests.get(url) # Package the request, send the request and catch the response
    html_doc = r.text # Extracts the response as html
    soup = BeautifulSoup(html_doc, 'lxml') # Create a BeautifulSoup object from the HTML
    
    links = []
    for link in soup.find_all('a'):
        links.append((link.get('href')))

    question_links = [k for k in links if k and 'questions' in k] 

    # Without checking if k is in k, an error is returned.

    pattern = re.compile('questions/\d') # Create pattern to search for

    question_links = filter(pattern.search, question_links) # Filter only links which are questions
    question_links = list(set(question_links)) # Remove duplicates
    
    return(question_links)
#%%
def create_stackexchange_url(category, ID):
    '''Concatenates Stack Exchange category and ID to form Stack Exchange URL'''
    return('https://'+category+'.stackexchange.com/questions/'+str(ID))
    
#%%
def find_highest_id(cat, starting_id=1, max_iter=1000):
    '''Finds highest valid Stack Exchange URL given inputed category and a starting ID. 
        May malfunction in the case of removed questions. Use with caution.'''
    highest_id = starting_id
    limit=0
    while limit < max_iter:
        try: 
            get_text(create_stackexchange_url(category=cat, id=highest_id))
            limit += 1
            highest_id += 1
        except AttributeError:
            return(highest_id-1)
            break

#%%
def fetch_cat_and_id(url):
    '''Returns the question ID and category of an inputed Stack Exchange question URL. Inverse of create_stackexchange_url'''
    url = url.split('/')
    ID = url[4]
    cat = url[2].split('.')[0]
    try:
        int(ID)
    except ValueError:
        print("Unexpected URL input. ID retrieved is not an integer")
    return(ID,cat)

#%%
def get_text(url):
    '''Outputs the text of a question from a Stack Exchange URL. Outputs np.NaN in case of error'''
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'lxml')
    try:
        text =soup.find(attrs={'class':'post-text'}).get_text()
        return(text.replace('\n',''))
    except:
        return(np.NaN)
        
    ### Need add functionality to remove numbers.
    
#%%
def find_cat(url):
    '''Returns just category from stack exchange question url'''
    return(url.split("https://")[1].split(".")[0])
    
    ### Time this to determine if it is fast enough to keep or just redudant given fetch_cat_and_id does the same thing