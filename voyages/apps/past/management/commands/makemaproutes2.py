from voyages.apps.past.models import Enslaved,LanguageGroup,ModernCountry
from voyages.apps.common.utils import *
import csv
from django.core.management.base import BaseCommand
import os
import re
import json
from math import sqrt
from voyages.apps.past.models import Enslaved
from voyages.apps.voyage.models import Place,Region,Voyage
import networkx as nx
from voyages.apps.assessment.models import Estimate,ExportRegion,ImportRegion

class Command(BaseCommand):

	def handle(self, *args, **options):
		from voyages.apps.past.management.commands.diaspora import routeNodes,links
		base_path='voyages/apps/past/'
		print('making a directed network graph of the oceanic waypoints from diaspora.py')
		
		#nodes have
		##lat/long coordinates
		##and their id's range from offset:offset+len(routeNodes)
		
		offset=1000000000
		
		G=nx.DiGraph()
		c=0
		for n in routeNodes:
			latlong=n
			G.add_node(c+offset,coords=latlong)
			c+=1
		
		#edges have
		#a source and targetnode (already in the graph)
		#an id (ranging from 1:len(links))
		#a weight (euclidean distance btw source & target lat/long)
		
		all_targets={}
		all_sources={}
		
		adjacency_ids_lookup={}
		
		def dict_tree(s,t,d,c):
			if s in d:
				d[s][t]=c
			else:
				d[s]={t:c}
			return d
			
		edgecount=1
		for e in links:
			print(e)
			s,t=e
			s_id=s+offset
			t_id=t+offset
			
			s_c=G.nodes[s_id]['coords']
			t_c=G.nodes[t_id]['coords']
			
			s_lat,s_long=s_c
			t_lat,t_long=t_c
			
			distance=sqrt((s_lat-t_lat)**2 + (s_long-t_long)**2)
			
			G.add_edge(s_id,t_id,weight=distance,id=edgecount)
			adjacency_ids_lookup=dict_tree(s_id,t_id,adjacency_ids_lookup,edgecount)		
			
			edgecount+=1
		
		# now we get itinerary source/target pairs
		
		# pull the estimates
		estimate=Estimate.objects.all()
		# filter for the year range 1808-1848
		estimate=estimate.filter(year__gte=1808)
		estimate=estimate.filter(year__lte=1848)
		
		estimate.select_related(
			'embarkation_region',
			'disembarkation_region'
		)
		
		estimate=estimate.filter(embarkation_region__longitude__lte=30)
		estimate=estimate.filter(embarkation_region__longitude__gte=-25)
		stpairs=list(set(estimate.values_list(
			'embarkation_region__name',
			'embarkation_region__latitude',
			'embarkation_region__longitude',
			'disembarkation_region__name',
			'disembarkation_region__latitude',
			'disembarkation_region__longitude'
		)))
		
		## use the source/target pairs to make onramps & offramps
		print('making onramps & offramps in digraph')
		
		embarkation_regions={s[0]:(s[1],s[2]) for s in stpairs}
		
		print(embarkation_regions)
		
		disembarkation_regions={t[3]:(t[4],t[5]) for t in stpairs}
		
		print(disembarkation_regions)
		
		onramp_ids=[i[0]+offset for i in links if i[0]+offset not in [i[1]+offset for i in links]]
		offramp_ids=[i[1]+offset for i in links if i[1]+offset not in [i[0]+offset for i in links]]
		
		onramps={i:G.nodes[i]['coords'] for i in onramp_ids}
		offramps={i:G.nodes[i]['coords'] for i in offramp_ids}
		
		print(offramps)
# 		onramps={i:embarkation_regions[i] for i in embarkation_regions if i not in disembarkation_regions}
# 		offramps={i:disembarkation_regions[i] for i in disembarkation_regions if i not in embarkation_regions}
		
		def closestneighbor(latlong,comp_nodes):
			a_lat,a_long=latlong
			distances=[
				(
					sqrt(
						(a_lat-comp_nodes[n][0])**2 +
						(a_long-comp_nodes[n][1])**2
					),n
				)
				for n in comp_nodes
			]
			print(distances)
			closest_neighbor=sorted(distances, key=lambda tup: tup[0])[0][1]
			distance=min([i[0] for i in distances])
			return closest_neighbor,distance
		
		added_region_node_ids=[]
		# print(embarkation_regions)
		for er_id in embarkation_regions:
			
			lat,long=embarkation_regions[er_id]
			latlong=(lat,long)
			closest_onramp_id,closest_onramp_distance=closestneighbor(latlong,onramps)
			
			
			if er_id not in added_region_node_ids:
				G.add_node(er_id,coords=latlong)
				added_region_node_ids.append(er_id)
