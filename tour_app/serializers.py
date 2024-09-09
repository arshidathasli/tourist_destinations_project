from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from tour_app.models import Tour
from rest_framework_simplejwt.authentication import JWTAuthentication




User = get_user_model()  # Use get_user_model() for custom user models


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'password')
    
    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create_user(email=email, password=password)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError("Both email and password are required.")
        
        data['user'] = user
        return data

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ('place_name', 'weather', 'location_state', 'location_district', 'google_map_link', 'image', 'description')


class TourUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ('place_name', 'weather', 'location_state', 'location_district', 'google_map_link', 'image', 'description')

    def update(self, instance, validated_data):
        instance.place_name = validated_data.get('place_name', instance.place_name)
        instance.weather = validated_data.get('weather', instance.weather)
        instance.location_state = validated_data.get('location_state', instance.location_state)
        instance.location_district = validated_data.get('location_district', instance.location_district)
        instance.google_map_link = validated_data.get('google_map_link', instance.google_map_link)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    

class AddDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ['place_name', 'weather', 'location_state', 'location_district', 'google_map_link', 'image', 'description']    

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs        
