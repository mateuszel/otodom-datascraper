# Otodom Data Scraper

Python scraper developed to collect Warsaw apartment listings for the
[Warsaw Apartment Price Prediction](https://github.com/mateuszel/warsaw-apartment-price-prediction)
project.

The scraper collects listing URLs, avoids duplicates between runs and supports
resuming detailed-data collection after an interruption.

> This project was developed against the Otodom website structure available at
> the time of development. Changes to the website may require updates to the
> parser.

## Features

- Load previously collected listings to avoid duplicates
- Collect new listing URLs from selected pages
- Retrieve detailed information for each listing
- Save progress and resume interrupted collection

## Main functions

### `load_old_offers(file)`

Loads previously collected listing identifiers from a text file and returns
them as a set.

### `get_new_offers(session, start_page, last_page, old_offers)`

Collects new listing URLs from the selected page range while excluding listings
already present in `old_offers`.

### `get_details(offers, session, output_file)`

Retrieves detailed information for the selected listings and saves the results
to `output_file`. The function stores progress so that collection can be
resumed after interruption.

Additional information about the output format is available in
[`details_docs.txt`](details_docs.txt).
