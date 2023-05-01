from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'recouvrement'

urlpatterns = [
    # ... other URL patterns ...
    path('login/', auth_views.LoginView.as_view(), name='login'),

        path('notifications/', views.notifications, name='notifications'),
                path('recouvrement/', views.recouvrement, name='recouvrement'),
    path('accepter/<int:pk>/', views.accepter, name='accepter'),
    path('unite/<int:pk>/pdf/', views.generate_pdf, name='generate_pdf'),

####
####
   path('montant_mensuel/', views.montant_mensuel, name='montant_mensuel'),

    path('montant_mensuel_updates/<str:unit>/', views.montant_mensuel_updates, name='montant_mensuel_updates'),
    path('montant_mensuel_updates_anne/<str:unit>/<int:anne>/', views.montant_mensuel_updates_anne, name='montant_mensuel_updates_anne'),

    
]