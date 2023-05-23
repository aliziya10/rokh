from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



class ExpertiseSelializer(serializers.ModelSerializer):
    class Meta:
        model = Expertise
        fields = ("id", 'title','image','text')


class ExampleSerializer(serializers.ModelSerializer):
    doctor = serializers.ReadOnlyField(source='doctor.username')
    # expertise = serializers.SerializerMethodField()

    class Meta:
        model = Example
        fields = '__all__'
        read_only_fields = ['id', 'doctor']

    #
    # def get_expertise(self, instance):
    #     return instance.expertise.title if instance.expertise else None

class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    # is_superuser = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    # is_staff=serializers.SerializerMethodField()
    # is_doctor=serializers.SerializerMethodField()
    expertise = ExpertiseSelializer(many=True)
    class Meta:
        model = Profile
        fields = ('user_id', 'username', 'name', 'bio', 'profile_image', 'expertise',"birth_year", 'pezeshki_code', 'working_hour')
        read_only_fields = ('id', 'doctor')

    #
    # def get_is_superuser(self, obj):
    #     return obj.user.is_superuser
    #
    def get_username(self,obj):
        return obj.user.username
    #
    # def get_is_staff(self,obj):
    #     return obj.user.is_staff
    #
    # def get_is_doctor(self,obj):
    #     return obj.user.is_doctor


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
