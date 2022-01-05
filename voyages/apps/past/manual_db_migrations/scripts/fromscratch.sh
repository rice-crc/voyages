docker exec -i voyages-mysql mysql -uroot -pvoyages -e "drop schema voyages_python3_enslavermigration_jan4;"
docker exec -i voyages-mysql mysql -uroot -pvoyages -e "create database voyages_python3_enslavermigration_jan4;"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 < ../data/voyages_newdb_20211222.sql

docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslaveralias add column text_id char(255)"


#The below steps stand in for the django migrations I've suggested in models.py
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "delete from past_enslaverinrelation;"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "delete from past_enslaveralias;"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "delete from past_enslaveridentity;"


docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslaveralias add column text_id char(255)"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "create table past_enslaverrole (id int not null auto_increment primary key,role varchar(100) NOT NULL)"
#docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "CREATE TABLE past_enslaveridentityplaceconnection (id int NOT NULL AUTO_INCREMENT,place_id int,enslaver_id int,PRIMARY KEY (id),FOREIGN KEY (place_id) REFERENCES voyage_place (id),FOREIGN KEY (enslaver_id) REFERENCES past_enslaveridentity (id))"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslavervoyageconnection drop column role"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslavervoyageconnection add column role_id int"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslavervoyageconnection add foreign key (\`role_id\`) references past_enslaverrole(\`id\`)"

docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslaverinrelation drop column role"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslaverinrelation add column role_id int"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslaverinrelation add foreign key (\`role_id\`) references past_enslaverrole(\`id\`)"

docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslaveridentity add column first_active_year int;"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslaveridentity add column text_id char(255);"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslaveridentity add column last_active_year int;"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslaveridentity add column number_enslaved int;"

docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslaveridentity add column principal_location_id int;"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslaveridentity add foreign key (principal_location_id) references voyage_place(id);"

docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslaveralias add constraint unique(text_id)"


docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "CREATE TABLE past_enslavementrelationtype (id int NOT NULL AUTO_INCREMENT,relation_type char(255),PRIMARY KEY (id))"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslavementrelation drop column relation_type"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslavementrelation add column relation_type_id int"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslavementrelation add foreign key (relation_type_id) references past_enslavementrelationtype(id)"

#and this last group here corrects for the fact that past_enslavementrelation's primary key did not autoincrement
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "ALTER TABLE past_enslaverinrelation drop foreign key \`past_enslaverinrelat_transaction_id_a9604345_fk_past_ensl\`;"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "ALTER TABLE past_enslavedinrelation drop foreign key \`past_enslavedinrelat_transaction_id_28a692bb_fk_past_ensl\`;"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "ALTER TABLE past_enslavementrelation MODIFY id INT AUTO_INCREMENT;"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "ALTER TABLE past_enslavementrelation add column transaction_id INT;"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "ALTER TABLE past_enslavementrelation add constraint unique(transaction_id);"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "ALTER TABLE past_enslavedinrelation add foreign key (transaction_id) references past_enslavementrelation(id);"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "ALTER TABLE past_enslaverinrelation add foreign key (transaction_id) references past_enslavementrelation(id);"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "ALTER TABLE past_enslavedinrelation MODIFY id INT AUTO_INCREMENT;"
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "ALTER TABLE past_enslaverinrelation MODIFY id INT AUTO_INCREMENT;"

#need room for higher dollar amounts
docker exec -i voyages-mysql mysql -uroot -pvoyages voyages_python3_enslavermigration_jan4 -e "alter table past_enslavementrelation modify amount decimal(10,2);"

python3 iam_to_enslavers.py
python3 kinfolk_to_enslavers_sql.py