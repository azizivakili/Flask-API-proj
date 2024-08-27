# Flask API sample project 
- WI this project, we will make an API dealing with sentiment analysis. 
- It will then suffice to fill in the sentence whose associated sentiment we want to study by HTTP requests.

The API will be accessible via a pseudo/password system provided by the credentials.csv file. 

From this file, it is visible that the API has two sentiment analysis templates and not all users have access to the same versions.

In addition, the credentials.csv file also shows the templates available to a user because the API will contain two sentiment analysis templates. Let's say a user has v1=1 and v2=0, then that means he has access to the v1 model but not the v2 model.

First, create a /status route that will return 1 if the API is functional. Then add a route greeting the user. Next, make a /permissions route indicating which models a user has access to.

The first version of the model, available with the /v1/sentiment route, should return a random number between -1 and 1, while the /v2/sentiment route should return the compound of a VaderSentiment.SentimentIntensityAnalyzer(). 

Here is a summary of the routes to realize with specificities in the methods to use.

- GET /status: returns 1 if the API is working.
- GET /welcome: returns a greeting message with the username specified by query string.
- POST /permissions: returns a list of permissions for a user authenticated by username and password, add a header to the response including the username, the value taken by v1 and v2.- 
- POST /v1/sentiment: returns the sentiment score by the v1 template of the sentence proposed by the sentience argument sent by POST if the user has identified himself by the pair (username,password). This pair should be transmitted by the following header {Authorization: username=password}, the pair should be encoded but to simplify the exercise, you can leave it as it is.
- POST /v2/sentiment: Same as the previous route, but we want the score returned by the v2 model.

Project inlcludes:
- A python file app.py that contains the API program developed with Flask
- requirements.txt file that represents the minimal (Python) environment that allows to run this API
- A documentation provided as a text or pdf file of your API.
