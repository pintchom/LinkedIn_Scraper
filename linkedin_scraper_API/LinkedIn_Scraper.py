#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import time
import json
import sys
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


# In[2]:


def login(driver):  # Thanks to someone code at Tract
    # personal linkedin login code
    # create a seperate login file and keep credentials
    login = open("/Users/maxpintchouk/Code/linkedIn_scraper_tract/linkedin_scraper_API/logins.txt")
    line = login.readlines()

    email = line[0].strip()
    password = line[1]
    driver.get("https://www.linkedin.com/login")
    time.sleep(1)

    em = driver.find_element(by=By.ID, value="username")
    em.send_keys(email)
    pswrd = driver.find_element(by=By.ID, value="password")
    pswrd.send_keys(password)
    loginButton = driver.find_element(
        by=By.XPATH, value="//*[@id=\"organic-div\"]/form/div[3]/button")
    loginButton.click()
    time.sleep(3)
    #input("Please solve the CAPTCHA and press Enter to resume...")
    return


# In[3]:


def scrape_topCard(section):
    name = section.find(
        "h1", {"class": "text-heading-xlarge"}).text.strip()  # subject name
    # subject title description
    title = section.find("div", {"class": "text-body-medium"}).text.strip()
    location = section.find_all(
        "span", {"class": "text-body-small"})[-1].text.strip()  # Subject location

    return name, title, location


# In[4]:


def scrape_about(section):
    about = section.find_all(
        "span", {"class": "visually-hidden"})[-1].text.strip()

    return about


# In[5]:


