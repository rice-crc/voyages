from voyages.apps.past.models import Enslaved,LanguageGroup,ModernCountry
from voyages.apps.common.utils import *
import csv
from django.core.management.base import BaseCommand
import os
import re
import json
from math import sqrt
from voyages.apps.past.models import Enslaved,LanguageGroup,ModernCountry
from voyages.apps.voyage.models import Place,Region,Voyage
import networkx as nx

class Command(BaseCommand):


	def handle(self, *args, **options):
		from voyages.apps.past.management.commands.ao_individuals_map import routeNodes,links
		
		for dataset in ['region','place']:
			print("--------",dataset,"----------")
			base_path='voyages/apps/past/static/'
			print('making a directed network graph of the oceanic waypoints from ao_individuals_map.py')
		
			#1. oceanic network
			#1a. add oceanic nodes with an id offset, since we're stitching a few graphs together
		
			oceanic_ids_offset=1000000000
			G=nx.DiGraph()
			n=0
		
			onramp_ids=[i[0]+oceanic_ids_offset for i in links if i[0]+oceanic_ids_offset not in [i[1]+oceanic_ids_offset for i in links]]
			offramp_ids=[i[1]+oceanic_ids_offset for i in links if i[1]+oceanic_ids_offset not in [i[0]+oceanic_ids_offset for i in links]]
		
			for node in routeNodes:
				latitude,longitude=node
				latlong=(float(latitude),float(longitude))
				n_id=n+oceanic_ids_offset
				tags=["oceanic_waypoint"]
				if n_id in onramp_ids:
					tags.append("onramp")
				if n_id in offramp_ids:
					tags.append("offramp")
				G.add_node(n_id,coords=latlong,tags=tags,type="oceanic waypoint",name=None)
				n+=1
		
			print("added",len(routeNodes),"oceanic waypoints to the network")
		
			#1b. then, add oceanic connections w/ euclidean distance
		
			def get_geo_edge_distance(s_id,t_id,G):
				s_lat,s_long=G.nodes[s_id]['coords']
				t_lat,t_long=G.nodes[t_id]['coords']
				distance=sqrt((t_lat-s_lat)**2+(t_long-s_long)**2)
				return(distance)
					
			e=0
			for link in links:
				s_id,t_id=link
				s_id+=oceanic_ids_offset
				t_id+=oceanic_ids_offset
			
				distance=get_geo_edge_distance(s_id,t_id,G)
			
				G.add_edge(s_id,t_id,distance=distance,id=e,tag="oceanic_leg",curve=True)
				e+=1
		
			print("added",len(links),"oceanic links to the network")
		
			#2. then, fetch and add other relevant geo nodes
		
			enslaved_individuals=Enslaved.objects.all()
			african_origins_individuals=enslaved_individuals.filter(enslaved_id__lt=500000)

			print("pulling & saving to enslaved_ids_mapping_dataframe.py all the enslaved individuals' mapping data")
		
			print("creating geo data for",len(african_origins_individuals),"enslaved individuals")
		
			##2a. enslaved origin point (via language group)
			
			african_origins_individuals.select_related('language_group')
			individuals_with_languagegroup=african_origins_individuals.filter(language_group__isnull=False)
			individuals_with_languagegroup=individuals_with_languagegroup.filter(language_group__latitude__isnull=False)
			individuals_with_languagegroup=individuals_with_languagegroup.filter(language_group__longitude__isnull=False)


			print("...",len(individuals_with_languagegroup),"have a valid language group")
		
			languagegroup_nodes=list(set(individuals_with_languagegroup.values_list(
				'language_group__id',
				'language_group__latitude',
				'language_group__longitude',
				'language_group__name'
			)))
		
			language_group_ids_offset=1000000
			for languagegroup_node in languagegroup_nodes:
				id,latitude,longitude,name=languagegroup_node
				G.add_node(id+language_group_ids_offset,coords=(float(latitude),float(longitude)),name=name,tags=["origin"],type="african origin",pk=id)
			print("added",len(languagegroup_nodes),"african origin nodes")
	
			##2b. final destinations
			african_origins_individuals.select_related('post_disembark_location')
			individuals_with_post_disembark_locations=african_origins_individuals.filter(post_disembark_location__isnull=False)
			individuals_with_post_disembark_locations=individuals_with_post_disembark_locations.filter(post_disembark_location__latitude__isnull=False)
			individuals_with_post_disembark_locations=individuals_with_post_disembark_locations.filter(post_disembark_location__longitude__isnull=False)
		
			###we'll use the spss codes for ids whenever possible
			###as these are in fact unique across the place, region, broadregion tables in voyages
			post_disembark_nodes=list(set(individuals_with_post_disembark_locations.values_list(
				'post_disembark_location__id',
				'post_disembark_location__value',
				'post_disembark_location__latitude',
				'post_disembark_location__longitude',
				'post_disembark_location__place'
			)))
		
			for post_disembark_node in post_disembark_nodes:
				pk,id,latitude,longitude,name=post_disembark_node
				G.add_node(
					id,
					coords=(float(latitude),float(longitude)),
					tags=["final_destination"],
					type="final destination",
					name=name,
					pk=pk
				)
		
			print("added",len(post_disembark_nodes),"post-disembark nodes")
		
			##2c. voyage embarkation & disembarkation ports
			if dataset=='region':
				african_origins_individuals.select_related(
					'voyage__voyage_itinerary__imp_principal_region_of_slave_purchase',
					'voyage__voyage_itinerary__imp_principal_region_slave_dis',
				)
				voyage_itineraries=list(set(african_origins_individuals.values_list(
					'voyage__voyage_itinerary__imp_principal_region_of_slave_purchase__value',
					'voyage__voyage_itinerary__imp_principal_region_slave_dis__value',
				)))
				regions=Region.objects.all()
				embarkation_regions=regions.filter(value__in=[ei[0] for ei in voyage_itineraries],latitude__isnull=False,longitude__isnull=False)
		
				disembarkation_regions=regions.filter(value__in=[ei[1] for ei in voyage_itineraries],latitude__isnull=False,longitude__isnull=False)
				node_sets = [
					{
						"geo_data":disembarkation_regions,
						"namefield":"region",
						"tags":["disembarkation_region"],
						"connect_to_tags":[("final_destination","source","all",False),("offramp","target","single",True)]
					},
					{
						"geo_data":embarkation_regions,
						"namefield":"region",
						"tags":["embarkation_region"],
						"connect_to_tags":[("origin","target","all",True),("onramp","source","single",True)]
					},
				]

			elif dataset=='place':
				african_origins_individuals.select_related(
					'voyage__voyage_itinerary__imp_principal_place_of_slave_purchase',
					'voyage__voyage_itinerary__imp_principal_port_slave_dis',
				)
				voyage_itineraries=list(set(african_origins_individuals.values_list(
					'voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__value',
					'voyage__voyage_itinerary__imp_principal_port_slave_dis__value',
				)))		
				places=Place.objects.all()
		
				embarkation_ports=places.filter(value__in=[ei[0] for ei in voyage_itineraries],latitude__isnull=False,longitude__isnull=False)
			
				disembarkation_ports=places.filter(value__in=[ei[1] for ei in voyage_itineraries],latitude__isnull=False,longitude__isnull=False)
				
				node_sets = [
					{
						"geo_data":disembarkation_ports,
						"namefield":"place",
						"tags":["disembarkation_port"],
						"connect_to_tags":[("final_destination","source","all",False),("offramp","target","single",True)]
					},
					{
						"geo_data":embarkation_ports,
						"namefield":"place",
						"tags":["embarkation_port"],
						"connect_to_tags":[("origin","target","all",True),("onramp","source","single",True)]
					},
				]
	
			#throwing in a conditional on the straight lines -- if the hop is too far, disallow the straightening
			threshold_for_straight=5

			def geteuclideandistance(Ay,Ax,By,Bx):
				distance=sqrt(
					(Ay-By)**2 +
					(Ax-Bx)**2
				)
				return distance
		
			def getclosestneighbor(latlong,comp_nodes):
				a_lat,a_long=latlong
				distances=[
					(geteuclideandistance(a_lat,a_long,comp_nodes[n][0],comp_nodes[n][1])
					,n
					)
					for n in comp_nodes
				]
				closest_neighbor=sorted(distances, key=lambda tup: tup[0])[0][1]
				distance=min([i[0] for i in distances])
				return closest_neighbor,distance
		
			for node_set in node_sets:
				tags=node_set['tags']
				connect_to_tags=node_set['connect_to_tags']
				namefield=node_set['namefield']
	# 			print(tags)
				for node in node_set['geo_data']:
					latitude=float(node.latitude)
					longitude=float(node.longitude)
					id=node.value
					name=node.__dict__[namefield]
					pk=node.id
				
					#print(id,name)
					G.add_node(id,name=name,coords=(latitude,longitude),tags=tags,type=','.join(tags),pk=pk)
					for connect_to_tag in connect_to_tags:
						tag,as_type,mode,curve=connect_to_tag
						#print(tag)
						comp_nodes={comp_node:G.nodes[comp_node]['coords']
							for comp_node in G.nodes
							if tag in G.nodes[comp_node]['tags']
						}
						if mode=="single":
							closest_neighbor,distance=getclosestneighbor((latitude,longitude),comp_nodes)
							if curve==False and distance > threshold_for_straight:
								curve=True
							if as_type=="source":
								G.add_edge(id,closest_neighbor,distance=distance,id=e,curve=curve,tag=tag)
							else:
								G.add_edge(closest_neighbor,id,distance=distance,id=e,curve=curve,tag=tag)
							e+=1
						else:
							lat,long=G.nodes[id]['coords']
						
							for comp_node in comp_nodes:
								comp_lat,comp_long=comp_nodes[comp_node]
								distance=geteuclideandistance(lat,long,comp_lat,comp_long)
								if curve==False and distance > threshold_for_straight:
									this_curve=True
								else:
									this_curve=curve
								if as_type=="source":
									G.add_edge(id,comp_node,id=e,distance=distance,curve=this_curve,tag=tag)
								else:
									G.add_edge(comp_node,id,id=e,distance=distance,curve=this_curve,tag=tag)
								e+=1
	# 							if connect_to_tag[0]=="origin":
	# 								print(id,G.nodes[id],comp_node,G.nodes[comp_node],as_type,distance,e,mode)
								
			print("finished building graph")
		
			#NOTE: 4 IS KIND OF A MAGIC NUMBER HERE -- BEYOND THAT WE HAVE TO DO SOME FUNKY HANDLING ON DISCONTINUOUS ROUTES
			#WITH 4 SLOTS, ALL OF THE FOLLOWING HOPS ARE CONTINUOUS: 4 ENTRIES-->3 HOPS; 3 ENTRIES --> MAX 2, MIN 1 HOP; 2 ENTRIES --> MAX 1 HOP
			if dataset=='region':
				all_individual_itineraries=list(set(african_origins_individuals.values_list(
					'language_group__id',
					'voyage__voyage_itinerary__imp_principal_region_of_slave_purchase__value',
					'voyage__voyage_itinerary__imp_principal_region_slave_dis__value',
					'post_disembark_location__value'
				)))
			elif dataset=='place':
				all_individual_itineraries=list(set(african_origins_individuals.values_list(
					'language_group__id',
					'voyage__voyage_itinerary__imp_principal_place_of_slave_purchase__value',
					'voyage__voyage_itinerary__imp_principal_port_slave_dis__value',
					'post_disembark_location__value'
				)))
		
			print("fetched",len(all_individual_itineraries),"itineraries")
			missing=[]
			def curvedab(A,B,C,ab_id,prev_controlXY,prev_wasstraight,result,smoothing=0.15):
				if prev_controlXY is None:
					#first edge
					ControlX = B[0] + smoothing*(A[0]-C[0])
					ControlY = B[1] + smoothing*(A[1]-C[1])
					Control=(ControlX,ControlY)
					result[ab_id]=[[A, B], [Control, Control]]
					return result,Control
				else:
					#last edge
					if C is None:
						C=B
					#all tother edges
					prev_ControlX,prev_ControlY=prev_controlXY
					if prev_wasstraight:
						A=prev_controlXY
					ControlX = A[0]*2 - prev_ControlX
					ControlY = A[1]*2 - prev_ControlY
					next_ControlX = B[0] + smoothing*(A[0]-C[0])
					next_ControlY = B[1] + smoothing*(A[1]-C[1])
					result[ab_id]=[[A, B],[[ControlX,ControlY],[next_ControlX,next_ControlY]]]
					return result,(next_ControlX,next_ControlY)
				
			def straightab(A,B,ab_id,result):
				midx=(A[0]+B[0])/2
				midy=(A[1]+B[1])/2
				Control=(midx,midy)
				result[ab_id]=[[A, B], [Control, Control]]
				isstraight=True
				return result,Control
		
			print("calculating shortest routes & making bezier curves")
		
			routes={}
		
			for itinerary in all_individual_itineraries:
				route={}
				routename="-".join([str(i) for i in itinerary])
			
				#let the below stitch together a path even if there are gaps, by removing nulls
			
				#but before we pull out the nulls, do 2 quick adjustments to accommodate for this data's intractability
				offset_itinerary=[i for i in itinerary]
				if offset_itinerary[0] is not None:
					offset_itinerary[0]+=language_group_ids_offset
				#this is a quick hack to get the embark/disembark self-loops back into the oceanic routes
				#really, it's about Sierra Leone
				#by finding the embarkation node's onramp neighbor, and inserting that into the itinerary
				#we force shortest_path to find a way back to disembark via the oceanic network
				## this works because we've already created placeholder edges:
				####for every origin to every embarkation
				####& for every disembarkation to every final destination
				####so that if we find that we know that a person originated at A, with a disembark of C and final of D, but embark B is unknown, then we just sub in the closest neighbor B
				####this could affect the displayed stats -- but it's either that or we don't draw a line
				embark,disembark=offset_itinerary[1:3]
				if embark==disembark and embark is not None:
					onramp=None
					for n in G.neighbors(embark):
						if 'onramp' in G.nodes[n]['tags']:
							onramp=n
					if onramp is not None:
						offset_itinerary.insert(2,onramp)
			
				offset_itinerary=[i for i in offset_itinerary if i is not None]
				legs=[]
				#print(offset_itinerary)
				for i in range(len(offset_itinerary)-1):
					a=offset_itinerary[i]
					b=offset_itinerary[i+1]
	# 				print(a,b,G.has_node(a),G.has_node(b))
					if a is not None and b is not None and G.has_node(a) and G.has_node(b):
						legs.append((a,b))
			
				shortest_path=[]

				#print(legs)
				for leg in legs:
					s_id,t_id=leg
	# 				print(s_id,t_id)
	# 				print(G.has_node(s_id),G.has_node(t_id))
					try:
						sp=nx.shortest_path(G,s_id,t_id,'weight')
					except:
						print("no path btw",s_id,t_id)
				
					if shortest_path==[]:
						shortest_path+=sp
					else:
						shortest_path+=sp[1:]
			
			
			
			
					
	# 			print("path--->",shortest_path)
				route_edge_ids=[]
				for i in range(len(shortest_path)-1):
					a=shortest_path[i]
					b=shortest_path[i+1]
	# 				print(a,b)
					e_id=G.edges[a,b]['id']
					route_edge_ids.append(e_id)
			
				if len(route_edge_ids)==1:
					edge_id=route_edge_ids[0]
					this_edge=[edge for edge in G.edges(data=True) if edge_id in route_edge_ids][0]
					a_id,b_id,data=this_edge
					a_coords=G.nodes[a_id]['coords']
					b_coords=G.nodes[b_id]['coords']
					route,control=straightab(a_coords,b_coords,edge_id,{})
				elif len(route_edge_ids)>1:
					edgepairs=[(route_edge_ids[i],route_edge_ids[i+1]) for i in range(len(route_edge_ids)-1)]
					prev_controlXY=None
					prev_wasstraight=False
					for edgepair in edgepairs:
						ab_id,bc_id=edgepair
						AB=[edge for edge in G.edges(data=True) if edge[2]['id']==ab_id][0]
						BC=[edge for edge in G.edges(data=True) if edge[2]['id']==bc_id][0]
						a_id,b_id,abdata=AB
						b_id,c_id,bcdata=BC
						A=G.nodes[a_id]['coords']
						B=G.nodes[b_id]['coords']
						C=G.nodes[c_id]['coords']
						ab_iscurved=abdata['curve']
						bc_iscurved=bcdata['curve']
						if ab_iscurved:
							route,prev_controlXY=curvedab(A,B,C,ab_id,prev_controlXY,prev_wasstraight,route)
							prev_wasstraight=False
						else:
							route,prev_controlXY=straightab(A,B,ab_id,route)
							prev_wasstraight=True
					if bc_iscurved:
						route,prev_controlXY=curvedab(B,C,None,bc_id,prev_controlXY,prev_wasstraight,route)
					else:
						route,prev_controlXY=straightab(B,C,bc_id,route)
				
				else:
					print("bad itinerary:",itinerary,offset_itinerary,legs,route_edge_ids,shortest_path)
			
				if route!={}:
					routes[routename]=route
		
			d=open(base_path+dataset+'_routes_curves.py','w')
			d.write(dataset+"_route_curves="+str(routes))
			d.close()
			
			edgetagvisibilitydict={
				"oceanic_leg":True,
				"offramp":True,
				"onramp":True,
				"origin":False,
				"final_destination":False
			}
					
			d=open(base_path+dataset+'_edge_ids.json','w')
			edge_dict={str(G.edges[id]['id']):edgetagvisibilitydict[G.edges[id]['tag']] for id in G.edges}
			d.write(json.dumps(edge_dict))
			d.close()
				
			geo_points={}
			for n in G.nodes:
				node=G.nodes[n]
				if 'oceanic_waypoint' not in node['tags']:				
					node_in_edges=G.in_edges(n)
					node_out_edges=G.out_edges(n)
				
					node_hidden_edges=[]
				
					for e_pair in node_in_edges:
						e=G.edges[e_pair]
						e_tag=e['tag']
						e_id=e['id']
# 						print(e_id,e_tag)
						if not edgetagvisibilitydict[e_tag]:
# 							print('hidden')
							node_hidden_edges.append(e_id)
				
					for e_pair in node_out_edges:
						e=G.edges[e_pair]
						e_tag=e['tag']
						e_id=e['id']
						if not edgetagvisibilitydict[e_tag]:
							node_hidden_edges.append(e_id)
					
					print(node_hidden_edges)
					
					coords=node['coords']
					name=node['name']
					pk=node['pk']
					geo_points[n]=(coords,name,pk,node_hidden_edges)
		
			d=open(base_path+dataset+'_routes_points.json','w')
			d.write(json.dumps(geo_points))
			d.close()
								
			
