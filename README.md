# Pixelarium - an image repo experiment

## [Use Pixelarium here](https://pixelarium.herokuapp.com>)

[https://pixelarium.herokuapp.com/](https://pixelarium.herokuapp.com/)

## Why I made this

I made Pixelarium as part of job application, and also as a way to experiment with fuzzy text string search (via image tags).

## Instructions

- On the Pixelarium home page, you can type in search terms to find pictures. Try searches for tags like "cats", "flower", "landscape".
- Using quotation marks around your search string will search only for exact string matches
- Using either the keyword string "tag" or "title" followed by a colon an then your search will search either only tags or only titles. 
- When you click the search button, you'll be taken to a page showing your results. Images will be displayed above their tags, and each tag is clickable, if you want to look at all images that have that tag.
- The nav menu appears below the content on most pages, but there's a "Search again" link at the top of the search results page, always.
- To upload your own image from your computer, click the "Upload" link in the nav menu.
- On the Upload page, click the "Upload" button to open the upload widget. 
- Optional: If you want to add a tag or title to your image(s), you have to do so before dragging an dropping your image. Click the "Advanced" arrow in the lower-left corner of the Upload widget.
- To add a tag, type the text of your tag, and hit "return". Commas are valid strings in tags, unlike some other image upload services.
- If you'd like to add a title, add it to the "public ID" field above "Add a tag"
- When you're done, drag and drop the picture you'd like to upload in to the widget window. 
- Wait for your upload to complete (progress is shown in the upper-left corner of the window), and click "Done" to finish and close the widget.

Pixelarium lets you upload pictures and perform text searches for the "tag" and "title" fields of each image. It was designed with photos in mind, because I'm an amateur photographer. 

You can also search the library of pictures I've alread uploaded, all of which are pictures I've taken personally.

The home page features a search bar along with some search tips, and a menu to navigate to a couple other pages: Browse shows you all photos, and most pages that show photos also have the tags for each photo listed, which are clickable links that allow you to view all photos that have that particular tag.

## Tags I used (alphetized, comma separated, **bold** for frequently used tags)

2012, 2013, air boat, apollo 11, art, artifacts, ash, b&w, **barcelona**, beach, big water, birds, blue, books, casa batllo, **cats**, chandelier, cherry blossoms, chicago, chickadee, chihuly, city, dandelion, dogs, dongdaemun design plaza, driftwood, dublin, ducks, edit, escalator, facepaint, fall 2005, fall 2008, fall 2011, fall 2012, fall 2017, family, fashion, film, fireworks, flower, **flowers**, gaudi, glass, gondoliers, gyeongbokgung palace, hats, highway, holiday, home, hydrangea, i'm on a boat, iron fence, it's all happening at the zoo, **italy**, ivy, ladder, **landscape**, lavender-cotton, leaves, lenore, libraries, light, lighting, lisa frankenstein, los angeles, lummi island, macro, maine, makeup, mirrors, momo, museum, nasa, **nature**, new orleans, new york, niblings, northern magnolia, nyc, old books, orcas island, outside space, palm trees, **pets**, **plants**, portland, portrait, prisma, sad cat diary, scav, seattle, see you later alligator, **seoul**, **sky**, snakes, snow, south korea, sparrows, spring 2019, summer 2010, summer 2013, summer 2014, summer 2018, summer 2019, **sunset**, swamp, texture, the great indoors, the great outdoors, **travel**, **trees**, trinity library, venice, where you hang your hat, **wildlife**, winter 2013, winter 2014, wooden fence, woodland park zoo, yellow anaconda 

# Installation

To install and run Pixelarium on your local machine:
- Contact me for Cloudinary API keys or create your own [cloudinary](https://cloudinary.com/) account
- Store API keys in secrets.sh as env variables and run secrets.sh
- Install PostgreSQL
- pip install from requirements.txt
- Modify model.py: comment out lines 88 and 91
- Modify model.py: uncomment line 87
- Modify server.py: comment out line 116
- Modify server.py: uncomment line 117
- run server.py to launch server locally

# Under the Hood

## Tech stack

- Flask & Flask-SQLAlchemy
- Python
- JavaScript & jQuery
- PostgresQL
- Jinja
- HTML
- Heroku
- Cloudinary APIs

## Thought processes

My considerations in approaching this project were to think about what interested me about the prompt and focus on that. As an amateur photographer, I primarily use Flickr (in addition to proper cloud backup software) to store and manage my photo library outside of my desktop computer. 

The one search feature that Flickr has always lacked is a duplicate search, which I envision as working a lot like TinEye, which allows the user to feed it an image, and returns a list of other places that image shows up on the web.

I knew that getting to that level of image search would involve a level of familiarity with computer vision that I don't have yet, but I wanted to head in that direction. 

I knew that I could do direct matching of text-based search pretty easily, and it was a core function in my mind, so I started there. That ended up taking my full attention and energy, and I learned a lot in the process!

## Thoughts on technologies and structure

Because I wanted to focus on learning about search, I used a structure that was familiar to me: a Flask server backend which would render HTML and Jinja templates on the front end, and a PostgreSQL database to query against for my searches. Yes, there are some image search APIs out there, but that would have, in my mind, defeated the purpose of learning how to implement search from the ground up. 

I use Cloudinary's Admin API to seed my database with relevant photo data from my cloudinary account. This was in part to avoid running into rate limits on the API, since I'm only calling it each time I either spin up the project or upload a new photo, and in part because I was anticipating wanting to store further data alongside each photo in my db, specifically pertaining to numpy arrays representing colors in each image, and/or color histograms, which I hope to implement in the future.

The db gets seeded by a seed.py file when the app is initially launched. DB is updated on uplaod with new image files information.

Python is my most comfortable programming language, and I've gotten familiar with Flask-SQLAlchemy in another project, so those were obvious choices for me to speed this project along.

This is my first time deploying an app to Heroku, and that was a fun learning experience, as well.

## Upload image

 - Using Cloudinary upload widget
 - Can upload 1 or more images at a time
 - I used the widget rather than upload API because the adding of images wasn't the interesting part for me (that's search).
 - Widget returns an object with data about the photo(s) just uploaded
 - I added a short script to pass that data over to my Flask server
 - Cloudinary's upload leaves a lot to be desired, but using it helped me get to search.

 ## Image search - tags and title

This was my first ever real experience playing with natural language processing, though I've thought about the constraints of search a lot. In a previous job, I worked for a website while the dev team was in the process of adding Elasticsearch to the site, and I did extensive search testing to see if certain features were working as intended.

 - Limited to searching only tags and title field for images. Image relates to Tag via an association table in my db, to handle the many-to-many relationships.
 - Achieved fuzzy matching on search strings through using fuzzywuzzy python library, and setting my WRatio threshold for a valid match at 85 or above. This was based on a specific WRatio match I discovered between two related tag searches while testing.
 - - I plan to tweak my search function in the future so that fuzzy matching only applies to longer, multi-word search strings. This is where it (and the Levenshtein distance it relies on) is most useful. 
 - Exact search matching with use of "" around search string.
 - Keyword search, using tag: or title: in search string.
 - If I were doing this for scale, Elasticsearch would be the obvious choice for my search engine, however, at the current scale, it would be overkill.
 - I did not get around to not-searching (i.e. search for tag "cat" but not tag "vacation"). That's my next feature to tackle on this project, which I intend to continue.

## Future plans

- Beyond the aforementioned tweaks to text based search, I started researching numpy arrays, and how they can be used to represent color channels in an image, in conjunction with OpenCV
- I hope to use this tool to find dominant colors in each image, and allow the user to type in a color name like "blue" or a hexcode, and find images that have a significant amount (I'd have to pick the threshold) of that color in it.
- - Hexcode search would require finding a dataset of color hexcodes, mapped into families/base colors. 
- K-means could also be useful here. 

### To fix

- Push updates to heroku
- Browse all is repeating pictures. Find out why and make it stop!

## To do list

- pytest
- docker
- search by color?

### Tests I need to include

- validate user search strings?
- validate database
- validate route functions