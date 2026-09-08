from django.urls import path
from . import views

urlpatterns = [
    path("", views.ticket_list, name="ticket_list"),
    path("submit/", views.submit_ticket, name="submit_ticket"),
    path("<int:pk>/", views.ticket_detail, name="ticket_detail"),
]