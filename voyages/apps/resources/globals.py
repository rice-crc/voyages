from .models import Country, AfricanName

names_search_strict_text = ['slave_name', 'slave_ship_name', 'slave_voyage_number', 'slave_date_arrived__gte',
                            'slave_date_arrived__lte', 'slave_age__gte', 'slave_age__lte', 'slave_height__gte',
                            'slave_height__lte']

names_search_checkboxes = ['search_slave_sex_boys', 'search_slave_sex_girls', 'search_slave_sex_men',
                           'search_slave_sex_women', 'search_slave_sex_males', 'search_slave_sex_females']

names_sort_fields = ['slave_name', 'slave_ship_name', "slave_country", "slave_embarkation_port",
                     "slave_disembarkation_port"]