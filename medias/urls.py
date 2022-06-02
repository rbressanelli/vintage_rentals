from django.urls import path

from .views import (MediaRentalsCreateView, MediaRentalsView,
                    MediaRetrieveUpdateDeleteView, MediaView)

urlpatterns = [
    path("medias/", MediaView.as_view()),
    path("medias/<str:media_id>/", MediaRetrieveUpdateDeleteView.as_view()),
    path("medias/<str:media_id>/rentals/", MediaRentalsView.as_view()),
    path("medias/rentals/<str:media_id>/", MediaRentalsCreateView.as_view()),
]
