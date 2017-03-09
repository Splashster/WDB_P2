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
#auth_checkbox = "on"
#author = "Frank G G"

def generateBaseXQuery():
	
	xpath = 'MedlineCitationSet//MedlineCitation//Article['
	multiple_items = False

	if auth_checkbox:
		try:
			fullname = author.split()
			if len(fullname) == 3:
				forename = fullname[0] + " " + fullname[1]
				lastname = fullname[2]
			elif len(fullname) == 2:
				forename = fullname[0]
				lastname = fullname[1]
			elif len(fullname) == 1:
				forename = fullname[0]
				lastname = ""
		except:
			forename = ""
			lastname = ""

		xpath += "AuthorList/Author[LastName= '{0}' and ForeName='{1}']".format(lastname,forename) 
		multiple_items = True
	if title_checkbox:
		if multiple_items:
			xpath += " and contains(ArticleTitle,'{0}')".format(title_content)
		else:
			multiple_items = True
			xpath += "contains(ArticleTitle,'{0}')".format(title_content)
	if type_checkbox:
		if multiple_items:
			xpath += " and PublicationTypeList='{0}'".format(search_type)
		else:
			multiple_items = True
			xpath += "PublicationTypeList='{0}'".format(search_type)
	if abstract_checkbox:
		if multiple_items:
			xpath += " and contains(Abstract,'{0}')".format(abstract_content)
		else:
			multiple_items = True
			xpath += "contains(Abstract,'{0}')".format(abstract_content)

	xpath += ']'
	xpath += '/PublicationTypeList/PublicationType | ' + xpath + '/AuthorList/Author | ' + xpath + '/ArticleTitle | ' + xpath + '/Abstract/AbstractText'

	query = 'htttp://admin:admin@localhost:8984/rest/medsamp2012?query=distinct-values(data('+xpath+'))'
	return query

art = generateBaseXQuery()
print """Content-type:text/html\r\n\r\n
<html>
<body>
<script>console.log("{0}");</script>
</body>
</html>
""".format(art)
