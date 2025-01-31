from rest_framework import serializers

from watchlist_app.models import Movie

# 2) Modelserializer
class MovieSerializer(serializers.ModelSerializer):
    
    #custom serializerfield(calculating some python3 managcustom field)
    # create specific method
    len_name = serializers.SerializerMethodField()#field 
     #len_name(variable_name)
    class Meta:
        model = Movie
        fields = "__all__"
        #exclude = ['name'] # if we dont want to include one field we can exclude that
        
    def get_len_name(self,object):#object has access to id,name ,desc
        length = len(object.name)
        return length
        
          
        
        
        # if you need to define validation
    def validate_name(self,value):# value of the   name 
        if len(value) < 2:
            print("jhkjhu")
            raise serializers.ValidationError("name is too short")
        else:
            return value 
    def validate(self,data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("title ana des. shpuld not same")
        else:
            return data    

# validations works when we called the method (serializer.is_valid())

#this is validators (instead of field level validation we can use validators in field as a validator like this )
# we dont need self as aarugument bcz it is out of class

# def name_length(value):
    
#     if len(value) < 2: 
#         raise serializers.ValidationError("name is too short")
#     # else:
#     #     return value 
    

# class MovieSerializer(serializers.Serializer):# in model serializer we can reduce this code also
#     id =serializers.IntegerField(read_only= True)# only access not any change
#     name =serializers.CharField(validators=[name_length])
#     description=serializers.CharField()
#     active= serializers.BooleanField()
     
    
#     def create(self,validated_data):
#         return Movie.objects.create(**validated_data)
        
#     def update(self,instance,validated_data):# instance-old data,validated_data-new data
#         # we have to map everything here and change to old to 
#         #instance.name - old data
#         #validate_data-  new data
#         instance.name = validated_data.get('name',instance.name)
#         instance.description= validated_data.get('description',instance.description)
#         instance.active = validated_data.get('active',instance.active)
#         instance.save() 
#         return instance
    
#     # 3 types of validations are available FIELD -LEVEL,OBJECT-LEVEL,VALIDATION
#     #Field level validation 
#     # def validate_name(self,value):# value of the   name 
#     #     if len(value) < 2:
#     #         print("jhkjhu")
#     #         raise serializers.ValidationError("name is too short")
#     #     else:
#     #         return value 
#         # object level validation
#     def  validate(self,data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("title ana des. shpuld not same")
#         else:
#             return data
        
       # validators
        