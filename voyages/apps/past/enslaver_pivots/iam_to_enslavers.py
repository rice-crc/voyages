import mysql.connector
import time
import json
import re

d=open("dbcheckconf.json","r")
t=d.read()
d.close()
conf=json.loads(t)

cnx = mysql.connector.connect(**conf)
cursor = cnx.cursor()
role_id_dict={}

'''for the captain and owner tables we:'''
for role in [['captain','captain','captain'],['shipowner','owner','investor']]:
	
	'''pull the all the records (rowids and names)'''
	cursor.execute('select id,name from voyage_voyage'+role[0])
	enslavers=cursor.fetchall()
	'''... so now for each enslaver in each role table'''
	for enslaver in enslavers:
		id,name=enslaver
		'''we get the enslaver voyages (everything else comes out of that)'''
		cursor.execute('select voyage_id,'+role[1]+'_order from voyage_voyage'+role[0]+'connection where '+role[1]+'_id=%d' %id)
		voyage_ids=cursor.fetchall()
		voyage_order={i[0]:i[1] for i in voyage_ids}
		'''then we remove any non-AIM voyage ids'''
		voyage_ids_str=','.join([str(i[0]) for i in voyage_ids])
		cursor.execute('select voyage_id from voyage_voyage where dataset=1 and voyage_id in (%s)' %voyage_ids_str)
		iam_voyage_ids=cursor.fetchall()
		iam_voyage_ids=[i[0] for i in iam_voyage_ids]
		voyage_ids_str=','.join([str(i) for i in iam_voyage_ids])
		
		for v_id in set([i[0] for i in voyage_ids])-set(iam_voyage_ids):
			del(voyage_order[v_id])
		
		'''if there are no iam voyages, we pass'''
		if len(iam_voyage_ids)>0:
			'''first we get the associated voyages' least sparse year data'''
			q='select imp_arrival_at_port_of_dis FROM voyage_voyagedates where voyage_id in (%s)' %voyage_ids_str
			cursor.execute(q)
			arrival_year_strs=cursor.fetchall()
			arrival_years=[]
			
			'''pull the arrival years for all the iam voyages this person was associated with, and use it to determine their first and last active year'''
			for ays in arrival_year_strs:
				try:
					year=int(ays[0].split(',')[2])
					arrival_years.append(year)
				except:
					pass
			if len(arrival_years)>0:
				first_active_year=min(arrival_years)
				last_active_year=max(arrival_years)
			else:
				first_active_year,last_active_year=[None,None]
			'''for now we are not attaching location data directly to the enslaver but instead drawing that in through voyages (or enslavementrelations, which sometimes have locations, as in the case of sales) '''
			#get the voyages' least-sparse and most-likely enslaver-related location data
			#or ... don't? we'll always have that in the voyages they're connected to.
			#and we don't have to run these enslavers through the enslavementrelation table, because that's just for sub-groups of enslaved people on given voyages
			#q='select imp_principal_place_of_slave_purchase_id,imp_principal_port_slave_dis_id FROM voyage_voyageitinerary where voyage_id in (%s)' %voyage_ids_str
			#cursor.execute(q)
			#locations_raw=cursor.fetchall()
			#locations=[]
			#for l in locations_raw:
			#	for i in l:
			#		if i!=None:
			#			locations.append(i)'''
		
			#get the number of enslaved people (embarked) associated with that voyage
			q='SELECT sum(imp_total_num_slaves_embarked) FROM voyage_voyageslavesnumbers where voyage_id in (%s);' %voyage_ids_str
			cursor.execute(q)
			number_enslaved=cursor.fetchone()
			number_enslaved=number_enslaved[0]
			rolename=role[2]
		
			if rolename in role_id_dict:
				role_id=role_id_dict[rolename]
			else:
				role_id=None
				while role_id==None:
		
					q="select id from past_enslaverrole where role='%s'" %rolename
					cursor.execute(q)
					role_id=cursor.fetchone()
					if role_id==None:
						q="insert into past_enslaverrole (role) values ('%s')" %rolename
						cursor.execute(q)
						cnx.commit()
					else:
						role_id=role_id[0]
					
			#print(name,first_active_year,last_active_year,voyage_ids,locations,number_enslaved,rolename)
			
			'''make a unique text id for the enslaver based on the dataset (IAM), their role (owner or captain), and their id in the owner or captain table at the time of the export'''
			hash_id="_".join(["IAM",rolename,str(id)])
			
			'''now start pushing the values over to PAST enslaver tables'''
			cursor.execute('insert into past_enslaveridentity (principal_alias,first_active_year,last_active_year,number_enslaved,text_id) values (%s,%s,%s,%s,%s)', (name,first_active_year,last_active_year,number_enslaved,hash_id))
			cursor.execute("select max(id) from past_enslaveridentity")
			identity_id=cursor.fetchone()
			identity_id=identity_id[0]
			
			'''and create a 1:1 mapped alias -- with the same, new uniqueid -- duplicate info. to maintain integrity with our next import/update after mergeing'''
			cursor.execute('insert into past_enslaveralias (alias,identity_id,text_id) values (%s,%s,%s)',(name,identity_id,hash_id))
			cnx.commit()
			cursor.execute("select max(id) from past_enslaveralias")
			alias_id=cursor.fetchone()
			alias_id=alias_id[0]
			
			'''and connect these new enslaver entities back to their voyages'''
			for v_id in voyage_order:
				e_order=voyage_order[v_id]
				q="insert into past_enslavervoyageconnection (`role_id`,`order`,`enslaver_alias_id`,`voyage_id`) values (%d,%d,%d,%d)" %(role_id,e_order,alias_id,v_id)
				cursor.execute(q)
			cnx.commit()
			