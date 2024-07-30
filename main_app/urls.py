from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('skaters/', views.skater_index, name='skater-index'),
    path('skaters/<int:skater_id>/', views.skater_detail, name='skater-detail'),
    path('skaters/create/', views.SkaterCreate.as_view(), name='skater-create'),
    path('skaters/<int:pk>/update/', views.SkaterUpdate.as_view(), name='skater-update'),
    path('skaters/<int:pk>/delete/', views.SkaterDelete.as_view(), name='skater-delete'),
    path(
        'skater/<int:skater_id>/add-behavior/', 
        views.add_behavior, 
        name='add-behavior'
    ),
    path('tricks/create/', views.TrickCreate.as_view(), name='trick-create'),
    path('tricks/<int:pk>/', views.TrickDetail.as_view(), name='trick-detail'),
    path('tricks/', views.TrickList.as_view(), name='trick-index'),
    path('tricks/<int:pk>/update/', views.TrickUpdate.as_view(), name='trick-update'),
    path('tricks/<int:pk>/delete/', views.TrickDelete.as_view(), name='trick-delete'), 
    path('skaters/<int:skater_id>/associate-trick/<int:trick_id>/', views.associate_trick, name='associate-trick'),
    path('skater/<int:skater_id>/remove-trick/<int:trick_id>/', views.remove_trick, name='remove-trick'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
]