# PlaystoreScraper
Gathers the list of unique email IDs and developer names, whose apps have had less than a threshold value of downloads. The progress is shown in realtime and also written to **emails.txt**

# Pre-requisites
1. [Geckodriver](https://github.com/mozilla/geckodriver/releases) (in PATH environment variable)
2. [Firefox](https://www.mozilla.org/en-US/firefox/new/)
3. Selenium (pip install selenium)

# Customizable Options
1. installThreshold = 500000
   - Tells the code to look for all apps which have the number of installs less than or equal to 500000
2. emailsNeeded = 200
   - Tells the code to stop once it has collected a list of 200 emails
3. scrollTimeout = 3
   - While loading pages and looking for more potential items on the page, waits for 3 seconds before scrolling down
4. openBrowser = True
   - If set to _True_, opens up a firefox browser and shows all progress of crawling, otherwise only shows the results in the console if set to _False_
