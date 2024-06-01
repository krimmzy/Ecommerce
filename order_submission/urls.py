from django.urls import path
from . import views

urlpatterns = [
	path('shipping/', views.shipping_form, name='shipping_form'),
	path('success/', views.success_view, name='success'),
]