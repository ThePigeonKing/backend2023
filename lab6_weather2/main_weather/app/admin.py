from django.contrib import admin
from .models import Location, WeatherData, Forecast, Subscription, Observation
from django.utils.html import format_html

admin.site.register(Location)
admin.site.register(WeatherData)
admin.site.register(Forecast)
admin.site.register(Subscription)

class ObservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'location', 'date_of_review', 'temperature', 'state')
    list_filter = ('user', 'location', 'date_of_review')
    search_fields = ('name', 'commentary')

    def observation_thumbnail(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="width: 50px; height:auto;">', obj.icon.url)
        else:
            return "No Image"
    observation_thumbnail.short_description = "Thumbnail"

# Register the Observation model with the custom admin options
admin.site.register(Observation, ObservationAdmin)
