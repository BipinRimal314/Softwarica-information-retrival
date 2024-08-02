# import requests
# from bs4 import BeautifulSoup
# import json

# def fetch_page_content(url):
#     response = requests.get(url)
#     return BeautifulSoup(response.content, 'html.parser')

# def extract_publication_details(publication_url):
#     pub_soup = fetch_page_content(publication_url)

#     title = pub_soup.select_one('div.introduction div.rendering h1 span').get_text(strip=True)

#     authors = []
#     for author in pub_soup.select('p.relations.persons a.link.person'):
#         author_name = author.select_one('span').get_text(strip=True)
#         author_link = author['href']
#         authors.append({'name': author_name, 'profile_link': author_link})

#     author_without_link = pub_soup.select_one('p.relations.persons')
#     for content in author_without_link.contents:
#         if isinstance(content, str):
#             for name in content.split(','):
#                 if name.strip():
#                     authors.append({'name': name.strip()})

#     publication_year = pub_soup.select_one('tr.status span.date').get_text(strip=True)

#     return {
#         'title': title,
#         'authors': authors,
#         'publication_year': publication_year,
#         'publication_link': publication_url
#     }

# def scrape_publications(start_url):
#     main_soup = fetch_page_content(start_url)
#     publications = []

#     for result in main_soup.select('li.list-result-item'):
#         publication_url = result.select_one('h3.title a')['href']
#         publication_details = extract_publication_details(publication_url)
#         publications.append(publication_details)

#     return publications

# def save_to_json(data, filename):
#     with open(filename, 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)

# if __name__ == "__main__":
#     start_url = "https://pureportal.coventry.ac.uk/en/organisations/eec-school-of-computing-mathematics-and-data-sciences-cmds/publications/"
#     publications_data = scrape_publications(start_url)
#     save_to_json(publications_data, 'research_publications.json')
#     print("Data has been saved to research_publications.json")


import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urlparse
import robotexclusionrulesparser

def fetch_page_content(url, delay=2):
    time.sleep(delay)  # Add delay between requests
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def extract_publication_details(publication_url, delay=2):
    pub_soup = fetch_page_content(publication_url, delay)
    title = pub_soup.select_one('div.introduction div.rendering h1 span').get_text(strip=True)

    authors = []
    for author in pub_soup.select('p.relations.persons a.link.person'):
        author_name = author.select_one('span').get_text(strip=True)
        author_link = author['href']
        authors.append({'name': author_name, 'profile_link': author_link})

    author_without_link = pub_soup.select_one('p.relations.persons')
    for content in author_without_link.contents:
        if isinstance(content, str):
            for name in content.split(','):
                if name.strip():
                    authors.append({'name': name.strip()})

    publication_year = pub_soup.select_one('tr.status span.date').get_text(strip=True)

    return {
        'title': title,
        'authors': authors,
        'publication_year': publication_year,
        'publication_link': publication_url
    }

def scrape_publications(start_url, delay=2):
    main_soup = fetch_page_content(start_url, delay)
    publications = []

    for result in main_soup.select('li.list-result-item'):
        publication_url = result.select_one('h3.title a')['href']
        publication_details = extract_publication_details(publication_url, delay)
        publications.append(publication_details)

    return publications

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def is_scraping_allowed(url):
    parsed_url = urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            rp = robotexclusionrulesparser.RobotFileParser()
            rp.parse(response.text)
            return rp.can_fetch("*", url)
        else:
            return True  # Assume allowed if no robots.txt is found
    except Exception as e:
        print(f"Error fetching robots.txt: {e}")
        return False  # Assume disallowed if error occurs

if __name__ == "__main__":
    start_url = "https://pureportal.coventry.ac.uk/en/organisations/eec-school-of-computing-mathematics-and-data-sciences-cmds/publications/"
    if is_scraping_allowed(start_url):
        publications_data = scrape_publications(start_url)
        save_to_json(publications_data, 'research_publications.json')
        print("Data has been saved to research_publications.json")
    else:
        print("Scraping is not allowed by the site's robots.txt")
