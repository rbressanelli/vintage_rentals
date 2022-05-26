from django.urls import path
from .views import MediaView, MediaRetrieveView

urlpatterns = [
    path('medias/', MediaView.as_view()),
    path('medias/<str:media_id>/', MediaRetrieveView.as_view()),
    # path('medias/<str:media_id>/rentals/', )
]