def scrape_experience(section, driver):
    all_exp = []

    def get_text(exps):
        all_exp = []
        for exp in exps:
            exp_cur = []
            for part in exp.find_all("span", {"class": "visually-hidden"}):
                if part.find("strong"):  # ignore Skills part
                    continue
                if len(part.text.strip()) != 0:
                    exp_cur.append(part.text.strip())
            
            # extract the company url from the current experience
            company_url = exp.find("a", {"class": "optional-action-target-wrapper"}).get('href')
            # apply the function to extract the overview
            overview = get_company(company_url)
            # append the overview to current experience
            exp_cur.append(overview.strip())
            
            for part in exp.find_all("a", {"class": "optional-action-target-wrapper"}):
                if len(part.text.strip()) != 0:
                    exp_cur.append(part.text.strip())
            all_exp.append(exp_cur)

        return all_exp
    
    # given a company url, extract the overview of the company
    def get_company(url):
        driver.get(url)
        curr_url = driver.current_url
        split_url = curr_url.split("/")
        # if the company is listed in LinkedIn

        # MY SLIGHT EDIT, original code assumes every company has an overview. 
        overview = "No Company Overview Available."
        if "company" in split_url:
            company_index = split_url.index("company")
            company_name = str(split_url[company_index + 1])
            about_url = "https://www.linkedin.com/company/" + company_name + "/about/"
            driver.get(about_url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            try:
                overview = soup.find("p", {"class": "break-words white-space-pre-wrap t-black--light text-body-medium"}).text
            except:
                overview = "No Company Overview Available."
            print(overview)
            #if soup.find("p", {"class": "break-words white-space-pre-wrap t-black--light text-body-medium"}):
                #overview = soup.find("p", {"class": "break-words white-space-pre-wrap t-black--light text-body-medium"}).text
        return overview
    
        #ORIGNAL CODE GIVEN TO ME
        #if "company" in split_url:
        #    company_index = split_url.index("company")
        #    company_name = str(split_url[company_index + 1])
         #   about_url = "https://www.linkedin.com/company/" + company_name + "/about/"
        #    driver.get(about_url)
        #    soup = BeautifulSoup(driver.page_source, 'html.parser')
        #    overview = soup.find("p", {"class": "break-words white-space-pre-wrap t-black--light text-body-medium"}).text
        #else:
        #    overview = "N/A"
        #return overview


    if section.find("div", {"class": "pvs-list__footer-wrapper"}):
        temp_sec = section.find("div", {"class": "pvs-list__footer-wrapper"})
        exp_link = temp_sec.find("a", href=True)["href"]
        driver.get(exp_link)
        time.sleep(3)
        soup_exp = BeautifulSoup(driver.page_source, 'html.parser')
        exps = soup_exp.find_all("div", {"class": "pvs-entity--padded"})
        all_exp = get_text(exps)
    else:
        exps = section.find_all("div", {"class": "pvs-entity--padded"})
        all_exp = get_text(exps)

    return all_exp


# In[6]:


def scrape_education(section):
    all_edus = []
    edus = section.find_all("div", {"class": "pvs-entity"})
    for edu in edus:
        edu_cur = []
        for part in edu.find_all("span", {"class": "visually-hidden"}):
            if part.find("strong"):  # ignore Skills part
                continue
            edu_cur.append(part.text.strip())
        all_edus.append(edu_cur)

    return all_edus


# In[7]:


def scrape_recommedation(section, driver):
    all_recs = []

    def get_text(recs):
        all_recs = []
        for rec in recs:
            rec_cur = []
            for part in rec.find_all("span", {"class": "visually-hidden"}):
                rec_cur.append(part.text.strip())
            link = rec.find("a", href=True)["href"]
            rec_cur.append(link)
            all_recs.append(rec_cur)

        return all_recs

    if section.find("div", {"class": "pvs-list__footer-wrapper"}):
        temp_sec = section.find("div", {"class": "pvs-list__footer-wrapper"})
        edu_link = temp_sec.find("a", href=True)["href"]
        driver.get(edu_link)
        time.sleep(3)
        soup_rec = BeautifulSoup(driver.page_source, 'html.parser')
        recs = soup_rec.find(
            "div", {"class": "pvs-list__container"}).find_all("div", {"class": "pvs-entity"})
        all_recs = get_text(recs)
    else:
        recs = section.find("div", {
                            "class": "pvs-list__outer-container"}).find_all("div", {"class": "pvs-entity"})
        all_recs = get_text(recs)

    return all_recs


# In[10]:

def main(userLink):

    # 2 lines below this are unneeded with new versions of selenium, makes it very complicated 
    # set up Chrome driver
    #path = os.getcwd()
    #driver_path = ChromeDriverManager(path=path).install()
    driver = webdriver.Chrome()
    login(driver)

    time.sleep(10) # Rate limited - allowing time for manual captcha solving 
    #url = sys.argv[-1]  # get profile url from node.js
    #print(url)
    #urls = [url.get_attribute('href') for url in driver.find_elements(By.TAG_NAME, 'a')]
    #linkedin_urls = [url.startswith("https://www.linkedin.com/in/") for url in urls]
    #print(linkedin_urls)
    #idx = np.where(linkedin_urls)[0][0]
    #url = str(urls[idx])

    #^none of this needed since URL provided in frontend

    url = userLink
    driver.get(url)

    #When frontend done -- change url code after logging in accessing url from written frontend url . Simply need to write url to file and read line[0] and make url = link provided 
    '''
    url = open("/Users/maxpintchouk/Code/linkedIn_scraper_tract/links.txt")
    driver.get(url)
    '''

    time.sleep(1)
    # Now using beautiful soup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    dic = {"Linkedin": "", "Name": "", "Title": "", "Location": "", "About": "", "Experiences": [],
           "Education": [], "Recommendation": []}

    # scrape top card section
    topCard = soup.find("div", {"class": "mt2 relative"})
    dic["Linkedin"] = url
    name, title, location = scrape_topCard(topCard)
    print(name, title, location, dic["Linkedin"])
    dic["Name"] = name
    dic["Title"] = title
    dic["Location"] = location

    # scrape other sections
    sections = soup.find_all("section", {"class": "mt2"})
    for section in sections:
        if section.find("div", {"id": "about"}):
            about = ""
            about = scrape_about(section)
            dic["About"] = about
        elif section.find("div", {"id": "experience"}):
            exps = []
            exps = scrape_experience(section, driver)
            dic["Experiences"] = exps
        elif section.find("div", {"id": "education"}):
            edus = []
            edus = scrape_education(section)
            dic["Education"] = edus
        elif section.find("div", {"id": "recommendations"}):
            recs = []
            recs = scrape_recommedation(section, driver)
            dic["Recommendation"] = recs

    driver.close()

    # THIS IS THE JSON OBJECT NEEDED ON THE WEBSITE 
    json_object = json.dumps(dic, indent=4)
    print(json_object)

    # with open("sample.json", "w") as outfile:
    #     json.dump(dic, outfile)

    sys.stdout.flush()  # send data back to node.js

    return json_object


# In[11]:


#main("https://www.linkedin.com/in/maxpintchouk/")
#Not needed since main will be called in flask backend 

# In[ ]:




