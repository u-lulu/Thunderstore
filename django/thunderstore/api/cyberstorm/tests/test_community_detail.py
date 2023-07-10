import pytest
from rest_framework.test import APIClient

from thunderstore.community.factories import PackageListingFactory
from thunderstore.community.models import CommunitySite


@pytest.mark.django_db
def test_api_cyberstorm_community_detail_success(
    client: APIClient, community_site: CommunitySite
):
    PackageListingFactory(
        community_=community_site.community, package_version_kwargs={"downloads": 0}
    )
    PackageListingFactory(
        community_=community_site.community, package_version_kwargs={"downloads": 23}
    )
    PackageListingFactory(
        community_=community_site.community, package_version_kwargs={"downloads": 42}
    )

    response = client.get(
        f"/api/cyberstorm/community/{community_site.community.identifier}/",
        HTTP_HOST=community_site.site.domain,
    )
    assert response.status_code == 200
    response_data = response.json()

    c = community_site.community

    assert c.name == response_data["name"]
    assert c.identifier == response_data["identifier"]
    assert c.total_download_count == response_data["total_download_count"]
    assert c.total_package_count == response_data["total_package_count"]
    assert c.background_image_url == response_data["background_image_url"]
    assert c.description == response_data["description"]
    assert c.discord_url == response_data["discord_url"]


@pytest.mark.django_db
def test_api_cyberstorm_community_detail_failure(
    client: APIClient, community_site: CommunitySite
):
    response = client.get(
        f"/api/cyberstorm/community/bad/",
        HTTP_HOST=community_site.site.domain,
    )
    assert response.status_code == 404