# 			print(er_id,closest_onramp_distance,closest_onramp_id,G.nodes[er_id]['coords'],G.nodes[closest_onramp_id]['coords'])

			G.add_edge(er_id,closest_onramp_id,weight=closest_onramp_distance,id=edgecount)
			adjacency_ids_lookup=dict_tree(er_id,closest_onramp_id,adjacency_ids_lookup,edgecount)	
			edgecount+=1
		
		for dr_id in disembarkation_regions:
			
			lat,long=disembarkation_regions[dr_id]
			latlong=(lat,long)
			print('-------')
			closest_offramp_id,closest_offramp_distance=closestneighbor(latlong,offramps)
			print(dr_id,closest_offramp_id,closest_offramp_distance)
			print('--------')
			if dr_id not in added_region_node_ids:
				G.add_node(dr_id,coords=latlong)
				added_region_node_ids.append(dr_id)
			
# 			print(closest_offramp_id,closest_offramp_distance,dr_id,G.nodes[closest_offramp_id]['coords'],G.nodes[dr_id]['coords'])
			
			G.add_edge(closest_offramp_id,dr_id,weight=closest_offramp_distance,id=edgecount)
			adjacency_ids_lookup=dict_tree(closest_offramp_id,dr_id,adjacency_ids_lookup,edgecount)
			edgecount+=1
		
		## then find the shortest paths for all abpairs, and generate the bezier curves as you go
		print("calculating shortest routes & making bezier curves")
		
		def calControlPoint_new(points, edge_ids, smoothing=0.15):
			#edge_ids = [i for i in range(len(points)-1)]
			A, B, C=points[:3]
			Controlx = B[0] + smoothing*(A[0]-C[0])
			Controly = B[1] + smoothing*(A[1]-C[1])
			result={}
			result[edge_ids[0]] = [[A, B], [[Controlx, Controly], [Controlx, Controly]]]
			for i in range(2, len(points)):
				if i == len(points)-1:
					start_point, mid_point, end_point = points[i-1], points[i], points[i]
				else:
					start_point, mid_point, end_point = points[i-1], points[i], points[i+1]
				next_Controlx1 = start_point[0]*2 - Controlx
				next_Controly1 = start_point[1]*2 - Controly
		
				next_Controlx2 = mid_point[0] + smoothing*(start_point[0] - end_point[0])
				next_Controly2 = mid_point[1] + smoothing*(start_point[1] - end_point[1])
		
				#result.append([[next_Controlx1, next_Controly1], [next_Controlx2, next_Controly2], mid_point])
				result[edge_ids[i-1]] = [[start_point, mid_point], [[next_Controlx1, next_Controly1], [next_Controlx2, next_Controly2]]]
				Controlx, Controly = next_Controlx2, next_Controly2
	
			return result
		
		routes={}
		
		ERs=ExportRegion.objects.all()
		
		for node in G.nodes:
			print(node,G.nodes[node]['coords'])
		for edge in G.edges:
			print(edge)
		
		for stpair in stpairs:
			route_edge_ids=[]
			s_id,s_latitude,s_longitude,t_id,t_latitude,t_longitude=stpair
			if float(0) not in [s_latitude,s_longitude,t_latitude,t_longitude]:
				try:
					sp=nx.shortest_path(G,s_id,t_id,'weight')
				except:
					sp=[s_id,t_id]
				
				if len(sp)<=2:
					selfloop=[(er.id,er.name) for er in ERs.filter(pk__in=[s_id,t_id])]
					print("self-loop:",selfloop)
					
# 					wpa=list(adjacency_ids_lookup[s_id].keys())[0]
# 					wpb=list(adjacency_ids_lookup[t_id].keys())[0]
# 					
# 					if wpa!=wpb and t_id not in (wpa,wpb) and s_id not in (wpa,wpb):
# 						sp=[s_id,wpa,wpb,t_id]
# 					else:
# 						sp=[s_id,wpa,t_id]
				
				print(sp)
				
				if len(sp)>2:
					c=0
					waypoints=[]
					try:
						for node_id in sp:
							node=G.nodes[node_id]
							latitude,longitude=node['coords']
							waypoints.append([float(latitude),float(longitude)])				
					
							if c!=0:
								route_edge_ids.append(adjacency_ids_lookup[sp[c-1]][node_id])
							c+=1
				
						route=calControlPoint_new(waypoints,route_edge_ids)

						if s_id not in routes:
							routes[s_id]={t_id:route}
						else:
							routes[s_id][t_id]=route

					except:
						bad_route=[(er.id,er.name) for er in ERs.filter(pk__in=[s_id,t_id])]
						print("self-loop:",bad_route)
				

			
			d=open(base_path+'diaspora_routes_curves.py','w')
			d.write("diaspora_route_curves="+str(routes))
			d.close()