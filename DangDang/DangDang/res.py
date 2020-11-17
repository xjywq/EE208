import re

url = "http://category.dangdang.com/pg2-cid4002378-a1%3A2040.html"
nurl = re.sub(".*cid", "", url)
print(nurl)