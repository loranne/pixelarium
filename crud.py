# CRUD functions for pixelarium
def process_search(str):
    """Takes in user input string and returns search results"""

    # checks to see if user typed ":" in search string
    if ":" in str:
        # if so, splits string into list based on that character
        search_list = str.split(":")
        keyword = search_list[0].lower()
    
    else:
        results = Image.query.filter(Image.tags.like("%str%"), Image.title.like("%str%")).all()


# searching tags for similar strings
results = []
search_tags = Tag.query.filter(Tag.text.like("%cat%")).all()

for tag in search_tags:
    # result of this is a list
    # tagged_images = tag.images
    # so we iterate through that list to get each object
    for image in tag.images:
        if image not in results:        
            # and add them all to one results list
            results.append(image)

search_titles = Image.query.filter(Image.title.like(%str%)).all()





# Returns tags cats and vacation