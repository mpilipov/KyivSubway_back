from rest_framework import serializers
from .models import Post, Comment
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.auth.models import User
from taggit.models import Tag

# Сериалайзер для постов
class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tag = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Post
        # какие поля нам нужны из БД
        fields = ("id", "h1", "title", "url_slug", "descr", "content", "image", "created", "author", "tag")
        # Запись получается из БД по полю slug
        lookup_field = "url_slug"
        extra_kwargs = {
            'url':{'lookup_field':'url_slug'}
        }

# Сериалайзер для тегов
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name", "slug", ) #!!!! В конце обязательна запятая!
        lookup_field = 'name'
        extra_kwargs = {
            'url':{'lookup_field':'name'}
        }

# Сериалайзер для страницы с обратной связью
class ContactSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    subject = serializers.CharField()
    message = serializers.CharField()

# Сериалайзер для регистрации
class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)
    class Meta:
        # указываем модель на основе которой создаем сериализатор
        model = User
        fields = [
            "username",
            "password",
            "password2"
        ]
        extra_kwargs = {"password": {"write_only": True}}
    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password":"Пароли не совпадают"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user
# Сериалайзер возвращает все данные о только что зарегистрировавшемся пользователе
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# Сериалайзер возвращает комментарии формата json
class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    post = serializers.SlugRelatedField(slug_field="url_slug", queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ("id", "post", "username", "text", "created")
    #    lookup_field = "id"
   #     extra_kwargs = {
      #      'url':{'lookup_field':'id'}
        #}