from typing import Optional

from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.middleware import csrf
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import DetailView

from thunderstore.community.models import PackageListing
from thunderstore.frontend.url_reverse import get_community_url_reverse_args
from thunderstore.repository.mixins import CommunityMixin
from thunderstore.repository.models import Package
from thunderstore.repository.models.wiki import PackageWiki
from thunderstore.repository.validation.markdown import MAX_MARKDOWN_SIZE
from thunderstore.repository.views.mixins import PackageTabsMixin
from thunderstore.repository.views.repository import get_package_listing_or_404
from thunderstore.wiki.models import WikiPage


class PackageWikiBaseView(CommunityMixin, PackageTabsMixin, DetailView):
    model = PackageListing
    object: Optional[PackageListing] = None
    wiki: Optional[PackageWiki] = None

    def get_wiki(self, package: Package) -> Optional[PackageWiki]:
        if not self.wiki:
            self.wiki = PackageWiki.get_for_package(package, False)
        return self.wiki

    def get_object(self, queryset=None) -> PackageListing:
        if not self.object:
            listing = get_package_listing_or_404(
                namespace=self.kwargs["owner"],
                name=self.kwargs["name"],
                community=self.community,
            )
            if not listing.can_be_viewed_by_user(self.request.user):
                raise Http404("Package is waiting for approval or has been rejected")
            self.object = listing
        return self.object

    def get_create_url(self) -> str:
        return reverse_lazy(
            **get_community_url_reverse_args(
                community=self.community,
                viewname="packages.detail.wiki.page.new",
                kwargs={
                    "owner": self.object.package.namespace.name,
                    "name": self.object.package.name,
                },
            ),
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        package_listing = context["object"]
        context["wiki"] = self.get_wiki(package_listing.package)
        context["can_manage_wiki"] = self.object.package.can_user_manage_wiki(
            self.request.user
        )
        context["create_url"] = self.get_create_url()
        context.update(
            **self.get_tab_context(self.request.user, package_listing, "wiki")
        )
        return context


class PackageWikiPageBaseView(PackageWikiBaseView):
    template_name = "repository/package_wiki_detail.html"
    page: Optional[WikiPage] = None

    def get_page(self, wiki: PackageWiki) -> Optional[WikiPage]:
        if not self.page:
            self.page = WikiPage.objects.filter(
                pk=self.kwargs.get("page"),
                wiki__package_wiki=wiki,
            ).first()
        return self.page

    def get(self, *args, **kwargs) -> HttpResponse:
        page = self.get_page(self.get_wiki(self.get_object().package))
        if page and self.kwargs.get("pslug", "") != page.slug:
            self.kwargs["pslug"] = page.slug
            return redirect(
                reverse(
                    **get_community_url_reverse_args(
                        community=self.community,
                        viewname="packages.detail.wiki.page.detail",
                        kwargs=self.kwargs,
                    )
                )
            )
        return super().get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["page"] = self.get_page(context["wiki"])
        return context


@method_decorator(ensure_csrf_cookie, name="dispatch")
class PackageWikiPageEditView(PackageWikiPageBaseView):
    template_name = "repository/package_wiki_edit.html"

    def get_wiki_url(self):
        return reverse(
            **get_community_url_reverse_args(
                community=self.community,
                viewname="packages.detail.wiki",
                kwargs={
                    "owner": self.object.package.namespace.name,
                    "name": self.object.package.name,
                },
            ),
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page = context["page"]
        context["title"] = "New page" if page is None else "Editing page"
        context["editor_props"] = {
            "editorTitle": context["title"],
            "csrfToken": csrf.get_token(self.request),
            "wikiUrl": self.get_wiki_url(),
            "options": {
                "titleMaxLength": WikiPage._meta.get_field("title").max_length,
                "markdownMaxLength": MAX_MARKDOWN_SIZE,
            },
            "package": {
                "namespace": self.object.package.namespace.name,
                "name": self.object.package.name,
            },
            "page": {
                "id": page.pk,
                "title": page.title,
                "markdown_content": page.markdown_content,
            }
            if page
            else None,
        }
        return context


class PackageWikiHomeView(PackageWikiBaseView):
    template_name = "repository/package_wiki_home.html"

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(*args, **kwargs)


class PackageWikiPageDetailView(PackageWikiPageBaseView):
    not_found_template_name = "repository/package_wiki_404.html"

    def get_edit_url(self) -> str:
        return reverse_lazy(
            **get_community_url_reverse_args(
                community=self.community,
                viewname="packages.detail.wiki.page.edit",
                kwargs=self.kwargs,
            ),
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["edit_url"] = self.get_edit_url()
        return context

    def get(self, request, *args, **kwargs):
        page = self.get_page(self.get_wiki(self.get_object().package))
        if not page:
            return HttpResponseNotFound(
                render(
                    request,
                    self.not_found_template_name,
                    self.get_context_data(object=self.get_object()),
                )
            )
        return super().get(request, *args, **kwargs)
