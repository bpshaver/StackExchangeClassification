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
def get_text(url, rm_digits = True, rm_punct = True):
    '''Outputs the text of a question from a Stack Exchange URL. Outputs np.NaN in case of error'''
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'lxml')
    
    digit_list = "1234567890"
    punct_list = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    try:
        text = soup.find(attrs={'class':'post-text'}).get_text()
        text = text.replace('\n',' ')
        if rm_punct  == True:
                for char in punct_list:
                    text = text.replace(char, "")
        if rm_digits == True:
                for char in digit_list:
                    text = text.replace(char, "")
        return(text)
    except:
        return(np.NaN)
        
    ### Need add functionality to remove numbers.
    
#%%
def find_cat(url):
    '''Returns just category from stack exchange question url'''
    return(url.split("https://")[1].split(".")[0])
    
    ### Time this to determine if it is fast enough to keep or just redudant given fetch_cat_and_id does the same thing
#%%
sample_question_links = ['https://raspberrypi.stackexchange.com/questions/72438/how-to-use-spi-on-raspberry-pi-3',
 'https://worldbuilding.stackexchange.com/questions/91909/why-colonise-planets',
 'https://networkengineering.stackexchange.com/questions/44121/where-can-i-use-the-ipv6-documentation-prefix',
 'https://ux.stackexchange.com/questions/111704/should-i-add-a-redundant-cancel-option',
 'https://cooking.stackexchange.com/questions/84310/why-would-boiling-milk-in-an-electric-kettle-break-the-kettle',
 'https://math.stackexchange.com/questions/2428015/prove-that-at-a-party-of-25-people-there-is-one-person-knows-at-least-twelve-peo',
 'https://gamedev.stackexchange.com/questions/148354/why-is-account-sharing-so-bad',
 'https://academia.stackexchange.com/questions/95860/mathematics-stack-exchange-as-an-indicator-for-academic-career',
 'https://politics.stackexchange.com/questions/24512/why-are-weapon-restriction-laws-considered-liberal',
 'https://math.stackexchange.com/questions/2427404/is-there-a-bijection-between-the-reals-and-naturals',
 'https://rpg.stackexchange.com/questions/106735/except-for-pc-rogues-who-else-knows-thieves-cant',
 'https://interpersonal.stackexchange.com/questions/3807/how-to-react-to-someone-pushing-me-in-public-transport',
 'https://security.stackexchange.com/questions/169320/any-reason-to-slow-hash-passwords-generated-randomly-by-our-site',
 'https://academia.stackexchange.com/questions/95890/if-you-have-severe-problems-with-speaking-is-it-okay-to-use-more-text-and-equat',
 'https://unix.stackexchange.com/questions/391987/how-can-i-use-wildcards-with-ls-to-find-files-that-are-missing-in-a-numeric-sequ',
 'https://scifi.stackexchange.com/questions/169561/why-is-jaqen-wearing-aryas-face',
 'https://skeptics.stackexchange.com/questions/39437/did-yuri-gagarin-end-up-in-critical-condition-after-coming-back-to-earth-due-to',
 'https://unix.stackexchange.com/questions/392001/how-do-i-secure-linux-systems-against-the-blueborne-remote-attack',
 'https://movies.stackexchange.com/questions/80276/why-were-sloths-chosen-to-depict-dmv-workers',
 'https://rpg.stackexchange.com/questions/106744/what-does-a-simulacrum-know',
 'https://math.stackexchange.com/questions/2428099/a-strange-exponential-inequality',
 'https://scifi.stackexchange.com/questions/169515/is-anyone-else-not-buying-the-buggers-story',
 'https://politics.stackexchange.com/questions/24555/why-is-privacy-a-subject-felt-more-in-europe-rather-than-the-us',
 'https://worldbuilding.stackexchange.com/questions/91717/how-would-it-make-sense-that-spellbooks-or-grimoires-teach-only-one-spell',
 'https://superuser.com/questions/1249251/how-can-i-intentionally-break-corrupt-a-sector-on-an-sd-card',
 'https://worldbuilding.stackexchange.com/questions/91869/with-some-exceptions-what-makes-me-the-most-powerful-mage-on-the-planet-not-j',
 'https://sqa.stackexchange.com/questions/29500/who-is-responsible-for-pinpointing-bugs',
 'https://workplace.stackexchange.com/questions/98818/is-it-common-business-practice-to-consider-constructive-break-times-as-billable',
 'https://mechanics.stackexchange.com/questions/47887/small-amount-of-wrong-fuel-type-put-in-the-tank',
 'https://workplace.stackexchange.com/questions/98738/asking-for-help-in-it-in-a-senior-position-while-keeping-credibility',
 'https://worldbuilding.stackexchange.com/questions/91897/why-might-it-be-desirable-to-engineer-aquatic-humans',
 'https://unix.stackexchange.com/questions/392035/can-i-use-sed-to-translate-characters-like-with-tr',
 'https://physics.stackexchange.com/questions/356998/how-fast-does-haumea-rotate',
 'https://judaism.stackexchange.com/questions/85490/why-would-a-jewish-woman-marry-through-a-religious-ceremony-knowing-she-risk-be',
 'https://interpersonal.stackexchange.com/questions/3833/how-to-politely-receive-someone-when-you-dont-know-how-to-pronounce-their-name',
 'https://diy.stackexchange.com/questions/123285/kitchen-wiring-14-to-12-neutral',
 'https://interpersonal.stackexchange.com/questions/3812/how-can-i-better-control-my-desire-or-need-to-send-long-messages',
 'https://interpersonal.stackexchange.com/questions/3762/i-sent-an-interesting-link-to-a-friend-that-he-didnt-ask-for-at-all-and-he-rep',
 'https://biology.stackexchange.com/questions/65816/which-red-bug-is-this',
 'https://workplace.stackexchange.com/questions/98824/is-it-appropriate-for-a-recruiter-to-tell-me-i-need-to-be-able-to-take-calls-dur',
 'https://stackoverflow.com/questions/46198648/usage-of-void-in-a-comma-separated-list',
 'https://electronics.stackexchange.com/questions/329138/piezoelectric-effect-in-cables',
 'https://english.stackexchange.com/questions/409677/how-popular-is-the-slang-usage-of-toss-in-british-english',
 'https://math.stackexchange.com/questions/2428163/prove-that-the-golden-ratio-is-irrational-by-contradiction',
 'https://mathematica.stackexchange.com/questions/155651/prepending-a-constant-value-to-sublists-of-a-list',
 'https://astronomy.stackexchange.com/questions/22651/does-the-milky-way-move-through-space',
 'https://skeptics.stackexchange.com/questions/39414/did-karl-marx-write-that-slavery-had-good-sides-and-abolishing-it-would-indirect',
 'https://money.stackexchange.com/questions/84975/why-is-auto-insurance-ridiculously-overpriced-for-those-who-drive-few-miles',
 'https://worldbuilding.stackexchange.com/questions/91888/what-kind-of-food-would-be-common-in-a-culture-that-tries-to-avoid-fire-as-much',
 'https://mathoverflow.net/questions/281043/feit-thompson-conjecture']
