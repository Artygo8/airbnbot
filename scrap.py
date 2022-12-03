import json
import re
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By

# You can change these values
OUTPUT_FILE = 'booking_rooms.json'
URL = 'https://www.airbnb.com/s/Paris--France/homes?refinement_paths%5B%5D=%2Fhomes&tab_id=home_tab&flexible_trip_dates%5B%5D=june&flexible_trip_dates%5B%5D=july&flexible_trip_dates%5B%5D=august&flexible_trip_lengths%5B%5D=weekend_trip&date_picker_type=calendar&query=Paris%2C%20France&place_id=ChIJD7fiBh9u5kcRYJSMaMOCCwQ&checkin=2020-06-05&checkout=2020-06-07&source=structured_search_input_header&search_type=autocomplete_click'
cookies = {'currency': 'EUR'}

# Start of the script
driver = webdriver.Firefox()
driver.add_cookie(cookies)

driver.get(URL)

results = []

re_stars = re.compile(r'(?P<score>[0-9].[0-9]+) \((?P<reviews>[0-9]+)\)')

MAX_PAGE = 100

for page in range(1, MAX_PAGE + 1):
    rooms = driver.find_elements(By.XPATH, "//div[@role='group']")
    for room in rooms:
        curr_result = {}

        # URL of the room
        links = room.find_elements(By.TAG_NAME, 'a')
        if not links:
            continue  # this is not a room
        href = links[0].get_attribute('href')
        curr_result['url'] = href

        # Name of the room
        number = href[:href.find('?')].split('/')[-1]
        name = room.find_elements(By.ID, f'title_{number}')
        if not name:
            continue
        curr_result['name'] = name[0].text

        # Price of the room
        spans = room.find_elements(By.TAG_NAME, 'span')
        total_price = set([span.text.strip().split()[0] for span in spans if 'total' in span.text])
        if len(total_price) > 1:
            print('WARNING: multiple total prices found', total_price, file=sys.stderr)
        total_price = total_price.pop()
        if total_price[0].isdigit():
            curr_result['currency'] = total_price[-1]
            total_price = total_price[:-1]
        else:
            curr_result['currency'] = total_price[0]
            total_price = total_price[1:]
        curr_result['price'] = float(''.join(total_price.split(',')))

        # Ratings of the room
        ratings = [re_stars.match(span.text) for span in spans]
        ratings = [rating for rating in ratings if rating is not None]
        score = reviews = 0
        if ratings:
            score = ratings[0].group('score')
            reviews = ratings[0].group('reviews')
        curr_result['score'] = float(score)
        curr_result['reviews'] = int(reviews)

        results.append(curr_result)

    next_page_link = driver.find_elements(By.XPATH, "//a[@aria-label='Next']")
    if next_page_link:
        print(f' > Go to page {page + 1}', file=sys.stderr)
        driver.get(next_page_link[0].get_attribute('href'))
    else:
        break

json.dump(results, open(OUTPUT_FILE, 'w'), indent=4)
print(f'All Done.\nResults written in {OUTPUT_FILE}', file=sys.stderr)
