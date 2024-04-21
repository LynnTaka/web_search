import urllib.request
from bs4 import BeautifulSoup
from pymongo import MongoClient
from urllib.parse import urljoin


def retrieveHTML(url):
    """
    :param url: url to retrieve html content from
    :return: html content as bytes or nothing if there is an error
    retrieve html content from a url
    """
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except Exception as e:
        print("Error retrieving HTML:", e)
        return None

def parseHTML(url, html):
    """
    :param url: string of base url of html content
    :param html: html content as bytes to parse
    :return: list of urls extracted from the html content
    """
    if html is None:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    return [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]

def storePage(url, html):
    """
    :param url: string the url of the html content
    :param html: bytes of the html content to store
    :return:
    store html content into mongodb
    """
    if html is None:
        return
    # error handling
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["crawler_db"]
        collection = db["pages"]
        page_data = {"url": url, "html": html}
        collection.insert_one(page_data)
    except Exception as e:
        print("Error storing page:", e)

def target_page(html):
    """
    :param html: bytes of html content to check
    :return: bool true if target else false
    check if the html content contains the target
    """
    if html is None:
        return False
    soup = BeautifulSoup(html, 'html.parser')
    headings = soup.find_all(['h1'])
    for heading in headings:
        if heading.text.strip() == "Permanent Faculty":
            return True
    return False

def crawlerThread(frontier):
    """
    :param frontier: list of urls to crawl, expecting first to be base
    :return: none
    acts as a controller
    crawls through web pages until the target page is found
    """
    while frontier:
        print(frontier)
        url = frontier.pop(0)
        html = retrieveHTML(url)
        storePage(url, html)
        if target_page(html):
            print("Target page found:", url)
            frontier.clear()
        else:
            urls = parseHTML(url, html)
            for new_url in urls:
                if new_url not in frontier:
                    frontier.append(new_url)

# run code
frontier = ["https://www.cpp.edu/sci/computer-science/"]
crawlerThread(frontier)