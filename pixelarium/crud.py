# CRUD functions for pixelarium

import utilities
from model import connect_to_db, db, Image, Tag, ImageTag
from fuzzywuzzy import fuzz, process


def create_image_from_upload(title, link):
    """Create new image record from scratch"""

    new_image = Image(title=title, link=link)
    db.session.add(new_image)
    db.session.commit()


def search_images(input_string):
    """Takes in user input search string and processes it to be passed into subsequent
    search functions"""

    utilities.log_color(input_string)

    # checks for " in search string, indicating user wants exact matches only
    # returns call of exact search function. this happens before calling lower 
    # on input string, because in exact matching, capital letters matter
    if '"' in input_string:
        search_string = input_string.strip('"')
        return search_exact_match(search_string)

    # if no " in string, remove trailing spaces and make it lowercase
    search_string = input_string.lower().strip()

    # keyword search! tags and titles
    # split search string into keyword and terms
    if ":" in search_string:
        search_keyword_list = search_string.split(":")
        
        keyword = search_keyword_list[0]
        utilities.log_color(keyword)

        terms = search_keyword_list[1].strip()
        utilities.log_color(terms)
    
        # if the keyword is tag, use tag search        
        if keyword == "tag":
            search_results = tag_search(terms)
            return search_results
        
        # if the keyword is title, use title search
        elif keyword == "title":
            search_results = title_search(terms)
            return search_results
        
        # if the keyword is blank or something other than tag or title
        # search both. no fuzzy matching
        else:
            tag_results = tag_search(terms)
            title_results = title_search(terms)
            search_results = tag_results | title_results
            return search_results

    # here's fuzzy matching, if no keyword, and not exact string. better for
    # longer search strings. 
    # TODO: later, adjust so fuzzy matching only applies if there's a space in terms
    else:
        tag_results = fuzzy_tag_search(search_string)
        title_results = fuzzy_title_search(search_string)
        search_results = tag_results | title_results
        return search_results
        

def tag_search(input_string):
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
    return set(tag_search_results)
        

def title_search(input_string):
    """Takes in user input search string and returns set of images that match
    works a lot like tag_search"""

    # very similar to tag search, but on a separate table
    search_string = f"%{input_string}%"

    title_search_results = []

    search_image_titles = Image.query.filter(Image.title.like(search_string)).all()

    for image in search_image_titles:
        title_search_results.append(image)

    return set(title_search_results)


def fuzzy_tag_search(input_string):
    """Takes in user input search string and compares against tags. Returns set
    of results"""

    all_tags = []

    # start by getting a list of all the tags for comparison with search string
    for tag in Tag.query.all():
        all_tags.append(tag.text)

    valid_tags = []

    # returns list of tuples containing highest Levenshtein dist values
    compare_input_tags = process.extract(input_string, all_tags, limit=20)

    # if the WRatio values are above a certain threshold (84), add the tag to 
    # the list of valid tags for search results
    # chose 84 because "cat" and "cats" have a WRatio of 86
    for result in compare_input_tags:
        if result[1] >= 85:
            # now we have a list of strings which are tag text values
            valid_tags.append(result[0])

    fuzzy_tag_results = []
    
    # run those values through a query to get the images they're applied to
    for tag_text in valid_tags:
        tag = Tag.query.filter(Tag.text==tag_text).first()
        for image in tag.images:
            fuzzy_tag_results.append(image)
    
    return set(fuzzy_tag_results)


def fuzzy_title_search(input_string):
    """Takes in user input search string and returns set of images as result. 
    Uses fuzzy matching via fuzzywuzzy"""

    # list to hold all image titles
    all_titles = []

    for image in Image.query.all():
        all_titles.append(image.title)
    
    valid_titles = []

    compare_input_titles = process.extract(input_string, all_titles, limit=20)

    for result in compare_input_titles:
        if result[1] >= 85:
            valid_titles.append(result[0])

    fuzzy_title_results = []

    for image_title in valid_titles:
        image = Image.query.filter(Image.title==image_title).first()
        fuzzy_title_results.append(image)

    return set(fuzzy_title_results)


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

    return set(exact_search_results)