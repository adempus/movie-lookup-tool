import pprint
from omdb import Movie

class Model(object):
    def __init__(self):
        self._favList = list()  # stores a list of movies
        self._movieData = Movie()


    def setFavorite(self, fav):
        self._favList.append(fav)


    def setMovieResult(self, movie):
        self._movieData = movie


    def getMovieResult(self):
        return self._movieData


    def getFavorites(self):
        return self._favList


class View(object):
    def promptFavoriteSelect(self, movie):
        print("Set movie: "+str(movie)+" as favorite? [Y/N]")


    def promptMovieTitle(self):
        print("Enter the name of a movie: ")


    def displayInputError(self):
        print("Incorrect input provided")


    def alertInvalidResponse(self):
        print("Invalid response provided. ")

    def showResponse(self, response):
        pprint.pprint(response)


    def showErrorMsg(self):
        print("Error: Movie not found!")


    def showFavConfirmation(self, movie):
        print("Added "+str(movie)+" as a favorite.")


    def viewResponseMenu(self, response):
        print("\n--Search Results--\n")
        print('\n'.join('{:d}: {:s}.'.format(n+1, str(r))
                        for n, r in enumerate(response)))
        print("\nEnter a selection: ")


    def displaySelected(self, movie):
        print(str(movie))


    def displayFavorites(self, favsList):
        print(favsList)


    def viewMenu(self):
        print("\nEnter choice:"
              +"\n1: Search movie by title"
              +"\n2: View Favorites"
              +"\n3: Exit")


class Controller(object):
    def __init__(self, model, view, dao):
        self._model = model
        self._view = view
        self._dao = dao


    def start(self):
        self._view.viewMenu()
        userIn = int(input())
        while userIn > 3 or userIn < 1:
            self._view.dispalyInputError()
        if userIn == 1:
            self.getMovieByTitle()
        elif userIn == 2:
            self._view.displayFavorites(self._model.getFavorites())
        elif userIn == 3:
            exit(0)


    def setFavoriteSelection(self, response):
        ''' :param response - a tuple'd list response from a query. '''
        selection = int(input())
        movie = self._model.getPostQueryResponse()[selection-1]
        self._view.promptFavoriteSelect(movie)
        userIn = str(input()).capitalize()
        if userIn == 'Y':
            self._model.setFavorite(movie)
            self._view.showFavConfirmation(movie)
        if userIn == 'N':
            self._view.viewMenu()


    def getResponseInput(self, response):
        respIn = input()
        if respIn.isdigit():
            if int(respIn) <= len(response):
                movie = response[int(respIn)-1]
                return movie
        else:
            return None


    def getMovieByTitle(self):
        self._view.promptMovieTitle()
        movieTitle = str(input())
        resp = self._dao.searchMovieByTitle(movieTitle)
        if resp is not None:
            self._view.viewResponseMenu(resp)
            selection = self.getResponseInput(resp)
            if selection is not None:
                movie = self._dao.getMovieDetails(selection[0])
                self._view.displaySelected(movie)
            else:
                self._view.alertInvalidResponse()
        else:
            self._view.showErrorMsg()
        #self.setFavoriteSelection(resp)
        self.start()





