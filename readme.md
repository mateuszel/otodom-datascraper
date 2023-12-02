
### A simple and efficient data scraper for Otodom.pl website. It allows to easily get information about thousands of apartments listings in Warsaw. The code is working and has been tested.

## Short documentation
`def load_old_offers(file)`  
Function takes path to a text file as an argument and returns a set of all rows in that file. It's used to avoid duplicates in database.  

`def get_new_offers(session, start_page, last_page, old_offers)`  
Function takes as arguments a Requests session and a range of pages user wants to search through. It also takes a set of strings, which contains all listings that already exist in database. Returns a list of new listings' URL's.  

`def get_details(OFFERS, session, output_file)`  
Function takes a list of URL's, a Requests session and path to a text file as arguments. It fetches detailed from URL's contained in `OFFERS` and saves them in `output_file`. Since getting the detailed data about listings can cost a lot of time, the function saves index of the most recently checked listing, so it's possible to interrupt and then resume the process.  

Specific info about the scraped data itself can be found in `details_docs.txt`.  

