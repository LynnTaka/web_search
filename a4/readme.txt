Requirements:
1) To write this program, strictly follow the pseudocode shown below. Your frontier must include
at the beginning only the single URL https://www.cpp.edu/sci/computer-science/ (CS home page)
and from this page, search through all linked pages until the target page is found. Links might
appear with full or relative addresses, and your crawler needs to consider this. Any other types of
resources rather than HTML or SHTML can be discarded.
2) Stop criteria: when the crawler finds the "Permanent Faculty" heading on the page body.
3) Use the Python libraries urllib and BeautifulSoup, and PyMongo.
4) Use the MongoDB collection pages to persist pages’ HTML data as text.
procedure crawlerThread (frontier)
while not frontier.done() do
url <— frontier.nextURL()
html <— retrieveHTML(url)
storePage(url, html)
if target_page (html)
clear_frontier()
else
for each not visited url in parse (html) do
frontier.addURL(url)
end for
end while
end procedure
5. [15 points]. By using the data persisted in the previous question, write a Python program parser.py that
will read the CS faculty information, parse faculty members' name, title, office, phone, email, and
website, and persist this data in MongoDB – one document for each professor. If you were not able to
finish question 4 properly, you are allowed to include the "Permanent Faculty" page HTML data
directly in MongoDB, so that you can try to complete question 5. Otherwise, use the target page URL
to find the Permanent Faculty page in the database.
Requirements:
1) Use the Python libraries BeautifulSoup and PyMongo.
2) Use the MongoDB collection professors to persist professors’ data
