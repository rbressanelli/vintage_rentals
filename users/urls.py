from django.urls import path

from users.views import (DeactivateUserProfileView, FilterUserByUserIdView,
                         FilterUserRentalHistoryByUserIdView,
                         GetLoggedUserRentalHistoryView,
                         GetUserProfileOrUpdateUserProfileView, LoginUserView,
                         RegisterAndListUsersView)

urlpatterns = [
    path("users/", RegisterAndListUsersView.as_view()),
    path("users/login/", LoginUserView.as_view()),
    path("users/profile/", GetUserProfileOrUpdateUserProfileView.as_view()),
    path("users/profile/deactivate/", DeactivateUserProfileView.as_view()),
    path("users/<user_id>/", FilterUserByUserIdView.as_view()),
    path("users/profile/rentals/", GetLoggedUserRentalHistoryView.as_view()),
    path("users/<user_id>/rentals/", FilterUserRentalHistoryByUserIdView.as_view()),
]
