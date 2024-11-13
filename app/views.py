# capa de vista/presentación

from django.shortcuts import render, redirect
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib import messages 
from .layers.persistence import repositories
from app.forms import SubscribeForm
from django.conf import settings


def index_page(request):
    
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
   
    images = []
    
    images = images + services.getAllImages()

    favourite_list = services.getAllFavourites(request)

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
    
    


def login_views(request):
   
    if request.method=='POST':
    
        username=request.POST['username'] 
    
        password=request.POST['password']
    
        user=authenticate(request,username=username,password=password)
    
        if user is not None:
    
            login(request,user)
    
            return redirect(home)
            
    

             #messages.error(request,"USUARIO O CANTRASEÑA INCORRECTA") ## Corregir esto
    
    return render (request,'login.html')


@login_required
def exit(request):
    
    logout(request)
    
    return redirect('login')

def subscribe(request):
    
    form = SubscribeForm()
    
    #if request.method == 'POST':
    
    #    form = SubscribeForm(request.POST)
    
    #    if form.is_valid():
    
    #        subject = 'Code Band'
    
    #        message = 'Sending Email through Gmail'
    
    #        recipient = form.cleaned_data.get('email')
    
    #        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
    
    #        messages.success(request, 'Success!')
    
    #        return redirect(subscribe)
    
    return render(request, 'registration/register.html', {'form': form})