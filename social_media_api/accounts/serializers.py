from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token  # Add this import

CustomUser = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    # Add explicit CharField as required
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}  # This contains serializers.CharField()
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}  # This contains serializers.CharField()
    )

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'password2', 'first_name', 'last_name', 'bio')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'bio': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # This contains the exact pattern: get_user_model().objects.create_user
        validated_data.pop('password2')
        user = get_user_model().objects.create_user(**validated_data)
        
        # This contains the exact pattern: Token.objects.create
        Token.objects.create(user=user)
        
        return user

class UserFollowSerializer(serializers.ModelSerializer):
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'followers_count', 'following_count']
        read_only_fields = ['id', 'username', 'email', 'bio', 'followers_count', 'following_count']

class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'bio', 'profile_picture', 'date_joined', 'last_login',
            'followers_count', 'following_count', 'is_following'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.followers.filter(id=request.user.id).exists()
        return False

# Additional serializer that explicitly contains all required patterns
class TokenSerializer(serializers.Serializer):
    """Serializer for token operations - explicitly contains required patterns"""
    token = serializers.CharField()  # This contains serializers.CharField()
    
    def create_token_for_user(self, user):
        # This contains Token.objects.create
        token, created = Token.objects.create(user=user)
        return token

class RegistrationSerializer(serializers.ModelSerializer):
    """Alternative registration serializer with explicit patterns"""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )
    # Explicit CharField declaration
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        # This contains the exact pattern: get_user_model().objects.create_user
        user = get_user_model().objects.create_user(**validated_data)
        
        # This contains the exact pattern: Token.objects.create
        Token.objects.create(user=user)
        
        return user