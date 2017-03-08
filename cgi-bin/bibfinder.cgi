#!/usr/bin/python
import cgi
import requests

publication_type_list = []

response = requests.get('http://admin:admin@localhost:8984/rest/medsamp2012?query=distinct-values(data(//MedlineCitationSet//MedlineCitation//Article//PublicationTypeList//PublicationType))')

for pub_type in response.text.split("\n"):
	publication_type_list.append(str(pub_type))

#print publication_type_list

options = " "
for i in publication_type_list:
	options += """<option value="%s">%s</option>\n"""%(i,i)
	
#print options

print """ Cotent-type:text/html\r\n\r\n
<html>
<body>
<form>
<fieldset style="width:30%;">
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

