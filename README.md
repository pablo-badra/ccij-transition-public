# ccij-transition
Transition from Lawlab to MyCamino CRM, including scraping, data transformations, and merges.

This project was started to scrape data from one CRM, transform data, and load it into a Saleforce CRM. 

I drafted a lot of the work in notebook format. Then I stored the most important funcitons in a package. 

scrape.ipynb - creates a list of records, creates a directory for each record, iterates over the list of records to download files for each record. extracts all compressed files. 

ccij_clean/create.py - creates the dataset by merging/transforming/cleaning files in the data directory. 


INSTRUCTIONS TO DOWNLOAD CASENOTE FILES

go to ccij-cdb.innovationlawlab.org/reports/parties

Not Null:
* party - aNum
* caseevent - caseaction
* caseevent - actiondate
* caseevent - created by 
* caseevent - comment

save as case_comments.csv

for transfers
* caseaction - mvdf
* same as above
* case comment contains, transfer, gsa, golden
save as transfer.csv, gsa.csv, golden.csv

INSTRUCTIONS TO DOWNLOAD CASE RECORDS
go to ccij-cdb.innovationlawlab.org/reports/parties

closed.csv
* caseregister casetype - not null
* caseregister open - not null
* caseregister closed - not null 

opened.csv
* caseregister casetype - not null
* caseregister open - not null
* caseregister closed - null 

casenote.csv
* caseaction = casenote
* caseeevent comment = not null
* caseevent created by = not null

caseevent - caseavtion = [@adelanto, @imperial, @mvdf, @gsa, @otaymesa, @yuba, @dublin]
adelanto.csv
imperial.csv
mvdf.csv
gsa.csv
otaymesa.csv
yuba.csv
dublin.csv

...

Not Null:

gender_id.csv
DOB.csv
aNum.csv
pob.csv
birth_country_id.csv
address.csv
city.csv
county.csv
state.csv
zip.csv
language_id.csv

race.csv
ethnicity.csv

phone.csv
phone_owner.csv


immigration_status_id.csv
initiated_date.csv

