import requests
from textwrap import fill


class Movie(object):
    ''' Class representing a single movie. Holds criteria pertaining to a queried movie. '''
    def __init__(self, title="", year=int(), director="", cast=list(), plot=""):
        self.title = title
        self.year = year
        self.director = director
        self.cast = cast
        self.plot = plot


    def __str__(self):
        return str("\n-- " + self.title +" --\n"
                   +"Year: " +str(self.year) +"\n"
                   +"Cast: " +str(self.cast) +"\n"
                   +"Director: " +self.director + "\n"
                   +"--Plot--\n" +str(fill(self.plot,width=75)))


class DAO(object):
    ''' Data Access Object for the OMDB site. Retrieves data from the API based on parameters. '''
    def __init__(self):
        self._url = "http://www.omdbapi.com/"
        self._queryType = str
        self._apiKey = self._initKey()
        self._paramDict = {
            'id': 'i',
            'search': 's',
            'getTitle': 't',
            'type': 'type',
            'year': 'y',
            'resType': 'r',
        }


    def _initKey(self):
        return open('./res/apikey.txt', 'r').read()


    def getJsonResponse(self, url):
        ''' :param url - link to a REST api to retrieve a response in JSON format.
            :returns a JSON formatted response of the URL's api request.
        '''
        return requests.get(url).json()


    def generateLink(self, paramVal):
        ''' :returns a link generated with specified parameters and API key to make an API request. '''
        return self._buildQueryLink(
            self._paramDict[paramVal])+str()


    def _buildQueryLink(self, paramVal, query):
        ''' :param - paramValue a corresponding value to the key in _paramDict.
            :param - queryStr - the item to search for
            :returns the URL concatenated with the parameter value.
        '''
        return self._url+'?'+paramVal+'='+query+self._apiKey


    def searchMovieByTitle(self, movieName):
        ''' :param movieName: the name of a movie to search for.
            :returns a list of tuples of search results if found, otherwise None.
        '''
        titleSearch = self._buildQueryLink(self._paramDict['search'], movieName)
        resp = self.getJsonResponse(titleSearch)
        if resp['Response'] == 'True':
            if int(resp['totalResults']) > 1:
                return self.parseMultiResponse(resp)
        else:
            return None


    def getMovieDetails(self, selection):
        ''' :param selection- string representing a movie's title, to retrieve full data of.
            :returns a Movie object of the selected movie.
        '''
        movieQuery = self._buildQueryLink(self._paramDict['getTitle'], selection)
        resp = self.getJsonResponse(movieQuery)
        if resp['Response'] == 'True':
            return self.parseDataToObj(resp)
        else :
            return None


    def parseMultiResponse(self, resp):
        ''':param resp - a json response from a user entered query.
           :returns a list of tuples of the movie's title and release year.
        '''
        return [(result['Title'], result['Year'])
                for result in resp['Search'] if result['Type'] == 'movie']


    def parseDataToObj(self, resp):
        ''' :param resp - a JSON object returned as a response from a movie query.
            :returns a Movie object constructed from the specified movie request.
        '''
        movie = Movie(resp['Title'], resp['Year'], resp['Director'],
                      resp['Actors'], resp['Plot'])
        return movie