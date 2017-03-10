#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()
import requests
import xml.etree.ElementTree as ET
from lxml import etree

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
#abstract_checkbox = "on"
#abstract_content = "Photolytic"
type_checkbox = "on"
search_type = "Journal Article"
main_list = []
msg = ""


def parseResponse(response, response_type):
	auth_list = []
	types_list = []
	title_list = []
	abs_list = []
	parts_list = []
	count = 0
	item_count = 1 
	parser = etree.XMLParser(recover=True)

	if response_type == 'baseX':
		responses = response.text.split("<ArticleTitle>")
		#print tree
		#print etree.tostring(tree)
		#print responses
		for items in responses:
			tree = "<root>" + "<ArticleTitle>" + items + "</root>"
			#print tree
			tree = etree.fromstring(tree,parser)
			root = ET.fromstring(etree.tostring(tree))
			if items != "":
				if "</ArticleTitle>" in items:
					first_slice = items.split("</ArticleTitle>")
					title = first_slice[0]
				else:
					title = "NONE"
				#print title
				if "<Abstract>" in items:
					#second_slice = first_slice[1].split("<AuthorList")	
					#tree = ET.fromstring(second_slice[0])
									#print root[1][0].text
					for child in root.find('Abstract'):
						abstract = child.text
						abs_list.append(abstract)
						#printi abstract
					#print root.tag
				else:
					abs_list.append("NONE")
				#print abs_list
				#print str(abstracts)
				#third_slice =  second_slice[1].split("<PublicationTypeList>")
				#third_slice[0] =  "<AuthorList" + third_slice[0]
				#tree = ET.fromstring(third_slice[0])
				if "<AuthorList" in items:
					for child in root.find("AuthorList"):
						try:	
							fullname = child.find("./ForeName").text + " " +  child.find("./LastName").text
							auth_list.append(fullname)
							#print fullname
						except:
							pass
				#	print auth_list
				else:
					auth_list.append("NONE")
				if "<PublicationTypeList" in items:
				#fourth_slice = "<PublicationTypeList>" + third_slice[1]
				#tree = ET.fromstring(fourth_slice)
					for child in root.find("PublicationTypeList"):
						types_list.append(child.text)
					#print types_list
				else:
					types_list.append("NONE")
				parts_list.append(types_list)
				parts_list.append(auth_list)
				parts_list.append(str(title))
				parts_list.append(abs_list)
				main_list.append(parts_list)
				#print main_list
				#print "*****************************************************"
				auth_list = []
				types_list = []
				abs_list = []
				parts_list = []
				message = ""
				for item in main_list:
					for parts in item:
						if count == 0:
							for i in parts:
								message += 'ReferenceType: {0}<br>'.format(i.encode('utf-8'))
							count = 1
						elif count == 1:
							for i in parts:
								message += 'Authors: {0}<br>'.format(i.encode('utf-8'))
							count = 2
						elif count == 2:
							message += 'Title: {0}<br>'.format(parts.encode('utf-8'))
							count = 3
						elif count == 3:
							for i in parts:
								message += 'Abstract: {0}<br>'.format(i.encode('utf-8'))
							count = 0
					if len(main_list) > 1 and item_count < len(main_list):
						message+='*********************************************<br>'
						item_count +=1
	
				global msg 
				msg = message
def sendQuery(query, response_type):
	#print query
	response = requests.get(query)
	if response.text != "":
		parseResponse(response, response_type)
	else:
		global msg 
		msg = "NONE"
def generateBaseXQuery():
	
	xpath = 'MedlineCitationSet//MedlineCitation//Article['
	
	oneChecked = False
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

		oneChecked = True
		xpath += "AuthorList/Author[LastName= '{0}' and ForeName='{1}']".format(lastname,forename)
	if title_checkbox:
		if oneChecked:
			xpath += " and contains(ArticleTitle,'{0}')".format(title_content)
 		else:
			oneChecked = True
			xpath += "contains(ArticleTitle,'{0}')".format(title_content)
	if type_checkbox:
		if oneChecked:
			xpath += " and PublicationTypeList[PublicationType='{0}']".format(search_type)
		else:
			oneChecked = True
			xpath += "PublicationTypeList[PublicationType='{0}']".format(search_type)
	if abstract_checkbox:
		if oneChecked:
			xpath += " and contains(Abstract,'{0}')".format(abstract_content)
		else:
			oneChecked = True
			xpath += "contains(Abstract,'{0}')".format(abstract_content)
	
	if oneChecked: 
		xpath += "]"
		xpath += '/PublicationTypeList|' + xpath + '/AuthorList|' + xpath + '/ArticleTitle|' + xpath + '/Abstract'  	
		query = 'http://admin:admin@localhost:8984/rest/medsamp2012?query='+xpath+''
		sendQuery(query, 'baseX')
	else:
		global msg 
		msg = "NONE"		
generateBaseXQuery()
#print msg
#print main_list
print """Content-type:text/html\r\n\r\n
<html>
<body>
<script>console.log({0});</script>
</body>
</html>
""".format(msg)
#print msg
