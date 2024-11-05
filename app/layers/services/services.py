# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from ..transport import transport

def getAllImages(input=None)->list:
    
    # obtiene un listado de datos "crudos" desde la API, usando a transport.py.

    json_collection = []

    #for i in range(1,4):
        
    json_collection = json_collection + transport.getAllImages()
    
    # recorre cada dato crudo de la colección anterior, lo convierte en una Card y lo agrega a images.
   
    images = []

    for object in json_collection:

        images.append(translator.fromRequestIntoCard(object))
    
    return images

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    
    fav = translator.fromTemplateIntoCard(request) # transformamos un request del template en una Card.
    
    fav.user = request.user # le asignamos el usuario correspondiente.

    repositories.saveFavourite(fav)

    return fav  # lo guardamos en la base.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = repositories.getAllFavourites(request.user) # buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
        
            mapped_favourites.append(translator.fromRepositoryIntoCard(favourite))  # transformamos cada favorito en una Card, y lo almacenamos en card.

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.