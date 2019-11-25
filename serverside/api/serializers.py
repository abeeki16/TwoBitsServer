from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Charity, Category

User = get_user_model()



class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProfileReadSerializer(serializers.ModelSerializer):
    #charities = CharitySerializer(many= True)
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'date_joined','charities','categories')

    def to_representation(self, instance):
        data = super(ProfileReadSerializer, self).to_representation(instance)
        print(data)
        for i in range(len(data['charities'])):
            charity_id = data['charities'][i]
            print(charity_id)
            value = CharitySerializer(Charity.objects.get(id=charity_id)).data
            data['charities'][i] = value
            print(data['charities'])

        return data
    
class ProfileSerializer(serializers.ModelSerializer):
    #charities = CharitySerializer(many= True)
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'date_joined','charities','categories')
    
    def update(self,instance, validated_data):
        charities = validated_data.pop("charities")
        categories = validated_data.pop("categories")
        print(charities)
        for category in categories:
            print(category)
            #charity = Charity.objects.get(id=charity_id)
            instance.categories.add(category)
        for charity in charities:
            print(charity)
            #charity = Charity.objects.get(id=charity_id)
            instance.charities.add(charity)
        return instance
    

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        # Tuple of serialized model fields (see link [2])
        fields = ['username', 'password','email','profile',]
        extra_kwargs = {"password": {"write_only":True}}
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.pop('password'))
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user