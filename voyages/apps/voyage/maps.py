from __future__ import absolute_import, unicode_literals

import os
import re
import threading
from queue import PriorityQueue

# Provide mapping data for voyages (e.g. routes) cached in the server.
# For convenience, we use the same route nodes and directed links as
# the javascript client side library.
from future import standard_library
from haversine import haversine as dist

from .cache import VoyageCache

standard_library.install_aliases()


class VoyageRoutes:

    def __init__(self, nodes, links, two_way=False):
        self._nodes = nodes
        edges = [[] for _ in self._nodes]
        for a, b in links:
            ab_dist = dist(self._nodes[a], self._nodes[b])
            edges[a].append((b, ab_dist))
            if two_way:
                edges[b].append((a, ab_dist))
        self._edges = edges
        self._routes = {}
        self._voyage_routes = {}

    def closest_node(self, pt):
        # This could be replaced by a quad-tree for faster operations.
        return min(enumerate(self._nodes),
                   key=lambda pair: dist(pt, pair[1]))[0]

    def find_route(self, start_index, final_index):
        idx = (start_index, final_index)
        route = self._routes.get(idx)
        if route is None:
            # Calculate route using A* algorithm.
            nodes = self._nodes
            final_pt = nodes[final_index]
            edges = self._edges
            frontier = PriorityQueue()
            frontier.put((0, start_index))
            came_from = {}
            cost_so_far = {}
            came_from[start_index] = None
            cost_so_far[start_index] = 0
            while not frontier.empty():
                (_, current) = frontier.get()
                if current == final_index:
                    break
                for (next_idx, edge_cost) in edges[current]:
                    new_cost = cost_so_far[current] + edge_cost
                    current_cost = cost_so_far.get(next_idx)
                    if current_cost is None or new_cost < current_cost:
                        cost_so_far[next_idx] = new_cost
                        priority = new_cost + dist(final_pt, nodes[next_idx])
                        frontier.put((priority, next_idx))
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
        if self._voyage_routes:
            return self._voyage_routes
        VoyageCache.load()
        all_voyages = VoyageCache.voyages
        ports = VoyageCache.ports
        port_node_index = {}
        voyage_by_ends = {}

        def geo_to_pt(g):
            if g.lat is None or g.lng is None:
                return None
            return (float(g.lat), float(g.lng))

        for v in list(all_voyages.values()):
            if v.emb_pk is None or v.dis_pk is None:
                continue
            idx = (v.emb_pk, v.dis_pk)
            route = voyage_by_ends.get(idx)
            if not route:
                src = geo_to_pt(ports[v.emb_pk])
                dest = geo_to_pt(ports[v.dis_pk])
                if src is None or dest is None:
                    continue
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
    def load(cls, force_reload=False):
        with cls._lock:
            if force_reload or not cls._cache:
                name = os.path.dirname(os.path.abspath(__file__))
                with open(name + '/../../sitemedia/maps/js/route_nodes.js',
                          'r') as f:
                    s = f.read()
                nodes = [(float(m.group(1)), float(m.group(2)))
                         for m in re.finditer(
                             r'LatLng\(([0-9\-\.]+),\s*([0-9\-\.]+)\)', s)]
                links = [(int(m.group(1)), int(m.group(2)))
                         for m in re.finditer(
                             r'start:\s*([0-9]+),\s*end:\s*([0-9]+)', s)]
                routes = VoyageRoutes(nodes, links)
                cls._cache = routes.get_voyage_routes()
            return cls._cache
