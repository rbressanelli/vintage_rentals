from django.urls import path
from .views import MediaView, MediaRentalsView, MediaRetrieveUpdateDeleteView

urlpatterns = [
    path('medias/', MediaView.as_view()),
    path('medias/<str:media_id>/', MediaRetrieveUpdateDeleteView.as_view()),
    path('medias/<str:media_id>/rentals/', MediaRentalsView.as_view() )
]