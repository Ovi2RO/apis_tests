from rest_framework import generics, permissions
from .serializers import ProfileSerializer
from .models import Profile
from .permissions import IsSuperuser, IsProfileOwnerOrSuperuser

class ProfileCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer