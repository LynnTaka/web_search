from bs4 import BeautifulSoup
from pymongo import MongoClient

def parse_faculty(soup):
    """
    :param soup: beautiful soup obj
    :return: list of professor info
    parse faculty info: name, title, office, phone, email, and website from html page
    """
    professor_data = []

    # loop through each faculty card
    for faculty in soup.find('section', {'id': 's0'}).find_all('div', {'class': 'clearfix'}):
        # if cant find name not a faculty card
        try:
            name = faculty.find('h2').get_text().strip()
        except Exception as e:
            continue

        # get text from paragraph and split
        text = faculty.find('p').get_text()
        parts = text.split(":")

        # extract title
        title = parts[1]
        title = title[1:].replace(' Office', '').strip()

        # extract office
        office = parts[2]
        office = office[1:].replace(' Phone', '').strip()

        # extract phone number
        phone = parts[3]
        phone = phone[1:].replace(' Email', '').strip()

        # extract email
        email = parts[4]
        email = email[1:].replace('Web', '').strip()

        # extract website
        website = parts[5]
        website = website[1:].strip()
        print(website)

        # append faculty data to list
        professor_data.append({
            "name": name,
            "title": title,
            "office": office,
            "phone": phone,
            "email": email,
            "website": website
        })

    return professor_data

def store_in_db(professor_data):
    """
    :param professor_data: list of professors data
    :return: none
    insert faculty information into mogodb
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["crawler_db"]
    professors_collection = db["professors"]
    professors_collection.insert_many(professor_data)

def get_permanent_faculty():
    """
    :return: html data
    get html data from permanent faculty page from mongodb
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["crawler_db"]
    collection = db["pages"]

    target_url = "https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"
    page_data = collection.find_one({"url": target_url})

    if page_data is None:
        print("Error: Permanent Faculty page HTML data not found in the database.")
        exit()
    return page_data


# run code
page_data = get_permanent_faculty()
html_content = page_data["html"]
soup = BeautifulSoup(html_content, 'html.parser')
data = parse_faculty(soup)
store_in_db(data)
print("Faculty information parsed and stored in MongoDB.")
