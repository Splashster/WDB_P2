#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()
import requests
import xml.etree.ElementTree as ET

form_items = cgi.FieldStorage()
auth_checkbox = form_items.getvalue('auth_search')
title_checkbox = form_items.getvalue('title_con')
type_checkbox = form_items.getvalue('type_search')
abstract_checkbox = form_items.getvalue('abs_con')
author = form_items.getvalue('authorname')
title_content = form_items.getvalue('title_content')
search_type = form_items.getvalue('searchtype')
abstract_content = form_items.getvalue('abstract_content')
responses = []
abstract_checkbox = "on"
abstract_content = "Duodenal"


def parseResponse(response, response_type):
	auth_list = []
	types_list = []
	title_list = []
	abs_list = []

	if response_type == 'baseX':
		responses = response.text.split("<ArticleTitle>")
		#print responses
		for items in responses:
			if items != "":
				first_slice = items.split("</ArticleTitle>")
				title = first_slice[0]
				print title
				second_slice = first_slice[1].split("<AuthorList")	
				tree = ET.fromstring(second_slice[0])
				#abstracts = second_slice[0].replace("<AbstractText>","").replace("\n","").split("</AbstractText>")
				for child in tree:
					abstract = child.text
					abs_list.append(abstract)
				print abs_list
				#print str(abstracts)
				third_slice =  second_slice[1].split("<PublicationTypeList>")
				third_slice[0] =  "<AuthorList" + third_slice[0]
				tree = ET.fromstring(third_slice[0])
				for child in tree:
					fullname = child.find("./ForeName").text + " " + child.find("./LastName").text
					auth_list.append(fullname)
				print auth_list
				
				fourth_slice = "<PublicationTypeList>" + third_slice[1]
				tree = ET.fromstring(fourth_slice)
				for child in tree:
					types_list.append(child.text)
				print types_list
				print "*****************************************************"
				auth_list = []
				types_list = []
				abs_list = []
		'''
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
		'''

def sendQuery(query, response_type):
	#print query
	response = requests.get(query)
	parseResponse(response, response_type)


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

		multiple_items = True
		xpath += "AuthorList/Author[LastName= '{0}' and ForeName='{1}']".format(lastname,forename)
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
			xpath += "contains(Abstract,'{0}')".format(abstract_content)
		else:
			multiple_items = True
			xpath += "contains(Abstract,'{0}')".format(abstract_content)

	xpath += "]"
	xpath += '/PublicationTypeList|' + xpath + '/AuthorList|' + xpath + '/ArticleTitle|' + xpath + '/Abstract'  	
	query = 'http://admin:admin@localhost:8984/rest/medsamp2012?query='+xpath+''
	sendQuery(query, 'baseX')
	
generateBaseXQuery()
print """Content-type:text/html\r\n\r\n
<html>
<body>
<script>console.log("{0}");</script>
</body>
</html>
""".format('s')
