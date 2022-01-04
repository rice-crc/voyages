import json
import pandas as pd
import re
import csv
import mysql.connector
import time

'''previously, i was transforming jennie's csv data into a gigantic dataframe and dictionaries
from which i was extracting the faceted relationships needed
and then dumping to json
and then in a second step importing from json to sql.
--this script goes straight from the csv to sql. it is more elegant, but still less so than i would like
and i don't think it can be made much prettier
'''

def cleanlist(l):
	l=[i for i in l if i not in [' ','']]
	return l
	
def getid(db_tablename,term_colname,val,createifnone=True,rowidname='id'):
	'''be careful, this assumes you are looking for a unique value -- and it will create one if it doesn't find it!'''
	q="select %s from %s where %s='%s'" %(rowidname,db_tablename,term_colname,val)
	cursor.execute(q)
	term_rowid=cursor.fetchone()
	if term_rowid != None:
		term_rowid=term_rowid[0]
	elif createifnone:
		q="insert into %s (%s) values ('%s')" %(db_tablename,term_colname,val)
		cursor.execute(q)
		cnx.commit()
		q="select max(id) from %s;" %(db_tablename)
		cursor.execute(q)
		term_rowid=cursor.fetchone()
		term_rowid=term_rowid[0]
	else:
		term_rowid=None
	return term_rowid

def create_or_update_enslaver(enslaver_name,number_enslaved_in_role,first_active_year_in_role,last_active_year_in_role,enslaver_location):
	'''this function updates an enslaver if they do exist, creates them if they don't'''
	'''check if the enslaver exists.'''
	global enslaver_autoincrement
	cursor.execute("select id,text_id,first_active_year,last_active_year,number_enslaved from past_enslaveridentity where principal_alias=%s and text_id like 'KIN_%'",(enslaver_name,))
	result=cursor.fetchone()
	
	if result is not None:
		'''if so, update the enslaver record with new information'''
		identity_id,text_id,first_active_year,last_active_year,number_enslaved = result
		cursor.execute("select id from past_enslaveralias where identity_id=%s",(identity_id,))
		result=cursor.fetchone()
		alias_id=result[0]
		if first_active_year is None:
			cursor.execute("update past_enslaveridentity set first_active_year=%s where id=%s",(first_active_year_in_role,identity_id,))
			cnx.commit()
		elif first_active_year_in_role < first_active_year:
			cursor.execute("update past_enslaveridentity set first_active_year=%s where id=%s",(first_active_year_in_role,identity_id,))
			cnx.commit()
		if last_active_year is None:
			cursor.execute("update past_enslaveridentity set last_active_year=%s where id=%s",(last_active_year_in_role,identity_id))
			cnx.commit()
		elif last_active_year_in_role > last_active_year:
			cursor.execute("update past_enslaveridentity set last_active_year=%s where id=%s",(last_active_year_in_role,identity_id))
			cnx.commit()
		cursor.execute("update past_enslaveridentity set number_enslaved=%s where id=%s",(number_enslaved+number_enslaved_in_role,identity_id))
		cnx.commit()
	else:
		'''if not, create the enslaver identity and alias records with the values from the current role.'''
		enslaver_autoincrement+=1
		location_slug=str(enslaver_location)
		textref_id="_".join(['KIN',location_slug,str(enslaver_autoincrement)])
		cursor.execute("insert into past_enslaveridentity (principal_alias,first_active_year,last_active_year,number_enslaved,text_id,principal_location_id) values (%s,%s,%s,%s,%s,%s)",
			(enslaver_name,first_active_year_in_role,last_active_year_in_role,number_enslaved_in_role,textref_id,enslaver_location))
		cnx.commit()
		cursor.execute("select max(id) from past_enslaveridentity")
		result=cursor.fetchone()
		identity_id=result[0]
		cursor.execute("insert into past_enslaveralias (alias,identity_id,text_id) values (%s,%s,%s);",(enslaver_name,identity_id,textref_id))
		cnx.commit()
		cursor.execute("select max(id) from past_enslaveralias")
		result=cursor.fetchone()
		alias_id=result[0]
	return identity_id,alias_id


