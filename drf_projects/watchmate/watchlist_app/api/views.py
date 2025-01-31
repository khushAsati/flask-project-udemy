from rest_framework.response import Response
from rest_framework import status
#from rest_framework.decorators import api_view
from watchlist_app.models import Movie 
from watchlist_app.api.serializers import MovieSerializer
from rest_framework.views import APIView


#CLASS BASED VIEW(APIView)
#  this class for complete list
class MovieListAV(APIView):
    def get(self,request):  #requst:all the data
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies,many=True)
        return Response(serializer.data)
        
      
    def post(self,request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
         
      # this class  for specific item   
class MovieDetailAV(APIView):
    def get(self,request,pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'error':"Movie not found"},status= status.HTTP_404_NOT_FOUND) 
        serializer= MovieSerializer(movie)
        return Response(serializer.data) 
        
    
    def put(self,request,pk):
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie,data=request.data)
        if serializer.is_valid(): # check validation here bcz we get the data from he user
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        
            
    def delete(self,request,pk):
        movie = Movie.objects.get(pk=pk)
        movie.delete()
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
        
        
            
    
        
        