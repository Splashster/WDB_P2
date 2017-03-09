#!/usr/bin/python
import cgi
import requests

publication_type_mapping = {'0': 'Journal Article', '1': 'Book', '3': 'In a conference proceedings', '5': 'In a collection (part of a book but has its own title)', '10': 'Tech Report', '13': 'Unpublished', '16': 'Miscellaneous', '47': 'In a conference proceedings'}
publication_type_list = []

'''
Get all publication types from existdb document.
'''
existdb_response = requests.get('http://localhost:8080/exist/rest/db/acm-turing-awards/acm-turing-awards.xml?_query=distinct-values(//XML/RECORDS/RECORD/REFERENCE_TYPE)&_howmany=1000')


'''
Removing exist result tags that existdb sends back in response.
'''
existdb_pub_types = existdb_response.text.replace('<exist:value exist:type="xs:untypedAtomic">', "").replace('</exist:value>',"").split(">")
existdb_pub_types  = existdb_pub_types[1].split("<")
existdb_pub_types = existdb_pub_types[0].strip().replace("\n", ";").replace(" ", "").split(";")


for existdb_pub_type in existdb_pub_types:
	publication_type_list.append(publication_type_mapping[existdb_pub_type])


'''
Get all publication types from basex document.
'''
basex_response = requests.get('http://admin:admin@localhost:8984/rest/medsamp2012?query=distinct-values(data(//MedlineCitationSet//MedlineCitation//Article//PublicationTypeList//PublicationType))')

for basex_pub_type in basex_response.text.split("\n"):
	publication_type_list.append(str(basex_pub_type))

publication_type_list = list(set(publication_type_list))

'''
Create dropdown elements for each publication types.
All Duplicate publication types have been removed.
'''
options = " "
for i in sorted(publication_type_list):
	options += """<option value="%s">%s</option>\n"""%(i,i)
	

print """ Cotent-type:text/html\r\n\r\n
<html>
<body>
<form>
<fieldset style="width:30%; margin-left:35%;">
<label for="author_check" style="margin-right:10%;">
<input id="auth_search" type="checkbox"> Search by Author
</label>
Author's name: <input name="authorname" style="margin-left:2%;" type="text"><br> 
<label for="title_con" style="margin-right:12%;">
<input id="title_con" type="checkbox"> Title contains...
</label>
Content: <input name="title_content" style="margin-left:12.2%;" type="text"><br> 
<label for="search_type" style="margin-right:13.5%;">
<input id="type_search" type="checkbox"> Search by type
</label>
Type: <select style="margin-left:16.8%; width:32.7%;">
<option>Select Type</option>
{0}
</select>
<br> 
<label for="abstract_con" style="margin-right:6%;">
<input id="abs_con" type="checkbox"> Abstract contains...
</label>
Content: <input name="abstract_content" style="margin-left:12%;" type="text"><br><br>
<input type="submit" value="Submit" style="margin-left:40%;"> 
</fieldset>
</form>
</body>
</html>
""".format(options)

