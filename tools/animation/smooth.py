# Pre-compile paths connecting "regions" and link ports to such regions.
from voyages.apps.voyage.cache import *
from region_from import *
from region_to import *
from region_network import *
from scipy.interpolate import interp1d
import numpy as np
import mpu

def precompile_paths():
    VoyageCache.load()
    source_port_pks = set([v.emb_pk for v in VoyageCache.voyages.values() if v.emb_pk])
    dest_port_pks = set([v.dis_pk for v in VoyageCache.voyages.values() if v.dis_pk])

    def get_port(pk):
        p = VoyageCache.ports[pk]
        return (float(p.lat), float(p.lng))
    
    # Map closest point from an origin.
    def get_closest(origin, choices):
        min_index = min(enumerate(choices), key=lambda (_, pt): mpu.haversine_distance(pt, origin))[0]
        return min_index

    source_regions = { pk: get_closest(get_port(pk), region_from) for pk in source_port_pks }
    dest_regions = { pk: get_closest(get_port(pk), region_to) for pk in dest_port_pks }
    region_from_nodes = [get_closest(r, routeNodes) for r in region_from]
    region_to_nodes = [get_closest(r, routeNodes) for r in region_to]

    regional_pairs = set([(region_from_nodes[source_regions[v.emb_pk]], region_to_nodes[dest_regions[v.dis_pk]])
        for v in VoyageCache.voyages.values() if v.emb_pk and v.dis_pk])

    # We now compute the regional routes.
    distances = [mpu.haversine_distance(routeNodes[s], routeNodes[d]) for (s, d) in links]
    n = len(routeNodes)
    outlinks = [[(d, link_index) for (link_index, (s, d)) in enumerate(links) if s == i] for i in range(0, n)]

    # We are doing a Depth first search since the network is very 
    # low degree and we do not need to be very fast in the tooling code.
    def find_path(source, target):
        if source == target: return (0.0, [target])
        best = None
        for (neighbor, link_index) in outlinks[source]:
            candidate = find_path(neighbor, target)
            if candidate is not None:
                candidate_dist = distances[link_index] + candidate[0]
                if best is None or candidate_dist < best[0]:
                    best = [candidate_dist, candidate[1]]
        return (best[0], [source] + best[1]) if best else None

    def smooth_path(source, target):
        path = find_path(source, target)
        if path is None: return None
        path = path[1]
        nodes = [routeNodes[idx] for idx in path]
        points = np.array([[pt[0] for pt in nodes], [pt[1] for pt in nodes]]).T
        # Linear length along the points:
        distance = np.cumsum(np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1)))
        distance = np.insert(distance, 0, 0) / distance[-1]
        # Interpolate curve and evaluate at equidistant points along the curve.
        interpolated = interp1d(distance, points, kind='quadratic', axis=0)
        alpha = np.linspace(0, 1, max([20, 5 * len(path)]))
        return interpolated(alpha)

    regional_routes = [(s, d, smooth_path(s, d)) for (s, d) in regional_pairs]
    return regional_routes

# from tools.animation.smooth import *
# from tools.animation.region_from import *
# from tools.animation.region_to import *
# from tools.animation.region_network import *
# precompile_paths()
