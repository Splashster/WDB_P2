#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()
#import requests


form_items = cgi.FieldStorage()
auth_checkbox = form_items.getvalue('auth_search')
title_checkbox = form_items.getvalue('title_con')
type_checkbox = form_items.getvalue('type_search')
abstract_checkbox = form_items.getvalue('abs_con')
author = form_items.getvalue('authorname')
title_content = form_items.getvalue('title_content')
search_type = form_items.getvalue('searchtype')
abstract_content = form_items.getvalue('abstract_content')
multiple_items = False
fullname = ""
#auth_checkbox = "on"
#author = "Frank G G"

def generateBaseXQuery():
	
	xpath = 'MedlineCitationSet//MedlineCitationi//Article['

	if auth_checkbox:
		multiple_items = True
		try:
			fullname = author.split()
			forename = fullname[0] + " " + fullname[1]
			lastname = fullname[2]
		except:
			forename = ""
			lastname = ""
		xpath += 'AuthorList/Author[LastName=' + lastname + ' and ForName=' + forename 
	
	if title_checkbox:
		search_items['Title_Contents'] = title_content
	if type_checkbox:
		search_items['Publication_Type'] = search_type  
	if abstract_checkbox:
		search_items['Abstract_Contents'] = abstract_content

	xpath += ']/ArticleTitle'

	query = 'htttp://admin:admin@localhost:8984/rest/medsamp2012?query=distinct-values(data('+xpath+'))'
	return xpath

art = generateBaseXQuery()
print """Content-type:text/html\r\n\r\n
<html>
<body>
<script>console.log("{0}");</script>
</body>
</html>
""".format(art)
