# Pre-compile paths connecting "regions" and link ports to such regions.
from voyages.apps.voyage.cache import *
from region_from import *
from region_to import *
from region_network import *
from scipy.interpolate import interp1d
from mpu import haversine_distance as hdist
import numpy as np

def precompile_paths():
    VoyageCache.load()
    source_port_pks = set([v.emb_pk for v in VoyageCache.voyages.values() if v.emb_pk])
    dest_port_pks = set([v.dis_pk for v in VoyageCache.voyages.values() if v.dis_pk])
    
    # Map closest point from an origin.
    def get_closest(origin, choices):
        min_index = min(enumerate(choices), key=lambda (_, pt): hdist(pt, origin))[0]
        return min_index

    region_from_nodes = [get_closest(r, routeNodes) for r in region_from]
    region_to_nodes = [get_closest(r, routeNodes) for r in region_to]
    # We now compute the regional routes.
    distances = [hdist(routeNodes[s], routeNodes[d]) for (s, d) in links]
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
        if path is None: return [routeNodes[source], routeNodes[target]]
        path = path[1]
        nodes = [routeNodes[idx] for idx in path]
        points = np.array([[pt[0] for pt in nodes], [pt[1] for pt in nodes]]).T
        # Linear length along the points:
        distance = np.cumsum(np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1)))
        distance = np.insert(distance, 0, 0) / distance[-1]
        # Interpolate curve and evaluate at equidistant points along the curve.
        interpolated = interp1d(distance, points, kind='quadratic', axis=0)
        alpha = np.linspace(0, 1, max([20, 5 * len(path)]))
        return interpolated(alpha).tolist()

    regional_routes = [[smooth_path(region_from_nodes[sind], region_to_nodes[dind]) 
        for dind in range(0, len(region_to))] 
        for sind in range(0, len(region_from))]

    def get_coords(geo_entry):
        if geo_entry is not None:
            valid_coord = geo_entry.lat and geo_entry.lng
            if valid_coord:
                pt = (float(geo_entry.lat), float(geo_entry.lng))
                valid_coord = abs(pt[0]) + abs(pt[1]) > 0.01
                if valid_coord: return pt
        return None

    warnings = []
    
    def connect_port_to_region(regions, threshold=5000):
        proutes = {}
        for (pk, p) in VoyageCache.ports.items():
            pt = get_coords(p)
            if pt is None:
                # This is an invalid coordinate, try parent coordinates instead.
                pt = get_coords(VoyageCache.regions.get(p.parent))
            if pt is None: 
                warnings.append('Port [' + str(pk) + ']' + p.name + ' has invalid coordinates')
                proutes[pk] = { 'reg': -1, 'path': [pt], 'name': p.name }
                continue
            closest_region_index = get_closest(pt, regions)
            region_pt = regions[closest_region_index]
            closest_distance = hdist(pt, region_pt)
            proutes[pk] = { 'reg': closest_region_index, 'path': [pt], 'name': p.name }
            if closest_distance > threshold:
                warnings.append('Port [' + str(pk) + ']' + p.name + ' is too far from any regional hub')
        return proutes

    port_routes = {}
    port_routes['src'] = connect_port_to_region(region_from)
    port_routes['dst'] = connect_port_to_region(region_to)
    return regional_routes, port_routes, warnings

def generate_static_files():
    """
    Generate JSON files with regional routes and port paths to respective hubs.
    """
    (regional_routes, port_routes, warnings) = precompile_paths()
    if len(warnings) > 0:
        print("Warnings (" + str(len(warnings)) + ")")
        for w in warnings:
            print(w)
    import os, json
    base_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../voyages/sitemedia/maps/js/')
    with open(os.path.join(base_folder, 'regional_routes.json'), 'w') as f:
        json.dump(regional_routes, f)
    with open(os.path.join(base_folder, 'port_routes.json'), 'w') as f:
        json.dump(port_routes, f)

# Tp update the static JSON files, run the following on ./manage.py shell
# from tools.animation.smooth import *
# generate_static_files()
