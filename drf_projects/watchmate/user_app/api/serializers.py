from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)  # bcz this password2 is no define in user model so we define this field
    
    
    
    class Meta:
        model = User
        fields = ['username','email','password','password2']
        extra_Kwargs = {
            'passowrd' : {'write_only':True}
        }
    
    
    def save(self):
        password = self.validate_data['password']
        password2 = self.validate_data['password2']
          
        if password != password2:
            raise serializers.ValidationError({'error':'p1 and p2 should be same !'})

        
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':"email already exists!"})
        
        
        account = User(email= self.validated_data['email'],username= self.validated_data['username'])
        account.set_password(password)
        account.save()
        
        return account