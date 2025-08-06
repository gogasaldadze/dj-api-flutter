from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)


from .querysets import PUBLIC_POSTS_QUERYSET, ALL_POSTS_QUERYSET
from .serializers import PostSerializer
from .filters import PostFilter
from api.permissions import AllowAny, IsAuthenticated
from content.models import Post

# region base classes


class PostAPIView(GenericAPIView):
    queryset = PUBLIC_POSTS_QUERYSET
    serializer_class = PostSerializer
    filterset_class = PostFilter
    permission_classes = [AllowAny]

    search_class = ["owner__name", "title"]
    order_fields = ["created_at"]

    ordering = ["-created_at"]


class PostMeAPIView(PostAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ALL_POSTS_QUERYSET.filter(owner=self.request.user)


# endregion
# region public


class PostListCreateView(ListModelMixin, CreateModelMixin, PostAPIView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostRetrieveView(RetrieveModelMixin, PostAPIView):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# endregion
# region private


class PostMeListView(ListModelMixin, PostMeAPIView):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# endregion
class PostMeRetrieveUpdateDestroyView(
    RetrieveModelMixin, PostMeAPIView, UpdateModelMixin, DestroyModelMixin
):

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance: Post):

        instance.status = Post.Status.DELETED
        instance.save()
