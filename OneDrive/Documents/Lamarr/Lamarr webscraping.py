import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from urllib.parse import urljoin

# Initialize the base URL for the entry page and the number of pages to scrape
entry_page_url = "https://www.legalbites.in/topics/articles"
num_pages_to_scrape = 5
data = []

# Function to scrape content from the redirecting page
def scrape_content(redirect_url):
    response = requests.get(redirect_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content_element = soup.find('div', class_='entry-main-content dropcap')
        if content_element:
            return content_element.text.strip()
    return None

# Function to convert HTML table to Markdown
def html_table_to_markdown(html_table):
    df = pd.read_html(str(html_table))[0]
    markdown_table = df.to_markdown(index=False)
    return markdown_table

# Function to handle different page formats
def process_article(article):
    title_element = article.find('h3')
    
    # Check if title element exists
    if title_element:
        title = title_element.text.strip()

        # Find the link to the redirecting page within the title element
        redirect_link = title_element.find('a')['href']

        # Construct the full URL for the redirecting page
        full_redirect_url = urljoin(entry_page_url, redirect_link)

        # Scrape content from the redirecting page
        content = scrape_content(full_redirect_url)

        if content:
            # Convert HTML tables in content to Markdown
            content_soup = BeautifulSoup(content, 'html.parser')
            tables = content_soup.find_all('table')
            for table in tables:
                markdown_table = html_table_to_markdown(table)
                content = content.replace(str(table), markdown_table)

            data.append({
                'title': title,
                'content': content
            })

# Loop through the pages of the entry page
for page_num in range(1, num_pages_to_scrape + 1):
    page_url = f"{entry_page_url}/page/{page_num}/"
    response = requests.get(page_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')

        for article in articles:
            process_article(article)

# Save the data to a JSON file
with open(r'C:\Users\sheri\OneDrive\Documents\Lamarr\legalbites_articles.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"Scraped data from {num_pages_to_scrape} pages and saved to legalbites_articles.json.")




# import requests
# from bs4 import BeautifulSoup
# import json
# import pandas as pd
# from urllib.parse import urljoin

# # Initialize the base URL for the entry page and the number of pages to scrape
# entry_page_url = "https://www.legalbites.in/topics/articles"
# num_pages_to_scrape = 5
# data = []

# # Function to scrape content from the redirecting page
# def scrape_content(redirect_url):
#     response = requests.get(redirect_url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         content_element = soup.find('div', class_='entry-main-content dropcap')
#         if content_element:
#             return content_element.text.strip()
#     return None

# # Function to convert HTML table to Markdown
# def html_table_to_markdown(html_table):
#     df = pd.read_html(str(html_table))[0]
#     markdown_table = df.to_markdown(index=False)
#     return markdown_table

# # Loop through the pages of the entry page
# for page_num in range(1, num_pages_to_scrape + 1):
#     page_url = f"{entry_page_url}/page/{page_num}/"
#     response = requests.get(page_url)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         articles = soup.find_all('article')

#         for article in articles:
#             title_element = article.find('h3')
            
#             # Check if title element exists
#             if title_element:
#                 title = title_element.text.strip()

#                 # Find the link to the redirecting page within the title element
#                 redirect_link = title_element.find('a')['href']

#                 # Construct the full URL for the redirecting page
#                 full_redirect_url = urljoin(entry_page_url, redirect_link)

#                 # Scrape content from the redirecting page
#                 content = scrape_content(full_redirect_url)

#                 if content:
#                     # Convert HTML tables in content to Markdown
#                     content_soup = BeautifulSoup(content, 'html.parser')
#                     tables = content_soup.find_all('table')
#                     for table in tables:
#                         markdown_table = html_table_to_markdown(table)
#                         content = content.replace(str(table), markdown_table)

#                     data.append({
#                         'title': title,
#                         'content': content
#                     })

# # Save the data to a JSON file
# with open(r'C:\Users\sheri\OneDrive\Documents\Lamarr\legalbites_articles.json', 'w', encoding='utf-8') as json_file:
#     json.dump(data, json_file, ensure_ascii=False, indent=4)

# print(f"Scraped data from {num_pages_to_scrape} pages and saved to legalbites_articles.json.")


