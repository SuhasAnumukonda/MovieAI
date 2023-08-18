# MovieAI
MovieAI is a website that allows users to search for movies, then have an AI analyze real reviews of the movie

To use it, download the 5 files and put them into a folder. Within that folder, put movieReviewHTML in a "templates" folder, and put movieReviewCSS and movieReviewJS in a "static" folder.

Before you run any code, make sure that you have all the necessary libraries installed, by entering "pip install (library)" into the terminal as needed

In addition, you need to get API keys from omdbapi.com, and from tmdb. Once you get these, append the urls and authentication headers in the movieReviewJS and movieReviewFlask files as needed. For the OMDB links, simply add your api key to the links. For the TMDB links, go to the API documentation of TMDB to find the proper links and head get requests

After that, open movieReviewML, and run the code to train the model. You should get a test accuracy of around 0.87. You only need to run this file once, because there is a line of code that saves the model to the folder.

From there, you can open movieReviewFlask, and run that file. once you see "Running on http://127.0.0.1:5000" (or something similar) in the terminal, open a browser and run enter "localhost:5000" into the search bar. From there, the website should load. If there is an issue, that most likely means there is an issue with your flask file accessing your JS, CSS and HTML files

Now, search for movies. You will see basic information such as the actors, writers, and plot summary. Furthermore, there will be rating and popularity information. In addition, there will be review information, where the AI that you trained in the movieReviewML file will run analysis on movie reviews, such as sentiment analysis, frequency analysis, and bigram analysis, displaying the data on graphs. Finally, there will be an additional information section, where it will display keywords associated with the movie, and similar movies

Keep in mind, the movie data is from OMDB, and the rating, review, and additional information is from TMDB. For some movies, such as old, unpopular, or international films, there may be limited or even no information. 
