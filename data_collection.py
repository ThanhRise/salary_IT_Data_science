# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 11:47:44 2020

@author: Ken
"""

import glassdoor_scraper as gs 
import pandas as pd 

path = "C:/Users/admin/LearningIT/20231/DS/Project/ds_salary_proj/chromedriver.exe"

df = gs.get_jobs('machine learning',2000, False, path, 5)

df.to_csv('glassdoor_jobs2.csv', index = False)