# Provide mapping data for voyages (e.g. routes) cached in the server.
# For convenience, we use the same route nodes and directed links as
# the javascript client side library.
from math import sqrt
from Queue import PriorityQueue
from cache import VoyageCache, CachedGeo
from haversine import haversine as dist
import os, re, threading

class VoyageRoutes():
    def __init__(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        with open(dir + '/../../sitemedia/maps/js/routeNodes.js', 'r') as f:
            s = f.read()
        self._routeJavaScriptData = s 
        self._nodes = [(float(m.group(1)), float(m.group(2))) for m in re.finditer('LatLng\(([0-9\-\.]+),\s*([0-9\-\.]+)\)', s)]
        edges = {}
        all_pairs = [(int(m.group(1)), int(m.group(2))) for m in re.finditer('start:\s*([0-9]+),\s*end:\s*([0-9]+)', s)]
        edges = [[] for _ in self._nodes]
        for a, b in all_pairs:
            edges[a].append((b, dist(self._nodes[a], self._nodes[b])))
        self._edges = edges
        self._routes = {}
        self._voyage_routes = {}
        
    def closest_node(self, pt):
        # This could be replaced by a quad-tree for faster operations.
        return min(enumerate(self._nodes), key=lambda pair: dist(pt, pair[1]))[0]

    def find_route(self, start_index, final_index):
        idx = (start_index, final_index)
        route = self._routes.get(idx)
        if route is None:
            # Calculate route using A* algorithm.
            nodes = self._nodes
            final_pt = nodes[final_index]
            edges = self._edges
            frontier = PriorityQueue()
            frontier.put(start_index, 0)
            came_from = {}
            cost_so_far = {}
            came_from[start_index] = None
            cost_so_far[start_index] = 0
            while not frontier.empty():
                current = frontier.get()
                if current == final_index:
                    break
                for next in edges[current]:
                    # next is a pair (node index, edge distance)
                    next_idx = next[0]
                    new_cost = cost_so_far[current] + next[1]
                    if next_idx not in cost_so_far or new_cost < cost_so_far[next_idx]:
                        cost_so_far[next_idx] = new_cost
                        priority = new_cost + dist(final_pt, nodes[next_idx])
                        frontier.put(next_idx, priority)
                        came_from[next_idx] = current
            route = []
            if final_index in came_from:
                backtrack = final_index
                while backtrack is not None:
                    route.insert(0, nodes[backtrack])
                    backtrack = came_from[backtrack]
            self._routes[idx] = route
        return route

    def get_voyage_routes(self):
        """
        Build or return a cached dictionary indexed by voyage pk
        containing pairs (route, idx) where route is a list of 
        lat-lng pairs and idx is a pair (embarkation port pk,
        disembarkation port pk).
        """
        if self._voyage_routes: return self._voyage_routes
        VoyageCache.load()
        all_voyages = VoyageCache.voyages
        ports = VoyageCache.ports
        port_node_index = {}
        voyage_by_ends = {}
        
        def geo_to_pt(g):
            if g.lat is None or g.lng is None: return None
            return (float(g.lat), float(g.lng)) 
        
        for v in all_voyages.values():
            if v.emb_pk is None or v.dis_pk is None: continue
            idx = (v.emb_pk, v.dis_pk)
            route = voyage_by_ends.get(idx)
            if not route:
                src = geo_to_pt(ports[v.emb_pk])
                dest = geo_to_pt(ports[v.dis_pk])
                if src is None or dest is None: continue
                start_index = port_node_index.get(v.emb_pk)
                finish_index = port_node_index.get(v.dis_pk)
                if start_index is None: 
                    start_index = self.closest_node(src)
                    port_node_index[v.emb_pk] = start_index
                if finish_index is None: 
                    finish_index = self.closest_node(dest)
                    port_node_index[v.dis_pk] = finish_index
                route = self.find_route(start_index, finish_index)
                route = [src] + route + [dest]
                voyage_by_ends[idx] = route
            self._voyage_routes[v.pk] = (route, idx)
        return self._voyage_routes
        
class VoyageRoutesCache:
    _cache = None
    _lock = threading.Lock()
    
    @classmethod
    def load(cls, force_reload = False):
        with cls._lock:
            if force_reload or not cls._cache:
                routes = VoyageRoutes()
                cls._cache = routes.get_voyage_routes()
            return cls._cache