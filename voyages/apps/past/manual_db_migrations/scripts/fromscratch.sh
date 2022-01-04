mysql -u voyages -pvoyagesPAST\!Branch2021 -e "drop schema PAST;"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "create database PAST;"
mysql -u voyages -pvoyagesPAST\!Branch2021 PAST < ../data/voyages_python3_20211028.sql

#The below steps stand in for the django migrations I've suggested in models.py
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslaveralias add column text_id char(255)"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "create table PAST.past_enslaverrole (id int not null auto_increment primary key,role varchar(100) NOT NULL)"
#mysql -u voyages -pvoyagesPAST\!Branch2021 -e "CREATE TABLE PAST.past_enslaveridentityplaceconnection (id int NOT NULL AUTO_INCREMENT,place_id int,enslaver_id int,PRIMARY KEY (id),FOREIGN KEY (place_id) REFERENCES voyage_place (id),FOREIGN KEY (enslaver_id) REFERENCES past_enslaveridentity (id))"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslavervoyageconnection drop column role"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslavervoyageconnection add column role_id int"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslavervoyageconnection add foreign key (\`role_id\`) references past_enslaverrole(\`id\`)"

mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslaverinrelation drop column role"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslaverinrelation add column role_id int"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslaverinrelation add foreign key (\`role_id\`) references past_enslaverrole(\`id\`)"

mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslaveridentity add column first_active_year int;"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslaveridentity add column text_id char(255);"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslaveridentity add column last_active_year int;"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslaveridentity add column number_enslaved int;"

mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslaveridentity add column principal_location_id int;"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslaveridentity add foreign key (principal_location_id) references voyage_place(id);"

mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslaveralias add constraint unique(text_id)"


mysql -u voyages -pvoyagesPAST\!Branch2021 -e "CREATE TABLE PAST.past_enslavementrelationtype (id int NOT NULL AUTO_INCREMENT,relation_type char(255),PRIMARY KEY (id))"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslavementrelation drop column relation_type"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslavementrelation add column relation_type_id int"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslavementrelation add foreign key (relation_type_id) references past_enslavementrelationtype(id)"

#and this last group here corrects for the fact that past_enslavementrelation's primary key did not autoincrement
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "ALTER TABLE PAST.past_enslaverinrelation drop foreign key \`past_enslaverinrelat_transaction_id_a9604345_fk_past_ensl\`;"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "ALTER TABLE PAST.past_enslavedinrelation drop foreign key \`past_enslavedinrelat_transaction_id_28a692bb_fk_past_ensl\`;"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "ALTER TABLE PAST.past_enslavementrelation MODIFY id INT AUTO_INCREMENT;"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "ALTER TABLE PAST.past_enslavementrelation add column transaction_id INT;"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "ALTER TABLE PAST.past_enslavementrelation add constraint unique(transaction_id);"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "ALTER TABLE PAST.past_enslavedinrelation add foreign key (transaction_id) references past_enslavementrelation(id);"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "ALTER TABLE PAST.past_enslaverinrelation add foreign key (transaction_id) references past_enslavementrelation(id);"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "ALTER TABLE PAST.past_enslavedinrelation MODIFY id INT AUTO_INCREMENT;"
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "ALTER TABLE PAST.past_enslaverinrelation MODIFY id INT AUTO_INCREMENT;"

#need room for higher dollar amounts
mysql -u voyages -pvoyagesPAST\!Branch2021 -e "alter table PAST.past_enslavementrelation modify amount decimal(10,2);"

python iam_to_enslavers.py
python kinfolk_to_enslavers_sql.py