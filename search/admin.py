from django.contrib import admin

# Register your models here.
from .models import Places, Distance

@admin.register(Places)
class PlacesAdmin(admin.ModelAdmin): 
        list_display = ('name', 'get_adjacent_places')
        
        def get_adjacent_places(self, obj): 
                adjacent_places = ', '.join([adjacent_place.name for adjacent_place in obj.adjacent_places.all()])
                return adjacent_places
        
        get_adjacent_places.short_description = 'Adjacent Places'
        # short_description is admin's built in - the str will be shown in place of the func name in admin panel 
        

@admin.register(Distance)
class DistanceAdmin(admin.ModelAdmin): 
        list_display = ('source_place', 'destination_place', 'distance')
        