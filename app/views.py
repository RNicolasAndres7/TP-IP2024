# capa de vista/presentación

from django.shortcuts import render, redirect
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages 


def index_page(request):
    
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
   
    images = []
    
    images = images + services.getAllImages()

    favourite_list =[]

    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})

def search(request):
   
    search_msg = request.POST.get('query', '') # Leer la doc de esto

    images = []

    images_search=[]
    
    images = images + services.getAllImages()  #( Lista de objetos )

    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if (search_msg != ''):
        
        for object in images: 

            if search_msg in object.name:
                
                images_search.append(object)

        return render(request, 'home.html',{'images': images_search})
    
    else:

        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):

    favourite_list = services.getAllFavourites(request) # llama al servicio para obtener favoritos

    return render(request, 'favourites.html', { 'favourite_list': favourite_list })


@login_required
def saveFavourite(request):
    
    images = services.getAllImages()

    favourite_list = [services.saveFavourite(request)]

    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list}) #llama al servicio para guardar el favorito
    

@login_required
def deleteFavourite(request):
    
    services.deleteFavourite(request) #llama al servicio para eliminar el favorito
    
    
    pass

def login_views(request):
    if request.method=='POST':
        username=request.POST['username'] 
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else: 
            messages.error(request,"USUARIO O CANTRASEÑA INCORRECTA")
    return render (request,'login.html')
    pass

@login_required
def exit(request):
    logout(request)
    return redirect('login')

    pass