def get_enslaverlocation(df,locationcol):
	
	default_value=999
	'''ENSLAVER LOCATION -- now pulling that from jennie's dedicated, role-based columns
	--and have made a column in enslaveridentity to capture it
	--default (unknown) location value is 999'''
	#enslaver_locations=list(set([voyages[i]['location'] for i in voyages]))
	if locationcol is not None:
		enslaver_locations=cleanlist(list(set(pd.unique(df[locationcol]))))
		if len(enslaver_locations)>0:
			enslaver_location=int(enslaver_locations[0])
		else:
			enslaver_location=default_value
	else:
		enslaver_location=default_value
	
	if enslaver_location is not None:
		enslaver_location_rowid=getid('voyage_place','value',enslaver_location,False)
	else:
		enslaver_location_rowid=None
	
	return(enslaver_location_rowid)


def sync_ownersshippersconsignors(enslaver_name,enslaver_role,namecol,locationcol):
	global enslaver_autoincrement
	global missing_enslaved_ids
	global missing_voyage_ids
	
	'''reduce the datafame to incidences of this enslaver name in this enslaver role'''
	entries=df[df[namecol]==enslaver_name]
	
	'''get the unique ids of the enslaved individuals & voyages listed in this context'''
	enslaved_ids=[int(i) for i in pd.unique(entries['Uniqueid'])]
	voyage_ids=pd.unique(entries['VoyageID'])
	
	#print(voyage_ids)
	
	'''gather up some minimal data on the voyages this enslaver name-role pair was associated with
	for the purposes of folding it into the enslaver relation'''
	voyages={int(i):{} for i in voyage_ids}
	voyage_ids_str=",".join([str(i) for i in voyage_ids])
	'''DATE: for now, using vessel_left_port will supply the date (alternative being first_dis_of_slaves)'''
	try:
		q="select voyage_id,vessel_left_port, first_dis_of_slaves from voyage_voyagedates where voyage_id in (%s)" %voyage_ids_str
		cursor.execute(q)
	except:
		print("ERROR -- NO VOYAGES ASSOCIATED WITH ENSLAVER: %s for ROLE: %s" %(enslaver_name,enslaver_role))
		return False
	results=cursor.fetchall()
	for r in results:
		voyage_id,vessel_left_port,first_dis_of_slaves=r
		voyages[voyage_id]['date']=vessel_left_port
	'''LOCATION (for the 'transportation' enslavement relation): for now, using imp_principal_place_of_slave_purchase_id
	(alternatives being: voyage_id,imp_principal_place_of_slave_purchase_id,first_landing_place_id,first_place_slave_purchase_id,int_first_port_dis_id)
	--this will gather up owners, shippers, and consignors in "transportation" relations'''
	cursor.execute("select voyage_id,imp_principal_place_of_slave_purchase_id from voyage_voyageitinerary where voyage_id in (%s)" %voyage_ids_str)
	results=cursor.fetchall()
	for r in results:
		voyage_id,imp_principal_place_of_slave_purchase_id=r
		voyages[voyage_id]['location']=imp_principal_place_of_slave_purchase_id
	
	enslaver_location=get_enslaverlocation(entries,locationcol)
	
	'''there are missing voyages. to write this script, i'm going to have to remove blanks (but log them)'''
	for v_id in list(voyages.keys()):
		if voyages[v_id]=={}:
			del(voyages[v_id])
			missing_voyage_ids.append(v_id)
	missing_voyage_ids=list(set(missing_voyage_ids))
	voyage_ids=[int(i) for i in list(voyages.keys())]
	
	active_dates=[voyages[v_id]['date'] for v_id in voyages]
	active_years=[int(i[-4:]) for i in active_dates if re.match('.*[0-9]{4}',i)]
	if len(active_years)>0:
		first_active_year_in_role=min(active_years)
		last_active_year_in_role=max(active_years)
	else:
		first_active_year_in_role,last_active_year_in_role=[None,None]

	
	'''calculate the number of people enslaved by this person in this capacity
	--in the future, obviously, we'd want to calculate this on the fly by accessing transaction and voyage data'''
	number_enslaved_in_role=len(enslaved_ids)
	
	identity_id,alias_id=create_or_update_enslaver(enslaver_name,number_enslaved_in_role,first_active_year_in_role,last_active_year_in_role,enslaver_location)
	
	'''I could be wrong, but I think the most efficient way to do non-transaction (buy/sell) enslavement relations
	is to use these enslavers'''
	
	'''because we have to group enslaved people by voyage *and* enslaver'''

	role_id=getid('past_enslaverrole','role',enslaver_role)
	relation_type_id=getid('past_enslavementrelationtype','relation_type','transportation')
	
	#print(entries)
	#print(voyage_ids)
	for v_id in voyage_ids:
		voyage_enslaved_ids=pd.unique(entries[entries['VoyageID']==v_id]['Uniqueid'])
		sources=sources_df[sources_df['Uniqueid']==voyage_enslaved_ids[0]]
		'''get the source -- there should only be one -- and unfortunately these are keyed against enslaved uniqueids in a separate sheet supplied by jennie to supplement a systemic issue with her sources. would be much easier and safer to be getting it from the main sheet, based on the voyage.'''
		source=sources.filter(['SourceA (original from jennie)','ShortRefA']).values.tolist()[0]
		if len(sources)!=1:
			print("SOURCES ERROR\n",enslaver_name,"\n",entries,"\n",sources)
			exit()
		sourceA,shortrefA=source
		sourceA_id=getid('voyage_voyagesources','short_ref',shortrefA,False)
		enslaved_ids=[int(i) for i in pd.unique(entries['Uniqueid'])]
		
		voyage_date=voyages[v_id]['date']
		voyage_location=voyages[v_id]['location']
		cursor.execute("insert into past_enslavementrelation (relation_type_id,date,text_ref,place_id,source_id,voyage_id) values (%s,%s,%s,%s,%s,%s)",
			(relation_type_id,voyage_date,sourceA,voyage_location,sourceA_id,int(v_id)))
		cnx.commit()
		cursor.execute("select max(id) from past_enslavementrelation")
		relation_id=cursor.fetchone()
		relation_id=relation_id[0]
		'''now link that relation to the enslaver'''
		cursor.execute("insert into past_enslaverinrelation (role_id,enslaver_alias_id,transaction_id) values (%s,%s,%s)",
			(role_id,alias_id,relation_id))
		cnx.commit()
		'''and now link each enslaved id here to this relation'''		
		
		#print(voyage_enslaved_ids)
		
		#print("BY VOYAGE",enslaver_name,relation_id,voyage_enslaved_ids)
		
		for e_id in voyage_enslaved_ids:
			try:
				cursor.execute("insert into past_enslavedinrelation (enslaved_id,transaction_id) values (%s,%s)",(int(e_id),relation_id))
				cnx.commit()
			except:
				missing_enslaved_ids.append(e_id)
		missing_enslaved_ids=list(set(missing_enslaved_ids))


