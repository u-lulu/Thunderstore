class CommunityMixin:
    @property
    def get_community_identifier(self):
        return self.kwargs["community_identifier"]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["community_identifier"] = self.get_community_identifier
        return context

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context["community_identifier"] = self.get_community_identifier
        return context