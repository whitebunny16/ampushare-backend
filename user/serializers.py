from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from user.models import Profile, Buddy, User

UserModel = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class LoggedInUserSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(source='profile.profile_pic')

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'profile_image',
        )


class UserLoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = LoggedInUserSerializer()


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Profile
        fields = ['user_id', 'first_name', 'last_name', 'email', 'username', 'profile_pic', 'date_of_birth',
                  'gender', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'profile']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create_user(**validated_data)
        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No user found with this email address."), code='invalid')
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(style={'input_type': 'password'})

    def validate_email(self, value):
        if not UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No user found with this email address."), code='invalid')
        return value


class FollowBuddySerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(source='profile.profile_pic', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'profile_pic']


class BuddySerializer(serializers.ModelSerializer):
    follower = FollowBuddySerializer(read_only=True)
    following = FollowBuddySerializer(read_only=True)

    class Meta:
        model = Buddy
        fields = ['id', 'follower', 'following']

    def to_representation(self, instance):
        self.fields['follower'] = FollowBuddySerializer()
        self.fields['following'] = FollowBuddySerializer()
        return super(BuddySerializer, self).to_representation(instance)

    def to_internal_value(self, data):
        self.fields['follower'] = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
        self.fields['following'] = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
        return super(BuddySerializer, self).to_internal_value(data)
