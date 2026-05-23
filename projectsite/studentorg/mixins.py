from django.db.models import Q


class SearchableListMixin:
    """Filter list queryset by ?q= across search_fields (icontains)."""

    search_fields = ()

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query and self.search_fields:
            criteria = Q()
            for field in self.search_fields:
                criteria |= Q(**{f'{field}__icontains': query})
            qs = qs.filter(criteria)
        return qs


class SortableListMixin:
    """Order list by ?sort_by= when value is in sort_fields."""

    sort_fields = ()
    default_sort = None

    def get_ordering(self):
        sort_by = self.request.GET.get('sort_by')
        if sort_by in self.sort_fields:
            return sort_by
        return self.default_sort
