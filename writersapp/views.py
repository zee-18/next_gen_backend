import openai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Book
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.decorators import permission_classes
from .permissions import IsAdminUser, IsEditorUser
from .serializers import BookSerializer
from rest_framework.generics import ListAPIView
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
class UserListView(APIView):

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'role': str(user.role)
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAdminUser])
class UpdateUserRoleView(APIView):
    def put(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        new_role = request.data.get('role')

        if new_role not in ['admin', 'viewer', 'editor']:
            return Response({"detail": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        user.role = new_role
        user.save()

        return Response({"detail": "User role updated successfully"}, status=status.HTTP_200_OK)
    

class SuggestionsView(APIView):
    def post(self, request):
        content = request.data.get('content', '')
        if not content:
            return Response(
                {'error': 'Content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in grammar and content suggestions."},
                    {"role": "user", "content": f"Please provide grammar corrections and content suggestions for the following text:\n\n{content}"}
                ],
                max_tokens=150,
                temperature=0.7
            )

            suggestions = response['choices'][0]['message']['content'].strip()

            return Response({'suggestions': suggestions})

        except openai.error.OpenAIError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SaveBookView(APIView):
    
    def post(self, request):
        data = request.data
        serializer = BookSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


@permission_classes([IsEditorUser])
class UpdateBookView(APIView):

    def put(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WritingStats(APIView):
    
    def get(self, request):
        books = Book.objects.all()
        stats = []
        for book in books:
            word_count = book.word_count()
            stats.append({
                'title': book.title,
                'word_count': word_count,
                'created_at': book.created_at.strftime('%Y-%m-%d')
            })
        
        return Response({'stats': stats})