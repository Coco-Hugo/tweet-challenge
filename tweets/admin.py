from django.contrib import admin
from django.db.models import Q
from .models import Tweet, Like

class ElonMuskFilter(admin.SimpleListFilter):
    title = 'Contains Elon Musk'
    parameter_name = 'contains_elon_musk'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Contains Elon Musk'),
            ('no', 'Does not contain Elon Musk'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(payload__icontains='Elon Musk')
        if self.value() == 'no':
            return queryset.exclude(payload__icontains='Elon Musk')
        return queryset

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    search_fields = (
        "payload",
        "user__username",
    )
    
    list_display = (
        "payload",
        "user",
        "like_count",
    )
    
    list_filter = (
        "created_at",
        ElonMuskFilter,  # Add the custom filter here
    )

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    search_fields = (
        "user__username",
    )
    
    list_filter = (
        "created_at",
    )
