# CRUD functions for pixelarium

import utilities
from model import connect_to_db, db, Image, Tag, ImageTag

# def process_search(str):
#     """Takes in user input string and returns search results"""

#     # checks to see if user typed ":" in search string
#     if ":" in str:
#         # if so, splits string into list based on that character
#         search_list = str.split(":")
#         keyword = search_list[0].lower()
    

def search_images(input_string):
    """Takes in user input search string and processes it to be passed into subsequent
    search functions"""

    utilities.print_color(input_string)

    # checks for " in search string, indicating user wants exact matches only
    # returns call of exact search function. this happens before calling lower 
    # on input string, because in exact matching, capital letters matter
    if '"' in input_string:
        search_string = input_string.strip('"')
        return search_exact_match(search_string)

    
    search_string = input_string.lower().strip()

    if ":" in search_string:
        search_keyword_list = search_string.split(":")
        keyword = search_keyword_list[0]
        utilities.print_color(keyword)
        terms = search_keyword_list[1].strip()
        utilities.print_color(terms)
    
        if keyword:
            if keyword == "tag":
                search_results = search_by_tag(terms)
                return search_results
            
            elif keyword == "title":
                search_results = search_by_title(terms)
                return search_results
            
            else:
                tag_results = search_by_tag(terms)
                title_results = search_by_title(terms)
                search_results = tag_results + title_results
                return search_results

    else:
        tag_results = search_by_tag(search_string)
        title_results = search_by_title(search_string)
        search_results = tag_results | title_results
        return search_results
        

def search_by_tag(input_string):
    """Takes in user input search string and compares against tags. Returns set
    of results"""

    # search string if str = "cat" is now "%cat%"
    search_string = f"%{input_string}%"

    tag_search_results = []

    # searching tags for similar strings
    search_tags = Tag.query.filter(Tag.text.like(search_string)).all()

    # search_tags is a list of tag objects, so we iterate through the list
    for tag in search_tags:
        # and get images attribute for each tag (also a list)
        for image in tag.images:   
            # and add them all to one results list
            tag_search_results.append(image)
    
    # eliminates any duplicates for only unique results
    tag_search_results = set(tag_search_results)
    
    return tag_search_results

def search_by_title(input_string):
    """Takes in user input search string and returns set of images that match
    works a lot like search_by_tag"""

    search_string = f"%{input_string}%"

    title_search_results = []

    search_image_titles = Image.query.filter(Image.title.like(search_string)).all()

    for image in search_image_titles:
        title_search_results.append(image)
    
    title_search_results = set(title_search_results)

    return title_search_results

def search_exact_match(input_string):
    """Searches only for exact matches in tags and titles"""

    search_results = []

    exact_tag_matches = Tag.query.filter(Tag.text==input_string).all()

    for tag in exact_tag_matches:
        for image in tag.images:
            search_results.append(image)
    
    exact_title_matches = Image.query.filter(Image.title==input_string).all()

    for image in exact_title_matches:
        search_results.append(image)
    
    exact_search_results = set(search_results)

    return exact_search_results
        


# def search_by_string(str):
#     """Takes in user input search string and returns set of images that match"""

#     # lowercase the user input
#     user_string = str.lower()
#     # empty list to hold images
#     search_results = []
    
#     # searching tags for similar strings
#     search_tags = Tag.query.filter(Tag.text.like(%user_string%)).all()

#     # search_tags is a list of tag objects, so we iterate through the list
#     for tag in search_tags:
#         # and get images attribute for each tag (also a list)
#         for image in tag.images:
#             # check to make sure a given image isn't already in results
#             if image not in search_results:        
#                 # and add them all to one results list
#                 search_results.append(image)

#     search_titles = Image.query.filter(Image.title.like(%str%)).all()
    
#     for image in search_titles:
#         if image not in results:
#             search_results.append(image)
    

#     return search_results



# Returns tags cats and vacation