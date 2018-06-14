import pprint
from omdb import Movie

class Model(object):
    ''' Holds data pertaining to responses from queries made to the API'''
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
    ''' Contains prompt outputs for displaying responses for user input. '''
    def promptFavoriteSelect(self, movie):
        print("\nSet \'"+str(movie)+"\' as a favorite? [Y/N]:")


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


    def confirmFavAdded(self, movie):
        print("Added \'"+str(movie)+"\' as a favorite.")


    def viewResponseMenu(self, response):
        print("\n--Search Results--\n")
        print('\n'.join('{:d}: {:s}.'.format(n+1, str(r))
                        for n, r in enumerate(response)))
        print("\nEnter a selection: ")


    def displaySelected(self, movie):
        print(str(movie))


    def displayFavorites(self, favsList):
        print('\n--My Favorites--\n')
        pprint.pprint(favsList)


    def viewMenu(self):
        print("\nEnter choice:"
              +"\n1: Search movie by title"
              +"\n2: View Favorites"
              +"\n3: Exit")


class Controller(object):
    ''' Contains methods for retrieving user input, and control flow based on user inputs'''
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
            self.start()
        elif userIn == 3:
            exit(0)


    def getResponseInput(self, response):
        respIn = input()
        if respIn.isdigit():
            if int(respIn) <= len(response):
                movie = response[int(respIn)-1]
                return movie
        else:
            return None


    def getFavoritesInput(self):
        respIn = str(input()).capitalize()
        if respIn == 'Y':
            return True
        else:
            return False


    def getMovieByTitle(self):
        self._view.promptMovieTitle()
        movieTitle = str(input())
        resp = self._dao.searchMovieByTitle(movieTitle)
        if resp is not None:
            self._view.viewResponseMenu(resp)
            selection = self.getResponseInput(resp)
            if selection is not None:
                self._view.displaySelected(
                    self._dao.getMovieDetails(selection[0])
                )
                self._view.promptFavoriteSelect(selection[0])
                saveFav = self.getFavoritesInput()
                if saveFav:
                    self._model.setFavorite(selection)
                    self._view.confirmFavAdded(selection[0])
            else:
                self._view.alertInvalidResponse()
        else:
            self._view.showErrorMsg()
        self.start()