def sync_buyersellers(enslaver_name,enslaver_role,namecol,locationcol):
	global enslaver_autoincrement
	global missing_enslaved_ids
	
	'''reduce the datafame to incidences of this enslaver name in this enslaver role'''
	entries=df[df[namecol]==enslaver_name]
	
	'''get the unique ids of the enslaved individuals & transactions listed in this context'''
	
	enslaved_ids=[int(i) for i in cleanlist(pd.unique(entries['Uniqueid']))]
	transaction_ids=[int(i) for i in cleanlist(pd.unique(entries['TransactionNumber']))]
	
	transaction_dates=cleanlist(pd.unique(entries['TransactionDate']))
	active_years=[int(i[-4:]) for i in transaction_dates if re.match('.*[0-9]{4}',i)]
	if len(active_years)>0:
		first_active_year_in_role=min(active_years)
		last_active_year_in_role=max(active_years)
	else:
		first_active_year_in_role,last_active_year_in_role=[None,None]
	
	enslaver_location=get_enslaverlocation(entries,locationcol)
	
	role_id=getid('past_enslaverrole','role',enslaver_role)
	
	number_enslaved_in_role=len(enslaved_ids)
		
	identity_id,alias_id=create_or_update_enslaver(enslaver_name,number_enslaved_in_role,first_active_year_in_role,last_active_year_in_role,enslaver_location)
	
	relationtype_id=getid('past_enslavementrelationtype','relation_type','transaction')
	
	'''in this case we can hook two different enslavers into the same relation
	specifically, because jennie has already grouped these buyer/seller/enslaved relations with a manual key
	'''
	
	for transaction_id in transaction_ids:
		cursor.execute("select id from past_enslavementrelation where transaction_id=%s",(transaction_id,))
		relation_id=cursor.fetchone()
		
		transaction_entries=entries[entries['TransactionNumber']==transaction_id]
		
		transaction_enslaved_ids=[int(i) for i in pd.unique(transaction_entries['Uniqueid'])]		
			
		if relation_id is None:

			x=pd.unique(transaction_entries['Uniqueid'])[0]
			sources=sources_df[sources_df['Uniqueid']==x]
			source=sources.filter(['SourceB','ShortRefB']).values.tolist()[0]
			if len(sources)!=1:
				print("SOURCES ERROR\n",enslaver_name,"\n",entries,"\n",sources)
				exit()
			sourceB,shortrefB=source
			sourceB_id=getid('voyage_voyagesources','short_ref',shortrefB,False)
			
			'''now i'm being a little fast & loose.
			assuming that we've only got one date and amount per transaction'''
			
			transaction_date=transaction_entries['TransactionDate'].values[0]
			
			transaction_location_id=transaction_entries['TransactionLocation'].values[0]
			
			transaction_location_rowid=getid('voyage_place','value',transaction_location_id,False)
			
			amount=transaction_entries['CaptivePrice'].values[0]
			
			cursor.execute("insert into past_enslavementrelation (relation_type_id,date,text_ref,place_id,source_id,transaction_id) values (%s,%s,%s,%s,%s,%s)",
			(relationtype_id,transaction_date,sourceB,transaction_location_rowid,sourceB_id,transaction_id))
			cnx.commit()
			cursor.execute("select max(id) from past_enslavementrelation")
			relation_id=cursor.fetchone()
		relation_id=relation_id[0]
		
		cursor.execute("insert into past_enslaverinrelation (role_id,enslaver_alias_id,transaction_id) values (%s,%s,%s)",
			(role_id,alias_id,relation_id))
		
		#print("BY TRANSACTION",enslaver_name,relation_id,enslaved_ids)
		
		for e_id in transaction_enslaved_ids:
			try:
				cursor.execute("insert into past_enslavedinrelation (enslaved_id,transaction_id) values (%s,%s)",(int(e_id),relation_id))
				cnx.commit()
			except:
				missing_enslaved_ids.append(e_id)

		missing_enslaved_ids=list(set(missing_enslaved_ids))


