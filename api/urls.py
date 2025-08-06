from django.urls import include, path

urlpatterns = [
    path("post/", include("api.post.urls")),
    # path("comment", include("api.comment.urls")),
    path("auth/", include("api.auth.urls")),
]
