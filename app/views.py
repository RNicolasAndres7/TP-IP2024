# capa de vista/presentación

from django.shortcuts import render, redirect #para que pueda redireccionar la pagina cuando se desloguea o se loguea mal
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout #para que funcione desloguarse
from django.contrib.auth import authenticate, login #agregamos para que funcione autenticarse y loguearse
from django.contrib import messages 
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django.core.paginator import Paginator

def index_page(request):
    
    return render(request, 'index.html')

def members(request):
    
    return render(request, 'members.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    
    contador=1

    images = services.getAllImages()

    images = Paginator(images,20)

    favourite_list = services.getAllFavourites(request)

    return render(request, 'home.html', {'images': images.page(contador), 'favourite_list': favourite_list})

def search(request):
   
    search_msg = request.POST.get('query', '') # Leer la doc de esto

    images = []

    images_search=[]
    
    images = images + services.getAllImages()  #( Lista de objetos )

    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if (search_msg != ''):
        
        search_msg = search_msg[0].upper() + search_msg[1:len(search_msg)]

        if " " in search_msg:

           search_msg = search_msg[0:search_msg.index(" ")+1] + search_msg[search_msg.index(" ")+1].upper() + search_msg[search_msg.index(" ")+2:len(search_msg)]

        for object in images: 

            if search_msg in object.name:
                
                images_search.append(object)

        return render(request, 'home.html',{'images': images_search})
    
    else:

        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
        
    favourite_list = services.getAllFavourites(request)# llama al servicio para obtener favoritos


    return render(request, 'favourites.html', { 'favourite_list': favourite_list })


@login_required
def saveFavourite(request):

    services.saveFavourite(request) #llama al servicio para guardar el favorito
    
    return redirect(home) 
    
    

@login_required
def deleteFavourite(request):
    
    services.deleteFavourite(request) #llama al servicio para eliminar el favorito

    return redirect(getAllFavouritesByUser)
    


def login_views(request):  #funciòn que sirve para autenticarse 
    
    username=request.POST['username'] 
    
    password=request.POST['password']

    user=authenticate(request,username=username,password=password)

    if user is not None: # si las credenciales son validas entonces devuelve el objeto usuario, si no lo son entonces vuelve a la pagina inicial y pide otra vez usuario y contraseña
    
        login(request,user)

    
   

@login_required
def exit(request): #funciòn que sirve para cerrar la sesiòn
    
    logout(request) # remite a la funion de django para desloguearse
    
    return redirect('login') # pedimos como retorno una redireccion a la pagina principal de inicio de sesion
    

def register(request):
    
    form = UserCreationForm(request.POST)

    if request.method == 'POST':

        if form.is_valid():
            
            form.save()

            user_name=request.POST['username']

            user_pwd=request.POST['password1']
    
            user=authenticate(request,username=user_name,password=user_pwd)

            login(request,user)

            return redirect('home')
    
        else:

            messages.error(request,"No se pudo crear usuario, intentelo de nuevo")

            return render(request, 'registration/register.html', {'form': form})
        
    return render(request, 'registration/register.html', {'form': form})

    

    
