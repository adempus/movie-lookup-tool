from mvc import Model, View, Controller
from omdb import DAO



def main():
    omdbDAO = DAO()
    model = Model()
    view = View()
    controller = Controller(model, view, omdbDAO).start()


main()
