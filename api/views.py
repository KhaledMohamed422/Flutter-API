from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .models import Profile
from .serializers import ProfileSerializer
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Product, Card, Favorite
from .serializers import ProductSerializer, CardSerializer, FavoriteSerializer
from django.shortcuts import get_object_or_404


# API for authentication 

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

        return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
    else:
        # Check if the username exists but the password is incorrect
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Incorrect password.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'User not found.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Create a profile for the new user
        Profile.objects.create(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Get'])
def logout_view(request):
    logout(request) 
    return Response({'message': 'User logged out successfully.'}, status=status.HTTP_200_OK)

# API for profile user    
  
@api_view(['GET'])
def get_profile(request):
    print(f"*******************User: {request.user}")
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    else:
        return Response({'error': 'User is not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(profile, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Product 

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


@api_view(['GET', 'DELETE'])
def user_card_detail(request, user_id, card_id):
    user = get_object_or_404(User, id=user_id)
    card = get_object_or_404(Card, id=card_id, user=user)
    
    if request.method == 'GET':
        serializer = CardSerializer(card)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        card.delete()
        return Response({'message': 'Card deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'DELETE'])
def user_favorite_detail(request, user_id, favorite_id):
    user = get_object_or_404(User, id=user_id)
    favorite = get_object_or_404(Favorite, id=favorite_id, user=user)
    
    if request.method == 'GET':
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        favorite.delete()
        return Response({'message': 'Favorite deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

