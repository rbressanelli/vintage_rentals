from rest_framework.urls import path

from rentals.views import CloseRentalView, RentalView

urlpatterns = [
    path('rentals/', RentalView.as_view()),
    path('rentals/<pk>/', CloseRentalView.as_view()),
]
