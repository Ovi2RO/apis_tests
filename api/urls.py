from django.urls import path
from .views import ProfileCreateView, ProfileDetailView

urlpatterns = [
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('', ProfileCreateView.as_view(), name='profile_list'),
]
