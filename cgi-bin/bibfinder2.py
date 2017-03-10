#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()
import requests


form_items = cgi.FieldStorage()
auth_checkbox = form_items.getvalue('auth_search')
title_checkbox = form_items.getvalue('title_con')
type_checkbox = form_items.getvalue('type_search')
abstract_checkbox = form_items.getvalue('abs_con')
author = form_items.getvalue('authorname')
title_content = form_items.getvalue('title_content')
search_type = form_items.getvalue('searchtype')
abstract_content = form_items.getvalue('abstract_content')
auth_list = []
types_list = []
title_list = []
abs_list = []
author_xpath = ""
#auth_checkbox = "on"
#author = "Jih Ru Hwu"


def parseResponse(response, response_type, element):
	if response_type == 'baseX':
		if element == 'author':
			authors = response.text.split("\n")
			count = 0 
			for item in reversed(authors):
				if count == 1:
					fullname += " " + str(item)
					auth_list.append(fullname)
					fullname = ""
					count = 0
				else:
					fullname = str(item)
					count = 1
		elif element == 'title':
			titles = response.text.split("\n")
			for item in titles:
				title_list.append(str(item))
		elif element == 'type':
			types = response.text.split("\n")
			for item in types:
				type_list.append(str(item))
		elif element == 'abstract':
			abstracts = response.text.split("\n")
			for item in abstracts:
				abs_list.add(str(item))			


def sendQuery(query, element, response_type):
	response = requests.get(query)
	parseResponse(response, response_type, element)


def generateBaseXQuery():
	
	author_xpath = 'http://admin:admin@localhost:8984/rest/medsamp2012?query=data(MedlineCitationSet//MedlineCitation//Article['
	title_xpath = 'http://admin:admin@localhost:8984/rest/medsamp2012?query=data(MedlineCitationSet//MedlineCitation//Article['
	type_xpath = 'http://admin:admin@localhost:8984/rest/medsamp2012?query=data(MedlineCitationSet//MedlineCitation//Article['
	abstract_xpath = 'http://admin:admin@localhost:8984/rest/medsamp2012?query=data(MedlineCitationSet//MedlineCitation//Article['
		

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

		author_xpath += "AuthorList/Author[LastName= '{0}' and ForeName='{1}']]/AuthorList/Author/*[position()<3])".format(lastname,forename)
		sendQuery(author_xpath, 'author', 'baseX')
	if title_checkbox:
		title_xpath += "contains(ArticleTitle,'{0}')])".format(title_content)
		sendQuery(title_xpath, 'title', 'baseX')
	if type_checkbox:
		type_xpath += "PublicationTypeList='{0}'])".format(search_type)
		sendQuery(type_xpath, 'type', 'baseX')
	if abstract_checkbox:
		abstract_xpath += "contains(Abstract,'{0}')])".format(abstract_content)
		sendQuery(abstract_xpath, 'abstract', 'baseX')


generateBaseXQuery()
print """Content-type:text/html\r\n\r\n
<html>
<body>
<script>console.log("{0}");</script>
</body>
</html>
""".format(auth_list)
