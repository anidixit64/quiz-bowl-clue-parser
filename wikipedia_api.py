#!/usr/bin/env python
# coding: utf-8

# In[1]:


import wikipedia
import wikipediaapi
import spacy
import re
from collections import Counter
nlp = spacy.load('en_core_web_md')
user_agent = "QuizBowlPractice/1.0 (ani.aniketdixit_00@yahoo.com)"
wiki_wiki = wikipediaapi.Wikipedia(
    language='en', extract_format= wikipediaapi.ExtractFormat.WIKI, user_agent = user_agent)


# In[2]:


def get_page(term, clues_list):
    page = wiki_wiki.page(term)
    
    if page.exists():
        if 'may refer to:' in page.text:
            link_list = [l.title for l in page.links.values()]
            
            counts = Counter()
            
            for link in link_list:
                link_page = wiki_wiki.page(link)
                link_text = link_page.text.lower()
                
                for c in clues_list:
                    counts[link] += link_text.count(c.lower())
                    
            best_link = max(link_list, key=lambda link: counts[link])
            return wiki_wiki.page(best_link)
        else:
            return page
        
    


# In[3]:


def get_page_clue(clue, main_term):
    page = wiki_wiki.page(clue)
    
    if page.exists():
        if 'may refer to:' in page.text:
            link_list = [l.title for l in page.links.values()]
            
            counts = Counter()
            
            for link in link_list:
                link_page = wiki_wiki.page(link)
                link_text = link_page.text.lower()
    
                counts[link] += link_text.count(main_term.lower())
                    
            best_link = max(link_list, key=lambda link: counts[link])
            return wiki_wiki.page(best_link)
        else:
            return page


# In[4]:


def find_sentences(term, clue_list, clue):

    page_t = get_page(term, clue_list)
    page_c = get_page_clue(clue, term)
    
    matching = []

    page_lower_t = page_t.text
    page_lower_c = page_c.text
    
    Tsentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s", page_lower_t)
    Csentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s", page_lower_c)
    
    for s in Tsentences:
        if clue.lower() in s.lower():
            new_sentence = s.replace(clue, clue.upper())
            matching.append(new_sentence)
        
    for s in Csentences:
        if term.lower() in s.lower():
            new_sentence = s.replace(term, term.upper())
            matching.append(new_sentence)
            
    if matching:
        n = 0
        for m in matching:
            n += 1
            print(f"{n}: {m}" + '\n\n')

