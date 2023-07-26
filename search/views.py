from django.shortcuts import render
from collections import defaultdict 
from heapq import heappop, heappush

from .forms import ShortestPathForm
from .models import Places, Distance

def find_shortest_distance(request): 
        form = ShortestPathForm(request.POST or None)
        template = 'search/generics.html'
        shortest_distance = None
        shortest_path = None 
        
        # all_places = Distance.objects.all()
        
        if request.method == 'POST': 
                if form.is_valid(): 
                        source_place = form.cleaned_data['source_place']
                        destination_place = form.cleaned_data['destination_place']
                        
                        shortest_distance, shortest_path = dijkstra_shorest_path(source_place, destination_place)
                        shortest_path = ' --> '.join([place.name for place in shortest_path])
        return render(request, template, {'form' : form, 'shortest_distance' : shortest_distance, 'shortest_path' : shortest_path}) # 'all_places' : all_places})



def dijkstra_shorest_path(source, destination): 
        ''' Dijkstra Algorithm '''
        dist = defaultdict(lambda: float('inf'))
        
        # Here, source and destination are instances of Places model.
        # using the ID of the instances of Places as the key 
        dist[source.id] = 0 
        parent = {}
        
        priority_queue = [(0, source.id)]
        
        try: 
                while priority_queue: 
                        distance_u, node_u_id = heappop(priority_queue)
                        
                        if node_u_id == destination.id: 
                                break 
                        
                        if distance_u > dist[node_u_id]: 
                                continue
                        
                        node_u = Places.objects.get(pk=node_u_id)
                        
                        for edges in node_u.source_places.all(): # source_places is related name (in edges : Node A <--> B and cost is present as it is an object of Distance model)
                                adjNode = edges.destination_place
                                weight = edges.distance 
                                distance_to_adjNode = distance_u + weight
                                # print(adjNode.name)
                                # print(distance_to_adjNode)
                                
                                if distance_to_adjNode < dist[adjNode.id]: 
                                        dist[adjNode.id] = distance_to_adjNode
                                        parent[adjNode.id] = node_u_id
                                        heappush(priority_queue, (distance_to_adjNode, adjNode.id))
        except Exception as e : 
                raise e 
                
        
        # Path Tracing 
        if destination.id not in parent: 
                return None 
        
        shortest_path = []
        curr_node_id = destination.id
        
        while True: 
                curr_node = Places.objects.get(pk=curr_node_id)
                shortest_path.append(curr_node)
                if curr_node_id == source.id: 
                        break
                curr_node_id = parent[curr_node_id]

        shortest_path.reverse()
        shortest_distance = dist[destination.id]
        
        return shortest_distance, shortest_path 

        
        
        
        
        
        
        