from django.urls import path
from .views import (
    GenerateSlideView,
    ProjectsView,
    ProjectsListView,
    GoogleAuthView,
    SlideEditView,
    ProjectRetrieveUpdateDestroyView,
    UserProfileView,
    AddSlideView,
    GenerateSlideTitleView,
)
from django.urls import include

urlpatterns = [
    path("generate_slide/", GenerateSlideView.as_view(), name="generate_slide"),
    path("projects/", ProjectsListView.as_view(), name="projects"),
    path("project/<uuid:project_id>/", ProjectsView.as_view(), name="project_slides"),
    path(
        "projects/<uuid:pk>/",
        ProjectRetrieveUpdateDestroyView.as_view(),
        name="project-update",
    ),
    path("google-auth/", GoogleAuthView.as_view(), name="google_auth"),
    path("slide-edit/<int:id>/", SlideEditView.as_view(), name="slide_edit"),
    path("user-profile/", UserProfileView.as_view(), name="user_profile"),
    path(
        "generate-title-slide/",
        GenerateSlideTitleView.as_view(),
        name="generate_title_slide",
    ),
    path("add-slide/<uuid:pk>/", AddSlideView.as_view(), name="add_slide"),
    path(
        "suggest-slide-title/<uuid:pk>/",
        GenerateSlideTitleView.as_view(),
        name="suggest_slide_title",
    ),
]
