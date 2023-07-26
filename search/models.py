from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Places(models.Model): 
        ''' This model stores a node, and all of its adjacent nodes (adjacent nodes are stored n parent_places) '''
        name = models.CharField(max_length=150)
        adjacent_places = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='adj_places')
        
        def __str__(self): 
                return self.name 
        

class Distance(models.Model): 
        ''' This model stores the edge and edge cost '''
        source_place = models.ForeignKey(Places, on_delete=models.CASCADE, related_name='source_places')
        destination_place = models.ForeignKey(Places, on_delete=models.CASCADE, related_name='destination_places')
        distance = models.DecimalField(max_digits=10, decimal_places=2)
        
        def __str__(self): 
                return f'{self.source_place} to {self.destination_place} : {self.distance} km'


@receiver(post_save, sender=Distance)
def create_or_update_reverse_distance(sender, instance, created, **kwargs): 
        ''' Signal to make the distances like undirected graph  '''
        if created : 
                reverse_distance, _ = Distance.objects.get_or_create(
                        source_place=instance.destination_place,
                        destination_place = instance.source_place, 
                        defaults={'distance' : instance.distance}
                )
        else : # not necessary though this else block as if block get_or_create will handle both 
                reverse_distance = Places.objects.get(
                        source_place=instance.destination_place,
                        destination_place = instance.source_place, 
                )
                
                reverse_distance.distance = instance.distance
                reverse_distance.save()
                
                
                


'''
symmetrical=False makes the Distance model as kind of Directed graph. 
and the Signal makes the model like an undirected graph. 

'''
                
                
                
                
                