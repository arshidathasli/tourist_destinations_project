from rest_framework import generics
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from .forms import LoginForm  # Your login form
from django.views import View
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from tour_app.models import Tour
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User  # or your custom User model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddDestinationForm 
from .forms import LogoutForm  # Create a simple form for the logout action
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .forms import TourUpdateForm  # Create this form based on your serializer
from .serializers import SignupSerializer,LoginSerializer,TourSerializer,TourUpdateSerializer,AddDestinationSerializer,LogoutSerializer

class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SignupView(TemplateView):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        # Render the signup form
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Handle form submission
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"email: {email}, password: {password}")

        # Create a new user
        if email and password:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered')
                return redirect('signup')
            
            user = User.objects.create_user(username=email, email=email, password=password)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)  # Log the user in after signup
            messages.success(request, 'Signup successful! You are now logged in.')
            return redirect(reverse_lazy('login'))  # Redirect to another page after signup
        
        messages.error(request, 'Invalid signup details')
        return render(request, self.template_name)



class LoginView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(f"email: {email}, pass: {password}")

            user = authenticate(request, email=email, password=password)
            print(f"User: {user}")
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('destinations')  # Redirect to the URL name that renders `destination.html`
            else:
                messages.error(request, 'Invalid email or password')
                return redirect('home')  # Redirect to the home page if login fails
            
        return render(request, self.template_name, {'form': form})
    


class DestinationsView(View):
    template_name = 'destination.html'

    def get(self, request, *args, **kwargs):
        tours = Tour.objects.all()  # Fetch all tour objects
        return render(request, self.template_name, {'tours': tours})
  


class UpdateView(UpdateView):
    model = Tour
    form_class = TourUpdateForm
    template_name = 'update.html'
    pk_url_kwarg = 'place_id'  # Ensure this matches the URL parameter name in your path

    def form_valid(self, form):
        # Save the updated instance
        form.save()
        # Redirect to a success page or back to the list of destinations
        return redirect(reverse_lazy('destinations'))  # Adjust this URL name as needed

    def form_invalid(self, form):
        # Render the form with errors if the data is not valid
        return render(self.request, self.template_name, {'form': form}) 


from django.views.generic import ListView
from django.db.models import Q
from .models import Tour

class SearchDestinationView(ListView):
    model = Tour
    template_name = 'search.html'
    context_object_name = 'tours'
    
    def get_queryset(self):
        query = self.request.GET.get('q')  # Retrieve search query from the request
        if query:
            return Tour.objects.filter(
                Q(place_name__icontains=query) |
                Q(weather__icontains=query) |
                Q(location_state__icontains=query) |
                Q(location_district__icontains=query) |
                Q(description__icontains=query)
            )
        else:
            return Tour.objects.all()  # Return all objects if no query is provided



class RemoveDestinationView(LoginRequiredMixin, View):
    template_name = 'remove.html'
    
    def get(self, request, *args, **kwargs):
        place_id = self.kwargs.get('place_id')
        destination = get_object_or_404(Tour, id=place_id)
        return render(request, self.template_name, {'destination': destination})

    def post(self, request, *args, **kwargs):
        place_id = self.kwargs.get('place_id')
        destination = get_object_or_404(Tour, id=place_id)
        destination.delete()
        messages.success(request, 'Destination deleted successfully')
        return redirect(reverse_lazy('destinations'))  

class AddDestinationsView(LoginRequiredMixin, View):
    template_name = 'add.html'
    
    def get(self, request, *args, **kwargs):
        form = AddDestinationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = AddDestinationForm(request.POST, request.FILES)  # Include request.FILES for image uploads
        if form.is_valid():
            form.save()
            messages.success(request, 'Destination added successfully')
            return redirect('destinations')  # Redirect to the list of destinations or another relevant page
        else:
            messages.error(request, 'There was an error adding the destination. Please try again.')
        return render(request, self.template_name, {'form': form})



class LogoutView(LoginRequiredMixin, View):
    template_name = 'logout.html'

    def get(self, request, *args, **kwargs):
        form = LogoutForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LogoutForm(request.POST)
        try:
            messages.success(request, "Successfully logged out")
            return redirect('login')  # Redirect to the login page or home page
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

        return render(request, self.template_name, {'form': form})