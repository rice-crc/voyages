# Pre-compile paths connecting "regions" and link ports to such regions.
from voyages.apps.voyage.cache import *
from voyages.apps.voyage.maps import VoyageRoutes
from scipy.interpolate import interp1d
from haversine import haversine as hdist
import importlib
import numpy as np

def precompile_paths(datasetName, twoWayLinks):
    def get_module(mod):
        return importlib.import_module("tools.animation." + datasetName + "." + mod)
        
    # Import the appropriate files
    region_from = get_module("region_from").region_from
    region_to = get_module("region_to").region_to
    region_network = get_module("region_network")
    routeNodes = region_network.routeNodes
    links = region_network.links
    if twoWayLinks:
        links = links + [(b, a) for (a, b) in links]
    links = set(links)

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
    route_finder = VoyageRoutes(routeNodes, links)

    def get_coords(geo_entry):
        if geo_entry is not None:
            valid_coord = geo_entry.lat and geo_entry.lng
            if valid_coord:
                pt = (float(geo_entry.lat), float(geo_entry.lng))
                valid_coord = abs(pt[0]) + abs(pt[1]) > 0.01
                if valid_coord: return pt
        return None

    def smooth_path(source, target):
        nodes = route_finder.find_route(source, target)
        if nodes is None or source == target: return [routeNodes[source], routeNodes[target]]
        points = np.array([[pt[0] for pt in nodes], [pt[1] for pt in nodes]]).T
        # Linear length along the points:
        distance = np.cumsum(np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1)))
        if len(distance) > 1:
            try:
                distance = np.insert(distance, 0, 0) / distance[-1]
                # Interpolate curve and evaluate at equidistant points along the curve.
                interpolated = interp1d(distance, points, kind='quadratic', axis=0)
                alpha = np.linspace(0, 1, max([20, 5 * len(nodes)]))
                return interpolated(alpha).tolist()
            except: pass
        print str(source) + " " + str(target)
        return [routeNodes[source], routeNodes[target]]

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

    # Construct a collection of pairs (src_region_ind, dest_region_ind) that are
    # actually used, to avoid producing unnecessary paths between hubs.
    def get_port_reg(voyage, mode):
        pk = voyage.emb_pk if mode == 'src' else voyage.dis_pk
        pdata = port_routes[mode].get(pk)
        return None if pdata is None else pdata.get('reg')

    reg_route_pairs = [(s, d) for (s, d) in 
        set([(get_port_reg(v, 'src'), get_port_reg(v, 'dst')) for v in VoyageCache.voyages.values()])
        if s is not None and d is not None and s >= 0 and d >= 0]

    print "Computing " + str(len(reg_route_pairs)) + " smooth paths between routes."

    regional_routes = {}
    computed = 0
    for (sind, dind) in reg_route_pairs:
        if computed % 10 == 0:
            print "Computing path #" + str(computed + 1)
        computed += 1
        d = regional_routes.setdefault(sind, {})
        d[dind] = smooth_path(region_from_nodes[sind], region_to_nodes[dind])

    return regional_routes, port_routes, warnings

def generate_static_files(datasetName, twoWayLinks=False):
    """
    Generate JSON files with regional routes and port paths to respective hubs.
    """
    (regional_routes, port_routes, warnings) = precompile_paths(datasetName, twoWayLinks)
    if len(warnings) > 0:
        print("Warnings (" + unicode(len(warnings)) + ")")
        for w in warnings:
            print(w.encode('utf-8'))
    import os, json
    base_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../voyages/sitemedia/maps/js/', datasetName)
    with open(os.path.join(base_folder, 'regional_routes.json'), 'w') as f:
        json.dump(regional_routes, f)
    with open(os.path.join(base_folder, 'port_routes.json'), 'w') as f:
        json.dump(port_routes, f)

# Tp update the static JSON files, run the following on ./manage.py shell
# from tools.animation.smooth import *
# generate_static_files('trans')
# or
# generate_static_files('intra', True)
