from collections import OrderedDict

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView, ListAPIView, get_object_or_404
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from thunderstore.community.api.experimental.serializers import (
    PackageListingReportRequestSerializer,
    PackageListingUpdateRequestSerializer,
    PackageListingUpdateResponseSerializer,
)
from thunderstore.community.models import Community, PackageListing
from thunderstore.frontend.api.experimental.serializers.views import (
    CommunitySerializer,
    PackageCategorySerializer,
)
from thunderstore.repository.views.repository import get_package_listing_or_404


class CustomCursorPagination(CursorPagination):
    ordering = "-datetime_created"
    results_name = "results"
    page_size = 100

    def get_paginated_response(self, data) -> Response:
        return Response(
            OrderedDict(
                [
                    (
                        "pagination",
                        OrderedDict(
                            [
                                ("next_link", self.get_next_link()),
                                ("previous_link", self.get_previous_link()),
                            ],
                        ),
                    ),
                    (self.results_name, data),
                ],
            ),
        )


class CustomListAPIView(ListAPIView):
    pagination_class = CustomCursorPagination
    paginator: CustomCursorPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is None:
            raise ValueError("Pagination not set")

        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class CommunitiesExperimentalApiView(CustomListAPIView):
    pagination_class = CustomCursorPagination
    queryset = Community.objects.listed()
    serializer_class = CommunitySerializer

    @swagger_auto_schema(tags=["experimental"])
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class PackageCategoriesExperimentalApiView(CustomListAPIView):
    pagination_class = CustomCursorPagination
    serializer_class = PackageCategorySerializer

    def get_queryset(self):
        community_identifier = self.kwargs.get("community")
        community = get_object_or_404(Community, identifier=community_identifier)
        return community.package_categories

    @swagger_auto_schema(tags=["experimental"])
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class CurrentCommunityExperimentalApiView(APIView):
    serializer_class = CommunitySerializer

    @swagger_auto_schema(
        responses={200: serializer_class()},
        operation_id="experimental.community.current",
        operation_description="Fetch the Community of the queried domain",
        tags=["experimental"],
    )
    def get(self, request, *args, **kwargs):
        serializer = CommunitySerializer(request.community)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PackageListingUpdateApiView(GenericAPIView):
    queryset = PackageListing.objects.active().select_related(
        "community",
        "package",
    )
    serializer_class = PackageListingUpdateResponseSerializer

    @swagger_auto_schema(
        operation_id="experimental.package_listing.update",
        request_body=PackageListingUpdateRequestSerializer,
        responses={200: serializer_class()},
        tags=["experimental"],
    )
    def post(self, request, *args, **kwargs):
        listing: PackageListing = self.get_object()
        request_serializer = PackageListingUpdateRequestSerializer(
            data=request.data, context={"community": listing.community}
        )
        request_serializer.is_valid(raise_exception=True)
        if listing.check_update_categories_permission(request.user):
            listing.update_categories(
                agent=request.user,
                categories=request_serializer.validated_data["categories"],
            )
            get_package_listing_or_404.clear_cache_with_args(
                namespace=listing.package.namespace.name,
                name=listing.package.name,
                community=listing.community,
            )
            serializer = self.serializer_class(instance=listing)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied()


class PackageListingReportApiView(GenericAPIView):
    queryset = PackageListing.objects.active().select_related(
        "community",
        "package",
    )
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="experimental.package_listing.update",
        request_body=PackageListingReportRequestSerializer,
        responses={200: "Success"},
        tags=["experimental"],
    )
    def post(self, request, *args, **kwargs):
        listing: PackageListing = self.get_object()
        request_serializer = PackageListingReportRequestSerializer(
            data=request.data, context={"community": listing.community}
        )
        request_serializer.is_valid(raise_exception=True)
        from thunderstore.repository.models import PackageVersion

        version: PackageVersion = PackageVersion.objects.filter(
            pk=request_serializer.validated_data["package_version_id"]
        ).first()
        if version:
            raise PermissionDenied(f"You tried to report {version.full_version_name}")
        return Response({"success": True})
