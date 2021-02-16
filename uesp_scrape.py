# -*- coding: utf-8" -*-
"""
Created on Thu Feb  4 23:01:48 2021

@author: pb122

This program serves the purpose of scraping the 
Unofficial Elder Scrolls Pages wiki for item data
to build a sqlite database programatically, instead
of by hand

This program will only fetch the data from eusp, and
will offload it to another python file to save it
to a db and handle SQL work 
"""

#Resource: bs4 documentation, 2019 version

import requests
from bs4 import BeautifulSoup

uesp_links = {
     "weapons": "https://en.uesp.net/wiki/Morrowind:Base_Weapons",
     "clothing": "https://en.uesp.net/wiki/Morrowind:Base_Clothing",
     "lights": "https://en.uesp.net/wiki/Morrowind:Lights",
     "potions": "https://en.uesp.net/wiki/Morrowind:Potions",
     "ingredients": "https://en.uesp.net/wiki/Morrowind:Ingredients",
     "picks": "https://en.uesp.net/wiki/Morrowind:Thieves_Tools"
     }

uesp_table_meta_map = {
        "/wiki/File:OBWeightIcon_small.png": "weight",
        "/wiki/File:OBHealthIcon_small.png": "endurance",
        "/wiki/File:OBValueIcon_small.png":  "value",
        "/wiki/File:OBDamageIcon_small.png": "damage (projectile)"
    }

uesp_table_bulk = {}


def handle_html(url):
    """
    This function will handle a url, and return an html string object,
    or will print an exception in the case of failure
    
    NOTE:
        this code block will read the file containing the url argument 
        as a string if the request is unsuccessful, written to allow me to 
        continue working on code while offline
    
    url: the url of the page 
    
    returns:
        html response in string format, if successful 
    """
    try:
        response = requests.get(url)
        
    except Exception as e:
        #print("Failed to get html from URL, Error:\n")
        #print(e)
        
        #See NOTE: in docstring
        for key in uesp_links:
            if uesp_links[key] == url:
                with open("{}.txt".format(key), "r", encoding = "utf-8") as html:
                    return html.read()
        
    return response.text


def make_soup(html):
    """
    This function will create and return a beautiful soup object
    based on the html provided to it
    """
    soup = BeautifulSoup(html, "html.parser")
    return soup


#Combined usage of handle_html and make_soup
def chef(url):
    """
    This function will combine handle_html and make_soup into 
    a soup kitchen :)
    """
    html = handle_html(url)
    soup = make_soup(html)
    return soup


def offline_work():
    """
    This function iterates through the uesp_links dicitonary of relevant pages 
    and stores them each as a text file, the precursor to the NOTE code block
    in handle_html
    
    Written so I can continue work offline with the html parsing
    
    returns:
        Nothing
        A file generator
    """
    for key in uesp_links:
        index = handle_html(uesp_links[key])
        with open("{}.txt".format(key), "w", encoding = "utf-8") as file:
            file.write(index)


def find_tags(tag, soup):
    """
    This function will essentially take a BeautifulSoup Soup and return a bs 
    iteratable object, with each element being an instance of the tag's 
    occurance 
    
    tag:  a string containing the tag to search for
    soup: the beautiful soup soup within which to search
    
    returns:
        beautifulsoup iteratable containing all tags in the soup
    """
    bs_tag_bulk = soup.find_all(tag)
    
    return bs_tag_bulk
    

def convert_to_name(bs_tag_bulk):
    """
    
    """


def narrow_tags(bs_tag_bulk, search_terms):
    """
    This function will take the iteratable bs object from find_tags
    and filter those tags by whether or not they contain any item in the
    search_terms argument, which is expected as a list 
    
    bs_tag_bulk:  a bs iteratable that includes tags searched for in find_tags
    search_terms: a list of words to check the tags for, and return if yes 
    
    returns:
        refined_tag_bulk: a python object containing tags filtered through 
                          search terms
    """
    refined_tag_bulk = []
    
    for tag in bs_tag_bulk:
        count = 0
        for term in search_terms:
            if term in tag.text:
                count += 1
        if count == len(search_terms):
            refined_tag_bulk.append(tag.text.strip())
                
    #print(len(placeholder))
                
    return refined_tag_bulk


def clean_duplicate_entries(refined_tag_bulk):
    """
    This function is my solution to the problem of data tables being nested
    within a table, so when I search for the tables containing words I want, 
    it also contains a virtually identical parent table filled with some 
    bloat I do not want. The ordering of the tables is such that narrow_tags()
    will always produce an even number with the search terms of "ID" and "Name"
    on the uesp pages, and the first table to be stored is the bloated table,
    so checking if a n entry is in the previous entry, then deleting the 
    previous entry, gets us to the point of having the unwanted duplicates
    removed
    
    refined_tag_bulk: a list of data from pre specified tags extracted from soup
    
    returns:
        refined_tag_bulk: a cleaned list with duplicate+bloat entries removed
    """
    index = 0 
    
    for element in refined_tag_bulk:
        if index < len(refined_tag_bulk):
            if refined_tag_bulk[index] in refined_tag_bulk[index-1]:
                del refined_tag_bulk[index-1]
            index += 1
                
    return refined_tag_bulk


def refine_second_tag_bulk(refined_tag_bulk):
    """
    This function serves the purpose of taking the tables we got out of the 
    previous functions, and sorting them into data structures for later work
    """
    pass


def run_scrape():
    """
    This function brings together the previously written functions in a way
    that allows for the automated data retrieval, parsing, cleansing,
    sorting, formatting, and db-ifying for use
    """
    pass                
    

if __name__ == "__main__":
    """
    Function Flow:
        
    """
    soup = chef(uesp_links["weapons"])
    bs_tag_bulk = find_tags("table", soup)
    
    #This function will get the image links from the pages
    #and convert them to entries in the headers of the data lists
    image_values = convert_to_name(bs_tag_bulk)
    
    refined_tag_bulk = narrow_tags(bs_tag_bulk, ["ID", "Name"])
    refined_tag_bulk = clean_duplicate_entries(refined_tag_bulk)
    
    
    