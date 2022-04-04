from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework import viewsets, permissions, pagination, generics, filters
from rest_framework.views import APIView
from .serializers import PostSerializer, TagSerializer, ContactSerializer, RegisterSerializer, UserSerializer, CommentSerializer
from .models import Post, Comment
from rest_framework.response import Response
from taggit.models import Tag
# Create your views here.
class PageNumberSetPagination(pagination.PageNumberPagination):
    # вывод постов с пагинацией
    page_size = 6
    page_size_query_param = 'page_size'
    ordering = 'created'

# Вывод всех постов

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    # поле, по которому будем получать одну запись
    lookup_field = 'url_slug'
    permission_classes = [permissions.AllowAny]
    # можно применять класс PostViewSet к любому View - использовать пагинацию для вывода списка постов
    pagination_class = PageNumberSetPagination

    # доп. поля, для поиска
    search_fields = ['content', 'h1', 'descr']
    filter_backends = (filters.SearchFilter,)


class TagDetailView(generics.ListAPIView):
    # устанавливаем сериалайзер для получения статей по опр. тегу из БД
    serializer_class = PostSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # получаем только записи с нужным тегом

        tag_slug = self.kwargs['tag_slug'].lower()
        print("ts=", tag_slug)
        tag = Tag.objects.get(slug=tag_slug)
        print("ts=", tag_slug, "t=", tag)
        return Post.objects.filter(tag=tag)


class TagView(generics.ListAPIView):
    # для получения списка тегов
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

class AsideView(generics.ListAPIView):
    # вывод 5 последних постов сбоку справа
    queryset = Post.objects.all().order_by('-id')[:5]
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

class FeedbackView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        # сохраняем данные, пришедшие с фронта
        serializer_class = ContactSerializer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            # отправляем полученные с формы данные на почту
            send_mail(f'От {name} | {subject}', message, from_email, ['mihail7538@gmail.com'])
            return Response({"success":"Sent"})

class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save() # задействуется метод create из сериалайзера
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message":"Пользователь успешно создан"
        })

class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        print("rr", request.user)
        return Response({
            "user": UserSerializer(request.user, context=self.get_serializer_context()).data,
        })

class GetCommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        post_slug = self.kwargs['post_slug'].lower()
        print('ps', post_slug)
        post = Post.objects.get(url_slug=post_slug)
        return Comment.objects.filter(post=post)

class AddCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

def index(request):
    return render(request, 'core/index.html')