def sync_enslavementrelations(yada,yadda,yoda):	
	role_id=getid('past_enslaverrole','role',enslaver_role)
	relation_type_id=getid('past_enslavementrelationtype','relation_type','transportation')
	
	'''voyage enslavement relations should, for Jennie's import, be unique by voyage
	--again, this is based on the assumption that we can roll up owners shippers and consignors as sharing a transportation enslavement relation'''
	
	for v_id in voyage_ids:
		cursor.execute("select id from past_enslavementrelation where voyage_id=%s",(int(v_id),))
		relation_id=cursor.fetchone()
		
		'''check if relation exists, and if not, create it.'''
		
		if relation_id is None:
			x=pd.unique(entries[entries['VoyageID']==v_id]['Uniqueid'])[0]
			sources=sources_df[sources_df['Uniqueid']==x]
			'''get the source -- there should only be one -- and unfortunately these are keyed against enslaved uniqueids in a separate sheet supplied by jennie to supplement a systemic issue with her sources. would be much easier and safer to be getting it from the main sheet, based on the voyage.'''
			source=sources.filter(['SourceA (original from jennie)','ShortRefA']).values.tolist()[0]
			if len(sources)!=1:
				print("SOURCES ERROR\n",enslaver_name,"\n",entries,"\n",sources)
				exit()
			sourceA,shortrefA=source
			cursor.execute("select id from voyage_voyagesources where short_ref=%s",(shortrefA,))
			sourceA_id=cursor.fetchone()
			sourceA_id=sourceA_id[0]
			
			voyage_date=voyages[v_id]['date']
			voyage_location=voyages[v_id]['location']
			cursor.execute("insert into past_enslavementrelation (relation_type_id,date,text_ref,place_id,source_id,voyage_id) values (%s,%s,%s,%s,%s,%s)",
				(relation_type_id,voyage_date,sourceA,voyage_location,sourceA_id,int(v_id)))
			cnx.commit()
			cursor.execute("select max(id) from past_enslavementrelation")
			relation_id=cursor.fetchone()
		relation_id=relation_id[0]
		
		'''now link that relation to the enslaver'''
		cursor.execute("insert into past_enslaverinrelation (role_id,enslaver_alias_id,transaction_id) values (%s,%s,%s)",
			(role_id,alias_id,relation_id))

	#enslaver_locations=list(set([voyages[v_id]['location'] for v_id in voyages]))



