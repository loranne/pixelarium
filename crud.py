# CRUD functions for pixelarium
def process_search(str):
    """Takes in user input string and returns search results"""

    # checks to see if user typed ":" in search string
    if ":" in str:
        # if so, splits string into list based on that character
        search_list = str.split(":")
        keyword = search_list[0].lower()
    

def search_images(str):
    """Takes in user input search string and processes it to be passed into subsequent
    search functions"""

    search_string = str.lower()

    if ":" in search_string:
        search_keyword_list = search_string.split(":")
        keyword = search_keyword_list[0]
        terms = search_keyword_list[1]
    
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
        search_results = tag_results + title_results
        return search_results
        

def search_by_tag(str):
    """Takes in user input search string and compares against tags. Returns set
    of results"""

    # search string if str = "cat" is now "%cat%"
    search_string = f"%{str}%"

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

def search_by_title(str):
    """Takes in user input search string and returns set of images that match
    works a lot like search_by_tag"""

    search_string = f"%{str}%"

    title_search_results = []

    search_image_titles = Image.query.filter(Image.title.like(search_string)).all()

    for image in search_image_titles:
        title_search_results.append(image)
    
    title_search_results = set(title_search_results)

    return title_search_results

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