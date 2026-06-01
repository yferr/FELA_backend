"""
OwnershipMixin — Mixin for ModelViewSets that:
1. Applies IsOwnerOrSuperuser as the default permission class.
2. Automatically assigns request.user to created_by on perform_create.

Usage (order matters — mixin must come first):
    class MyViewSet(OwnershipMixin, viewsets.ModelViewSet):
        queryset = MyModel.objects.all()
        serializer_class = MySerializer
"""
from .permissions import IsOwnerOrSuperuser


class OwnershipMixin:
    permission_classes = [IsOwnerOrSuperuser]

    def perform_create(self, serializer):
        """
        Assigns the authenticated user as the record owner.
        The client cannot supply this value — it is always taken from request.user.
        """
        serializer.save(created_by=self.request.user)