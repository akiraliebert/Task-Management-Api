import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    due_before = django_filters.IsoDateTimeFilter(field_name="due_date", lookup_expr="lte")
    due_after = django_filters.IsoDateTimeFilter(field_name="due_date", lookup_expr="gte")
    created_before = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")
    created_after = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")

    class Meta:
        model = Task
        fields = ["status", "category", "due_before", "due_after", "created_before", "created_after"]
