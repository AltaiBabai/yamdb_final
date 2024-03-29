from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilterSet(filters.FilterSet):
    """Inner backend's filter set."""

    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = filters.CharFilter(
        field_name='year'
    )
    genre = filters.CharFilter(
        field_name='genre__slug'
    )
    category = filters.CharFilter(
        field_name='category__slug'
    )

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'category']
