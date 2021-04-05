from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
import time
import os

###########################
installThreshold = 500000
emailsNeeded = 200
scrollTimeout = 3
openBrowser = True
###########################
visited = {}
visitedEmails = {}
emailList = []
playstoreUrl = 'https://play.google.com'

def scroll(driver, timeout):
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(timeout)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight

def initialize():
    global urlsList
    global collected
    collected = 0
    
    # Check for playstore.txt
    if not os.path.exists("playstore.txt") or os.path.getsize("playstore.txt") == 0:
        print("Starting browser in background..")
        print("Browser started!")
        driver.get(playstoreUrl + '/store/apps/new?hl=en')
        print("Scrolling..")
        scroll(driver,scrollTimeout)
        print("Scrolling completed!")
        html = driver.page_source
        print("Initializing with links..")
        try:
            f = open("playstore.txt",'a')
            for item in driver.find_elements_by_xpath("//a[@class='poRVub']"):
                f.write(item.get_attribute('href') + '\n')
                f.flush()
            print("Initial links obtained!")
        finally:
            f.close()
        print("Written to playstore.txt!")
    else:
        print("Already obtained initial list!")

    try:    
        f = open("playstore.txt",'r')
        urlsList = [line.strip() for line in f]
    finally:
        f.close()

    #Check for visited.txt
    if os.path.exists("visited.txt") and os.path.getsize("visited.txt") > 0:
        try:
            f = open("visited.txt")
            for line in f:
                visited[line.strip()] = True
        finally:
            f.close()

    #Check for emails.txt
    if os.path.exists("emails.txt") and os.path.getsize("emails.txt") > 0:
        for line in open("emails.txt"):
            collected += 1
            idx = line.find('-')
            email = line[idx+2:].strip()
            visitedEmails[email] = True
            emailList.append(line.strip())

    #Check for temp.txt
    if os.path.exists("temp.txt") and os.path.getsize("temp.txt") > 0:
        print("Previously collected temp file found!")
        for line in open("temp.txt"):
            if not line.strip() in visited:
               urlsList.append(line.strip())   
            

def getSimilar(driver):
    tempList = []
    try:
        f = open("temp.txt",'a')
        seeMore = driver.find_element_by_xpath("//a[@class='LkLjZd ScJHi U8Ww7d xjAeve nMZKrb  id-track-click ']")
        url = seeMore.get_attribute('href')
        driver.get(url)
        scroll(driver,scrollTimeout)
        for item in driver.find_elements_by_xpath("//a[@class='poRVub']"):
            url = item.get_attribute('href')
            id = url.strip()
            id = id[id.find("=")+1:]
            if not id in visited:
                f.write(url + '\n')
                f.flush()
                tempList.append(url)
        
    except:
        similar = driver.find_elements_by_xpath("//div[@class='WHE7ib mpg5gc']")
        for elements in similar:
            url = elements.find_element_by_xpath(".//c-wiz/div/div/div/div/div/a").get_attribute('href')
            id = url.strip()
            id = id[id.find("=")+1:]
            if not id in visited:
                f.write(url + '\n')
                f.flush()
                tempList.append(url)
    finally:
        f.close()
    return tempList

def process():
    global collected
    print("Total initial links -> " + str(len(urlsList)))
    global emailList
    try:
        f = open('emails.txt','a',encoding="utf-8")
        f2 = open('visited.txt','a')
        for url in urlsList:
            #print("Collected = " + str(collected))
            if collected >= emailsNeeded:
                print("Target reached!")
                break
            id = url.strip()
            id = id[id.find("=")+1:]
            if not id in visited:
                visited[id] = True
                f2.write(id+"\n")
                f2.flush()
                print("Processing " + id,end="")
                driver.get(url)
                try:
                    installsString = driver.find_element_by_xpath("//*[text()='Installs']/following-sibling::span").text
                    installs = 0
                    for d in installsString:
                        if d.isdigit():
                            installs = installs * 10 + int(d)
                    email = driver.find_element_by_xpath("//a[@class='hrTbp euBY6b']").text
                    developer = driver.find_element_by_xpath("//*[text()='Offered By']/following-sibling::span").text
                    print("..." + installsString)
                    if email in visitedEmails:
                        print("[-] Already encountered same developer")
                    elif installs <= installThreshold:
                        visitedEmails[email] = True
                        collected += 1
                        emailList.append(email)
                        devMail = developer + " - " + email
                        print("[+] " + devMail)
                        f.write(devMail + "\n")
                        f.flush()
                    urlsList.extend(getSimilar(driver))
                except:
                    print("... skipped")
                    
    finally:
        f2.close()
        f.close()
    print('Iterating list')
    for email in emailList:
        print(email)


def main():
    global driver
    options = FirefoxOptions()
    if not openBrowser:
        options.add_argument("--headless")
    try:
        driver = webdriver.Firefox(options=options)
        initialize()
        process()
    except KeyboardInterrupt:
        print("Program execution terminated abnormally with Ctrl+C!")
    finally:
        driver.quit()
    print("Done!")
    
if __name__ == "__main__":
    main()
