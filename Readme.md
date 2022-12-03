# Airbnbot

Small selenium bot to scrap information from airbnb based on a given first page.

You can change the values in the first lines of the `scrap.py` script.

The result is written to an output file in a `json` format of the form:

```json
[
    {
        "url": "https://www.airbnb.com/rooms/123456789?adults=2&check_in=2022-12-04&check_out=2022-12-17&previous_page_section_name=1000",
        "name": "Awesome Apartment",
        "currency": "$",
        "price": 1234.0,
        "score": 4.99,
        "reviews": 99
    },
    ...
]
```

The `analyse.py` is just used to play with the resulting json.
