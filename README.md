# MetOfficeSunshine
Python program to extract Sunshine Hours for various requested month and year for a specific UK region. 

main.py -u -r Scotland_W -y 2023 -m 7

Command Line Args:

-u: If stipulated, updates local cache file with Met Office data

-y: Year (as a 4 digit integer, defaults to current year)

-m: Month (as an integer, defaults to current month)

-r: Region (from a list of choices, default is Scotland_W)

If data is not available locally, reads data from Met Office web site, processes it, and holds data in a local cache file.