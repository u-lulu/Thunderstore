from django.urls import path

from thunderstore.api.cyberstorm.views import (
    AddTeamMemberAPIView,
    CommunityAPIView,
    CommunityFiltersAPIView,
    CommunityListAPIView,
    CommunityPackageListAPIView,
    NamespacePackageListAPIView,
    PackageDependantsListAPIView,
    PackageDetailAPIView,
    PackageVersionChangelogAPIView,
    PackageVersionReadmeAPIView,
    PackageVersionsAPIView,
    TeamDetailAPIView,
    TeamMembersAPIView,
    TeamServiceAccountsAPIView,
)

cyberstorm_urls = [
    path(
        "community/",
        CommunityListAPIView.as_view(),
        name="cyberstorm.community.list",
    ),
    path(
        "community/<str:community_id>/",
        CommunityAPIView.as_view(),
        name="cyberstorm.community",
    ),
    path(
        "community/<str:community_id>/filters/",
        CommunityFiltersAPIView.as_view(),
        name="cyberstorm.community.filters",
    ),
    path(
        "package/<str:community_id>/",
        CommunityPackageListAPIView.as_view(),
        name="cyberstorm.package.community",
    ),
    path(
        "package/<str:community_id>/<str:namespace_id>/",
        NamespacePackageListAPIView.as_view(),
        name="cyberstorm.package.community.namespace",
    ),
    path(
        "package/<str:community_id>/<str:namespace_id>/<str:package_name>/",
        PackageDetailAPIView.as_view(),
        name="cyberstorm.package.community.namespace.package-details",
    ),
    path(
        "package/<str:community_id>/<str:namespace_id>/<str:package_name>/dependants/",
        PackageDependantsListAPIView.as_view(),
        name="cyberstorm.package.community.namespace.package-dependants",
    ),
    path(
        "team/<str:team_id>/",
        TeamDetailAPIView.as_view(),
        name="cyberstorm.team.detail",
    ),
    path(
        "team/<str:team_id>/members/",
        TeamMembersAPIView.as_view(),
        name="cyberstorm.team.members",
    ),
    path(
        "team/<str:team_name>/members/add/",
        AddTeamMemberAPIView.as_view(),
        name="cyberstorm.team.members.add",
    ),
    path(
        "team/<str:team_id>/service-accounts/",
        TeamServiceAccountsAPIView.as_view(),
        name="cyberstorm.team.service-accounts",
    ),
    # TODO: rethink URL prefixes. Now "package" is in use for community
    # scoped things, so have to use something else for actually package
    # (version) scoped things.
    path(
        "changelog/<str:namespace_id>/<str:package_name>/",
        PackageVersionChangelogAPIView.as_view(),
        name="cyberstorm.package-version.changelog-latest",
    ),
    path(
        "changelog/<str:namespace_id>/<str:package_name>/<str:version_number>/",
        PackageVersionChangelogAPIView.as_view(),
        name="cyberstorm.package-version.changelog",
    ),
    path(
        "readme/<str:namespace_id>/<str:package_name>/",
        PackageVersionReadmeAPIView.as_view(),
        name="cyberstorm.package-version.readme-latest",
    ),
    path(
        "readme/<str:namespace_id>/<str:package_name>/<str:version_number>/",
        PackageVersionReadmeAPIView.as_view(),
        name="cyberstorm.package-version.readme",
    ),
    path(
        "versions/<str:namespace_id>/<str:package_name>/",
        PackageVersionsAPIView.as_view(),
        name="cyberstorm.package.versions",
    ),
]
