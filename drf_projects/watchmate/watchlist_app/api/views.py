from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from watchlist_app.api.permissions import AdminOrReadOnly
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from watchlist_app.api.throtling import ReviewCreateThrottle, ReviewListThrottle


#from rest_framework.decorators import api_view
from rest_framework import viewsets
from watchlist_app.models import WatchList,StreamPlatform,Review
from watchlist_app.api.serializers import (WatchListSerializer,StreamPlatformSerializer,
                                           ReviewSerializer)


class CustomLoginView(APIView):
    permission_classes = []  # Allow any user to access this endpoint

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            })
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)


class CustomRegisterView(APIView):
    permission_classes = []  # Allow any user to access this endpoint

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return Response({
                'error': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create new user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        # Create token for the user
        token = Token.objects.create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'message': 'Registration successful'
        }, status=status.HTTP_201_CREATED)
        
        
        
class UserReview(generics.ListAPIView):
     # queryset = Review.objects.all() (overriding this)
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    
    # def get_queryset(self):
    #     username = self.kwargs['username']#accessing primary key
    #     return Review.objects.filter(userreview__username = username)#filter review according id of watchlist
    
    def get_queryset(self):
         username = self.request.query_params.get('username')#accessing primary key
         return Review.objects.filter(userreview__username = username)#filter review according id of watchlist
      
 


class ReviewCreate(generics.CreateAPIView):
    # here something is overrided
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewCreateThrottle]
    


    def get_queryset(self):
        return Review.objects.all()
    
        
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk= pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist = watchlist, userreview = review_user)
        if review_queryset.exists():
            raise ValidationError("u have already review this watch")
        
        
        if watchlist.avg_number == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
            watchlist.avg_number = 1
        else:
            watchlist.avg_rating = (watchlist.avg_rating * watchlist.avg_number + serializer.validated_data['rating']) / (watchlist.avg_number + 1)
            watchlist.avg_number = watchlist.avg_number + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, userreview=review_user)


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all() (overriding this)
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    
    def get_queryset(self):
        pk = self.kwargs['pk']#accessing primary key
        return Review.objects.filter(watchlist =pk)#filter review according id of watchlist
    
        


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AdminOrReadOnly]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
        




#CLASS BASED VIEW(APIView)
#  this class for complete list
# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
    
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)
    
    


# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class =  ReviewSerializer
 
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
    
    
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
    
    
    
class WatchListAV(APIView):
    def get(self,request):  #requst:all the data
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies,many=True,context={'request': request})
        return Response(serializer.data)
        
      
    def post(self,request):
        serializer = WatchListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
         
      # this class  for specific item   
class WatchDetailAV(APIView):
    def get (self,request,pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except movie.DoesNotExist:
            return Response({'error':"Movie not found"},status= status.HTTP_404_NOT_FOUND) 
        serializer= WatchListSerializer(movie, context={'request': request})
        return Response(serializer.data) 
        
    
    def put(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie,data=request.data,context={'request': request})
        if serializer.is_valid(): # check validation here bcz we get the data from he user
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        
            
    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
    


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
 
# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self,request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset,many = True, context={'request': request})
#         return Response(serializer.data)    
    
#     def retrieve(self,request,pk=None):  
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist, context={'request': request})
#         return Response(serializer.data)
    
#     def create(self,request):
#         serializer = StreamPlatformSerializer(data=request.data,context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
    
    #🧠 Simple Analogy

# 👉 request = courier ka poora box 📦
# 👉 request.data = box ke andar ka samaan 🎁
# 🔹 Important Difference
# Concept	Meaning
# request.data	client se aaya hua input
# serializer.data	client ko bhejne wala output
    
        
        

class StreamPlatformAV(APIView):
    def get(self,request):
        print("im here")
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform,many=True,context={'request': request})
        return Response(serializer.data)
        
    def post(self,request): # accepath('stream/',StreamPlatformAV.as_view(),name='stream'),ss data through request then passed the data to serializer
        serializer = StreamPlatformSerializer(data = request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    
        
class StreamPlatformDetailAV(APIView):
    def get(self,request,pk):
        print("im here 73")
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error':'not Found'},status= status.HTTP_404_NOT_FOUND)
            
        serializer = StreamPlatformSerializer(platform, context={'request': request})
        return Response(serializer.data)
         
    
    def put(self,request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform,data= request.data, context={'request': request})# this is for single data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    
    def delete(self,request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
        
        
    
    
    
    

#FUNCTION BASED VIEW
# @api_view(['GET', 'POST']) # by default it will take get request 
# def movie_list(request):
#     if request.method == 'GET':
#         try:
            
#             movies = Movie.objects.all() # complex data
#             serializer = MovieSerializer(movies,many= True)# becz there are multiple objects
#             return Response(serializer.data,status=200)# .data means all the information
#         except Exception:
#             print("not found")
#             return Response("nahi h data",status=404)
        
#     #in 'GET'-we are sending the information to the user
#     #in 'POST'- user sending some data to store in  my database
#     if request.method == 'POST':
#         serializer= MovieSerializer(data=request.data)# data recieve from user and data converted into json  using serializer
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=201)
#         else:
#             return Response(serializer.errors,status=400)     
            
          
    
# @api_view(['GET','PUT','DELETE'])   
# def movie_details(request,pk):# for single record
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk =pk)
#             serializer = MovieSerializer(movie)# no need many= true becz of single object fetching
#             return Response(serializer.data)
              
#         except Movie.DoesNotExist:
#             print("not found")
#             return Response({"ERROR":'MOVIE NOT FOUND'},status=status.HTTP_404_NOT_FOUND)
        
    
#     if request.method == 'PUT':# recieve data (updated)data from user
#         movie= Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie,data= request.data)# here send the data and we serialized the data
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                
            
#     if request.method == 'DELETE':
#         try:
#             movie = Movie.objects.get(pk=pk)
#             movie.delete()
#             return Response(status = status.HTTP_204_NO_CONTENT)
#         except Exception as o:
#             print("this is exception",o.__getattribute__)
#             return Response("bhaiya j ye id nahi h mere pass")
        
        
            
    
        
        