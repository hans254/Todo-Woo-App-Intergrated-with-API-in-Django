from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoCompleteSerializer
from todowooApp.models import todowooApp
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password=data['password1'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status = 201)
        except IntegrityError:
            return JsonResponse({'error':'That username has already been taken. Please choose a new username'}, status = 400)

# Create your views here.
class TodoCompletedList(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes   = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return todowooApp.objects.filter(user=user, datecompleted__isnull=False).order_by('-datecompleted')

class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes   = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return todowooApp.objects.filter(user=user, datecompleted__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes   = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return todowooApp.objects.filter(user=user)

class TodoComplete(generics.UpdateAPIView):
    serializer_class = TodoCompleteSerializer
    permission_classes   = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return todowooApp.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.datecompleted = timezone.now()
        serializer.save()