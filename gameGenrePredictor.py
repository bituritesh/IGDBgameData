import os
import time
from asyncio import exceptions

from requests import post
from ratelimit import limits, sleep_and_retry

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


effective_writes_this_call = 0
all_api_responses_list = []


# Define the rate limit: 100 requests per minute (60 seconds)
@sleep_and_retry
@limits(calls=int(os.environ["IGDB_GAME_API_RATELIMIT_CALLS"]), period=int(os.environ["IGDB_GAME_API_RATELIMIT_CALLS"]))
def make_api_request(n: int):
    global effective_writes_this_call
    try:
        response = post(os.environ["IGDB_GAME_API_BASEURL"],
                        **{'headers': {'Client-ID': os.environ["IGDB_CLIENT_ID"],
                                       'Authorization': os.environ["IGDB_AUTHORIZATION_TOKEN"]},
                           'data': 'fields name,rating,rating_count,similar_games,storyline,summary,tags,themes,url,'
                                   'websites;where id>={0} & id < {1};sort id asc;limit 500;'.format(n, n+500)})
        response.raise_for_status()
        response = response.json()
        final_list = []
        
        for value in range(len(response)):
            msg = [response[value].get("id", "-"), response[value].get("name", "-"),
                   response[value].get("storyline", "-"), response[value].get("summary", "-"),
                   response[value].get("url", "-"),]
            if msg[2] == "-" and msg[3] == "-":
                continue
            else:
                middle_concatenated = msg[2] + msg[3]
                unwanted_chars = "-"  # Characters needed to be removed
                middle_concatenated = middle_concatenated.strip(unwanted_chars)
                msg[2] = middle_concatenated
                msg.pop(3)
                final_list.append(msg)
        effective_writes_this_call = effective_writes_this_call + len(final_list)
        print("final length of the list after eliminating the items neither has storyline and summary for range"
              " including {0} to {1} - ".format(n, n+500) + str(len(final_list)))
        print("*"*40)

        print("effective total writes until now = {}".format(effective_writes_this_call))
        return final_list, effective_writes_this_call
    
    except exceptions.HTTPError as err:
        print(f"Too Many Requests {err}")
        raise SystemExit(err)
    
    except ValueError as e:
        print(f"An error occurred: {e}")
        raise SystemExit(e)


def all_game_data(api_response) -> list:
    # global all_api_responses_list
    api_response_length = len(api_response)
    for j in range(0, api_response_length):
        all_api_responses_list.append(api_response[j])
    return all_api_responses_list


def game_data_for_id(start_id: int) -> tuple:
    for i in range(start_id, int(os.environ["IGDB_END_GAME_ID"]), 500):
        api_response, _ = make_api_request(i)
        all_game_data_list = all_game_data(api_response)
    return all_game_data_list, len(all_game_data_list)

#  ----------------------------------------------------------------------------------
#  Scraping IGDB website to get genres after reading url column from gsheet


def igdb_scrapper(url: str) -> list:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=2000)  # or p.firefox.launch()
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML,"
                       "like Gecko) Chrome/99.0.9999.999 Safari/537.36")
        page = context.new_page()
        # Navigate to the URL
        page.goto(url)
        # Wait for the page to load completely (you can adjust the time as needed)
        time.sleep(2)
        # Get the page content after rendering JavaScript
        html_content = page.content()
        # Close the browser
        context.close()
        browser.close()
        genre_list = igdb_html_parser(html_content)
        return genre_list
    

def igdb_html_parser(html_page_content: str) -> list:
    # Create a Beautiful Soup object
    soup = BeautifulSoup(html_page_content, 'html.parser')
    p_tags = soup.find_all('p')
    return list(p_tags)
