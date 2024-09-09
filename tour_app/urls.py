from django.contrib import admin
from django.urls import path, include
from .views import (SignupView, LoginView,DestinationsView,UpdateView,SearchDestinationView,RemoveDestinationView,AddDestinationsView,LogoutView,HomeView
    )
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Root URL for home with login and signup options
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('destinatons/', DestinationsView.as_view(), name='destinations'),
    path('update_details/<int:place_id>/', UpdateView.as_view(), name='update_details'),
    path('search_destination/', SearchDestinationView.as_view(), name='search'),
    path('remove/<int:place_id>/', RemoveDestinationView.as_view(), name='remove'),
    path('add_destination/', AddDestinationsView.as_view(), name='add'),
    path('logout/', LogoutView.as_view(), name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
