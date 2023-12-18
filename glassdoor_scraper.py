# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 09:32:36 2020

author: Kenarapfaik
url: https://github.com/arapfaik/scraping-glassdoor-selenium
"""
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1120, 1000)
    
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="
    #url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.
        time.sleep(slp_time)
        job_buttons = driver.find_element(By.CSS_SELECTOR, "ul.JobsList_jobsList__Ey2Vo").find_elements(By.CSS_SELECTOR, "li")
        print(len(job_buttons))
        #Going through each job in this page
        # job_buttons = driver.find_elements_by_class_name("jl")  #jl for Job Listing. These are the buttons we're going to click.
        # job_buttons = driver.find_elements(By.CLASS_NAME, value='jl')  #jl for Job Listing. These are the buttons we're going to click.

        for i, job_button in enumerate(job_buttons):
            if i < len(jobs)-1: 
                continue
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            # job_button.click()  #You might 
            driver.execute_script("arguments[0].click();", job_button)
            time.sleep(1)
            loaded = False
            loop = 0
            while not loaded:
                if loop > 3:
                    break
                try:
                    show_more = driver.find_element(By.CSS_SELECTOR, value='div.JobDetails_showMoreWrapper__I6uBt').find_element(By.CSS_SELECTOR, value='button')
                    loaded = True
                except:
                    time.sleep(1)
                    loop += 1
            if loaded:
                driver.execute_script("arguments[0].click();", show_more)
            collected_successfully = False
            
            while not collected_successfully:
                print('trying')
                try:
                    company_name = driver.find_element(By.CSS_SELECTOR, "span.EmployerProfile_employerName__Xemli").text
                    location = driver.find_element(By.CSS_SELECTOR, value='div.JobDetails_location__MbnUM').text
                    job_title = driver.find_element(By.CSS_SELECTOR, value='div.JobDetails_jobTitle__Rw_gn').text
                    job_description = driver.find_element(By.CSS_SELECTOR, value='section.JobDetails_jobDetailsSection__PJz1h').find_elements(By.CSS_SELECTOR, value='div')[0].text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = job_button.find_element(By.CSS_SELECTOR, value='div.JobCard_salaryEstimate___m9kY').text

            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
            print(salary_estimate)
            
            try:
                # rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
                # rating = driver.find_element(By.XPATH, value='.//span[@class="rating"]')
                rating = driver.find_element(By.CSS_SELECTOR, value='div#rating-headline').text
                print(rating)
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."
            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                # print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            try:
                company_overview = driver.find_element(By.CSS_SELECTOR, value='div.JobDetails_companyOverviewGrid__CV62w')
                # size is child 0 of company_overview
                size = company_overview.find_elements(By.CSS_SELECTOR, value='div')[0].find_elements(By.CSS_SELECTOR, value='div')[0].text
                founded = company_overview.find_elements(By.CSS_SELECTOR, value='div')[2].find_elements(By.CSS_SELECTOR, value='div')[0].text
                type_of_ownership = company_overview.find_elements(By.CSS_SELECTOR, value='div')[4].find_elements(By.CSS_SELECTOR, value='div')[0].text
                industry = company_overview.find_elements(By.CSS_SELECTOR, value='div')[6].find_elements(By.CSS_SELECTOR, value='div')[0].text
                sector = company_overview.find_elements(By.CSS_SELECTOR, value='div')[8].find_elements(By.CSS_SELECTOR, value='div')[0].text
                revenue = company_overview.find_elements(By.CSS_SELECTOR, value='div')[10].find_elements(By.CSS_SELECTOR, value='div')[0].text

            except NoSuchElementException:
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1


                
            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue})
            
            
        #Clicking on the "next page" button
            
        try:
            # driver.find_element_by_xpath('.//li[@class="next"]//a').click()
            # driver.find_element(By.XPATH, value='.//li[@class="next"]//a')
            button = driver.find_element(By.CSS_SELECTOR, value='div.JobsList_buttonWrapper__haBp5').find_element(By.CSS_SELECTOR, value='button')
            driver.execute_script("arguments[0].click();", button)
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
