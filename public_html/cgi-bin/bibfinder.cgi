#!/usr/bin/python
import cgi

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
<option value="temp">Temporary</option>
</select>
<br> 
<label for="abstract_con" style="margin-right:6%;">
<input id="abs_con" type="checkbox"> Abstract contains...
</label>
Content: <input name="abstract_content" style="margin-left:12%;" type="text"><br> 
</fieldset>
</form>
</body>
</html>
"""