'''connect to db'''
d=open("dbcheckconf.json","r")
t=d.read()
d.close()
conf=json.loads(t)
cnx = mysql.connector.connect(**conf)
cursor = cnx.cursor()

'''then load in the data from the csvs:'''
'''main sheet, and immediately isolate Jennies rows'''
df = pd.read_csv('../data/NewAO2Jennie5f_rev2.csv',quotechar='"',low_memory=False)
columns=['Uniqueid','AfricanName','AfricanName2','AfricanName3','ModernAfricanName','Certainty','Westernname','Gender','Age','Height','CaptiveStatus','SkinColor','VoyageID','Voyagestatus','Vesselfate','Captivefate','ShipName','Yearam','Mjbyptimp','Dateleftlastslavingport','Mjslptimp','Datelanded','AfricanLanguagegroup','Africancountry','SourceA','ShortrefA','SourceB','ShortrefB','SourceC','ShortrefC','LastKnownLocation','Lastknowndate','NameOwnerEmployer','OwnerEmployerLocation','OccupationOwnerEmployerBuyer','ShipperName','ShipperLocation','ConsignorName','ConsignorLocation','TransactionDate','CaptivePrice','Currency','TransactionNumber','SellerName','BuyerName','BuyerLocation','TransactionLocation','Notes','filter_$']
df= df[df['Uniqueid']>500000]

'''jennies cleaned sources, to be subbed in as we go.'''
sources_df = pd.read_csv('../data/sources CORRECTED.csv')
sources_columns=['Uniqueid','SourceA (original from jennie)','ShortRefA','SourceB','ShortRefB']

'''pull in all the enslaver names'''

df=df.fillna('')

owner_names=cleanlist(pd.unique(df['NameOwnerEmployer']))
shipper_names=cleanlist(pd.unique(df['ShipperName']))
consignor_names=cleanlist(pd.unique(df['ConsignorName']))
seller_names=cleanlist(pd.unique(df['SellerName']))
buyer_names=cleanlist(pd.unique(df['BuyerName']))



'''jennies kinfolk csv data has an interesting structure
because it's organized by unique enslaved people, that spreads the enslavers out across multiple rows and columns
specifically, some columns (like location and name) are bound to the role of the person'''
rolepairs_A=[
	[owner_names,'owner','NameOwnerEmployer','OwnerEmployerLocation'],
	[shipper_names,'shipper','ShipperName','ShipperLocation'],
	[consignor_names,'consignor','ConsignorName','ConsignorLocation'],
]

'''we need an enslaver autoincrement id as part of our unique key for them'''
enslaver_autoincrement=500000
missing_enslaved_ids=[]
missing_voyage_ids=[]

'''for rolepair in rolepairs_A:
	enslaver_names,role,namecol,locationcol=rolepair
	print("fetching enslavers by role:",role)
	for enslaver_name in enslaver_names:
		sync_ownersshippersconsignors(enslaver_name,role,namecol,locationcol)'''

rolepairs_B=[
	[buyer_names,'buyer','BuyerName','BuyerLocation'],
	[seller_names,'seller','SellerName',None]
]

for rolepair in rolepairs_B:
	enslaver_names,role,namecol,locationcol=rolepair
	print("fetching enslavers by role:",role)
	for enslaver_name in enslaver_names:
		sync_buyersellers(enslaver_name,role,namecol,locationcol)


for rolepair in rolepairs_A:
	enslaver_names,role,namecol,locationcol=rolepair
	print("fetching enslavers by role:",role)
	for enslaver_name in enslaver_names:
		sync_ownersshippersconsignors(enslaver_name,role,namecol,locationcol)

print("missing enslaved people uniqueids",missing_enslaved_ids)
print("missing voyage ids",missing_voyage_ids)

