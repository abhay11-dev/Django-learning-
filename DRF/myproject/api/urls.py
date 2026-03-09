from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'employees', views.EmployeeViewSet, basename='employee')

urlpatterns = [
    path('students/', views.studentsView),
    path('students/<int:id>/', views.studentDetailView),

    path('', include(router.urls)),

    path('blogs/', views.BlogView.as_view(), name='blog-create'),
    path('comments/', views.CommentView.as_view(), name='comment-create'),
    
    path('blogs/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),

    path('chats/', include('chat.urls')),
]