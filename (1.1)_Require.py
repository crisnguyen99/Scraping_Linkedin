from ntpath import join
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import random
import csv
from datetime import datetime
from datetime import date
import pickle
import gspread

#authorize
from google.oauth2.service_account import Credentials

scopes = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file('lamwork-linkedin-connect.json',scopes=scopes)
gc = gspread.authorize(credentials)


def time_start():
    start_time = datetime.now().strftime("%H:%M:%S")
    print("Start crawling =", start_time)  

def time_end():
    end_time = datetime.now().strftime("%H:%M:%S")
    print('Finish entire program at',end_time )

def Pick_cookie_based_times_in_a_day():
    now = datetime.now()
    b=int(now.strftime('%H'))
    if b<12:
        cookies='Cookies_Linkedin2.pkl'
    elif b<18:
        cookies='Cookies_Linkedin1.pkl'
    else:
        cookies='Cookies_Linkedin3.pkl'

    return cookies

def Pick_cookie_by_order(number):
    cookies=f'Cookies_Linkedin{number}.pkl'
    return cookies


#open ChromeWindow
def create_driver(profile_number):
    directory_profile=f"user-data-dir=E:\KNOWLEDGE\Coding\Crawling JD Linkedin\profile_{profile_number}"
    # directory_profile=f"user-data-dir=E:\\KNOWLEDGE\\Coding\\Crawling JD Linkedin\\profile_{profile_number}"
    option = webdriver.ChromeOptions()
    option.add_argument("--disable-features=ChromeWhatsNewUI")
    option.add_argument(directory_profile)
    option.add_argument("window-size=900,900")
    return webdriver.Chrome(options=option) 

def login():
    try:
        driver.get('http://www.linkedin.com/login')
        sleep(random.uniform(2,3))
        
        password_field = driver.find_element_by_id('password')
        password_field.send_keys('ewq123!@#')
        sleep(random.uniform(1,2))
        password_field.send_keys(Keys.ENTER)
        sleep(random.uniform(4,5))

        password_field = driver.find_element_by_id('password')
        password_field.send_keys('thao12345')
        sleep(random.uniform(1,2))
        password_field.send_keys(Keys.ENTER)
        sleep(random.uniform(4,5))
        
    except:
        driver.get('http://www.linkedin.com/feed/')
#load cookie and run
def Load_cookie(cookie_x):
    cookies= pickle.load(open(cookie_x,'rb'))
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get('http://www.linkedin.com/login')
    sleep(random.uniform(2,3))
    try:
        password_field = driver.find_element_by_id('password')
        password_field.send_keys('ewq123!@#')
        sleep(random.uniform(1,2))
        password_field.send_keys(Keys.ENTER)
        sleep(random.uniform(4,5))

        password_field = driver.find_element_by_id('password')
        password_field.send_keys('thao12345')
        sleep(random.uniform(1,2))
        password_field.send_keys(Keys.ENTER)
        sleep(random.uniform(4,5))
    except:
        pass

#initial_link_page_search
def root_page_search(jobname):
    job_title_12= jobname.replace('&','%26').replace(',','').replace('/','').split()
    job_title_21= "%20".join(job_title_12)
    url_job_search =  f'https://www.linkedin.com/jobs/search/?f_TPR=r2592000&geoId=92000000&keywords={job_title_21}'

    return url_job_search
def Create_All_page_search(job_name,number_of_page):
    All_page_search=[]
    url_page_1= root_page_search(job_name) 
    All_page_search.append(url_page_1)
    for i in range(2,number_of_page+1):
        page_next= '&start='+str((i-1)*25)
        url_page_next = root_page_search(job_name) + page_next
        All_page_search.append(url_page_next)
    return All_page_search



#mấu chốt
def ClickXpath(i):
    try:
        x = driver.find_element_by_xpath(f'/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{i}]/div/div/div[1]/div[2]/div[1]/a')
    except:
        try:
            x = driver.find_element_by_xpath(f'/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{i}]/div/div/div/div[2]/div[1]/a')
        except:
            try:
                x = driver.find_element_by_xpath(f'/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{i}]/div/div/div[1]/div[2]/div[1]/a')
            except:
                x = driver.find_element_by_xpath(f'/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{i}]/div/div/div/div[2]/div[1]/a')


    x.click()
    

#lọc
def Get_info_from_ul (ul,detail_list):
    all_li = ul.find_all('li')
    all_li_list = [each_string.get_text().strip() for each_string in all_li]
    detail = '\n'.join(all_li_list)
    detail_list.append(detail)

def Get_headline_from_ul(ul,headline_list):
    try:
        headline=ul.find_previous('strong').get_text().strip()
        headline_list.append(headline)
    except:
        try:
            headline=ul.find_previous('p').get_text().strip()
            headline_list.append(headline)
        except:
            try:
                headline=ul.find_previous('br').get_text().strip()
                headline_list.append(headline)
            except:
                headline_list.append("")




def Sorting_2(lst):
    lst2 = sorted(lst, key=len)
    return lst2

def adjust_title_final(title_cua_job, job_name):
    title_cua_job_list=title_cua_job.split()
    split_line=12
    number_check=title_check_list[:split_line]
    rank_check=title_check_list[split_line:]

    title_final= job_name
    for word in title_cua_job_list:
        for key in rank_check:
            if key==word:
                if key not in job_name:
                    title_final= key +' '+job_name

        for key in number_check:
            if key==word:
                if key not in job_name:
                    title_final= job_name+' '+key
    
    return title_final

#long_run
def RunFile(job_list,output_file):
    clear_f= open(output_file,'w', encoding="ascii")
    clear_f.close()
    
    job_order=0

    for job_name in job_list:
        job_order+=1
        if job_order %2==0:
            back_ground= {"backgroundColor": {"red": 0.74,"green": 0.87,"blue": 0.4}}

        next=write_sheet.col_values(1)
        very_first_next=int(len(next)+1)
        next_arrow_to_write=int(len(next)+1)


        
        sleep(random.uniform(6,12))
        jobnamesplit= job_name.lower().replace('of','').replace('and','').replace('-','').replace('&','').replace(',','').replace('/','').split()
        check=[]
        y=['------']
        job_name_count=''
        #job_name_count=0
        
        job_count_limit=30000

        #set limitation for VIP job
        job_title_value=['Manager', 'Engineer' , 'Specialist', 'Analyst', 'Director', 'Developer','Lead','Engineering']
        job_title_value=[ x.lower() for x in job_title_value  ]

        if any(item in job_title_value for item in jobnamesplit):
            job_count_limit=45*10000
        else:
            job_count_limit=int(random.choice([20,20,25,24,30,35,43]))*10000





        #create a list included All page
        list_page_search=Create_All_page_search(job_name,8)

        for page_search in list_page_search:
            #check limit per page
            if len(job_name_count) >= job_count_limit:
                break 


            try:
                driver.get(page_search)
                sleep(random.uniform(1,1.5)) 

                #1 Scroll
                driver.set_window_size(300,900)
                
                total_height = int(driver.execute_script("return document.body.scrollHeight"))
                for i in range(0, total_height, int(random.uniform(5,10))):
                    driver.execute_script(f"window.scrollTo(0,{i})")
                sleep(random.uniform(1.5,2))  
                

                #2. find all job post
                job_title_result=[]
                job_company_name=[]
                Xpath_page_list=[]
                for x in range(1,26):
                    Xpath_page_list.append(x)

                page_source = BeautifulSoup(driver.page_source,"html.parser")
                profiles = page_source.find_all('a', class_ = 'disabled ember-view job-card-container__link job-card-list__title')
                profiles_comp_name = page_source.find_all('a', class_ = 'job-card-container__link job-card-container__company-name ember-view')

                for profile,comp_name in zip(profiles, profiles_comp_name):
                    a_profile_name= profile.get_text().strip()
                    job_title_result.append(a_profile_name)
                    a_company_name= comp_name.get_text().strip()
                    job_company_name.append(a_company_name)
                
                driver.set_window_size(2000,900)
                sleep(random.uniform(1,2)) 
                

                #3 click right job and get data
                for i in range(0,len(job_title_result)):
                    #check limit per Click
                    if len(job_name_count) >= job_count_limit:
                        break 

                    job_title_result_check=job_title_result[i].lower()
                    #check 
                    if all(item in job_title_result_check for item in jobnamesplit):
                        each_check = job_title_result_check+job_company_name[i]
                        if each_check not in check:
                            check.append(each_check)
                            try:
                                ClickXpath(i+1)
                                sleep(random.uniform(2,3))
                                page_source= BeautifulSoup(driver.page_source,"html.parser")
                                info_div= page_source.find("div",class_ = 'jobs-description__content jobs-description-content')
                                info_loc= info_div.find_all('ul')

                                info_title = page_source.find('h2', class_ ='t-24 t-bold')
                                title_cua_job= info_title.get_text().strip()



                                headline_list=[]
                                detail_list=[]
                                if len(info_loc)==1:
                                    ul_1 = info_div.find('ul')
                                    Get_headline_from_ul(ul_1,headline_list)  


                                    Get_info_from_ul(ul_1,detail_list)
  
                                elif len(info_loc) ==2:
                                
                                    ul_1 = info_div.find('ul')
                                    ul_2 = ul_1.find_next_sibling('ul')
                                    
                                    Get_headline_from_ul(ul_1,headline_list)
                                    Get_headline_from_ul(ul_2,headline_list)

                                    Get_info_from_ul(ul_1,detail_list)
                                    Get_info_from_ul(ul_2,detail_list)

                                elif len(info_loc) == 3:
                                    #1
                                    ul_1 = info_div.find('ul')
                                    ul_2 = ul_1.find_next_sibling('ul')
                                    ul_3 = ul_2.find_next_sibling('ul')

                                    Get_headline_from_ul(ul_1,headline_list)
                                    Get_headline_from_ul(ul_2,headline_list)
                                    Get_headline_from_ul(ul_3,headline_list)

                                    Get_info_from_ul(ul_1,detail_list)
                                    Get_info_from_ul(ul_2,detail_list)
                                    Get_info_from_ul(ul_3,detail_list)

                                elif len(info_loc) == 4:
                                    #1
                                    ul_1 = info_div.find('ul')
                                    ul_2 = ul_1.find_next_sibling('ul')
                                    ul_3 = ul_2.find_next_sibling('ul')
                                    ul_4 = ul_3.find_next_sibling('ul')

                                    Get_headline_from_ul(ul_1,headline_list)
                                    Get_headline_from_ul(ul_2,headline_list)
                                    Get_headline_from_ul(ul_3,headline_list)
                                    Get_headline_from_ul(ul_4,headline_list)

                                    Get_info_from_ul(ul_1,detail_list)
                                    Get_info_from_ul(ul_2,detail_list)
                                    Get_info_from_ul(ul_3,detail_list)
                                    Get_info_from_ul(ul_4,detail_list)

                                elif len(info_loc) ==5 :
                                    #1
                                    ul_1 = info_div.find('ul')
                                    ul_2 = ul_1.find_next_sibling('ul')
                                    ul_3 = ul_2.find_next_sibling('ul')
                                    ul_4 = ul_3.find_next_sibling('ul')
                                    ul_5 = ul_4.find_next_sibling('ul')

                                    Get_headline_from_ul(ul_1,headline_list)
                                    Get_headline_from_ul(ul_2,headline_list)
                                    Get_headline_from_ul(ul_3,headline_list)
                                    Get_headline_from_ul(ul_4,headline_list)
                                    Get_headline_from_ul(ul_5,headline_list)

                                    Get_info_from_ul(ul_1,detail_list)
                                    Get_info_from_ul(ul_2,detail_list)
                                    Get_info_from_ul(ul_3,detail_list)
                                    Get_info_from_ul(ul_4,detail_list)
                                    Get_info_from_ul(ul_5,detail_list)

                                elif len(info_loc) ==6:
                                    #1
                                    ul_1 = info_div.find('ul')
                                    ul_2 = ul_1.find_next_sibling('ul')
                                    ul_3 = ul_2.find_next_sibling('ul')
                                    ul_4 = ul_3.find_next_sibling('ul')
                                    ul_5 = ul_4.find_next_sibling('ul')
                                    ul_6 = ul_5.find_next_sibling('ul')
                                    

                                    Get_headline_from_ul(ul_1,headline_list)
                                    Get_headline_from_ul(ul_2,headline_list)
                                    Get_headline_from_ul(ul_3,headline_list)
                                    Get_headline_from_ul(ul_4,headline_list)
                                    Get_headline_from_ul(ul_5,headline_list)
                                    Get_headline_from_ul(ul_6,headline_list)
                                    

                                    Get_info_from_ul(ul_1,detail_list)
                                    Get_info_from_ul(ul_2,detail_list)
                                    Get_info_from_ul(ul_3,detail_list)
                                    Get_info_from_ul(ul_4,detail_list)
                                    Get_info_from_ul(ul_5,detail_list)
                                    Get_info_from_ul(ul_6,detail_list)
                                    
                                elif len(info_loc) ==7:
                                    #1
                                    ul_1 = info_div.find('ul')
                                    ul_2 = ul_1.find_next_sibling('ul')
                                    ul_3 = ul_2.find_next_sibling('ul')
                                    ul_4 = ul_3.find_next_sibling('ul')
                                    ul_5 = ul_4.find_next_sibling('ul')
                                    ul_6 = ul_5.find_next_sibling('ul')
                                    ul_7 = ul_6.find_next_sibling('ul')

                                    Get_headline_from_ul(ul_1,headline_list)
                                    Get_headline_from_ul(ul_2,headline_list)
                                    Get_headline_from_ul(ul_3,headline_list)
                                    Get_headline_from_ul(ul_4,headline_list)
                                    Get_headline_from_ul(ul_5,headline_list)
                                    Get_headline_from_ul(ul_6,headline_list)
                                    Get_headline_from_ul(ul_7,headline_list)

                                    Get_info_from_ul(ul_1,detail_list)
                                    Get_info_from_ul(ul_2,detail_list)
                                    Get_info_from_ul(ul_3,detail_list)
                                    Get_info_from_ul(ul_4,detail_list)
                                    Get_info_from_ul(ul_5,detail_list)
                                    Get_info_from_ul(ul_6,detail_list)
                                    Get_info_from_ul(ul_7,detail_list)
                               
                                elif len(info_loc) ==8:
                                    #1
                                    ul_1 = info_div.find('ul')
                                    ul_2 = ul_1.find_next_sibling('ul')
                                    ul_3 = ul_2.find_next_sibling('ul')
                                    ul_4 = ul_3.find_next_sibling('ul')
                                    ul_5 = ul_4.find_next_sibling('ul')
                                    ul_6 = ul_5.find_next_sibling('ul')
                                    ul_7 = ul_6.find_next_sibling('ul')
                                    ul_8 = ul_7.find_next_sibling('ul')
                                    

                                    Get_headline_from_ul(ul_1,headline_list)
                                    Get_headline_from_ul(ul_2,headline_list)
                                    Get_headline_from_ul(ul_3,headline_list)
                                    Get_headline_from_ul(ul_4,headline_list)
                                    Get_headline_from_ul(ul_5,headline_list)
                                    Get_headline_from_ul(ul_6,headline_list)
                                    Get_headline_from_ul(ul_7,headline_list)
                                    Get_headline_from_ul(ul_8,headline_list)
                                    

                                    Get_info_from_ul(ul_1,detail_list)
                                    Get_info_from_ul(ul_2,detail_list)
                                    Get_info_from_ul(ul_3,detail_list)
                                    Get_info_from_ul(ul_4,detail_list)
                                    Get_info_from_ul(ul_5,detail_list)
                                    Get_info_from_ul(ul_6,detail_list)
                                    Get_info_from_ul(ul_7,detail_list)
                                    Get_info_from_ul(ul_8,detail_list)
                                                                  
                                elif len(info_loc) > 8:
                                    #1
                                    ul_1 = info_div.find('ul')
                                    ul_2 = ul_1.find_next_sibling('ul')
                                    ul_3 = ul_2.find_next_sibling('ul')
                                    ul_4 = ul_3.find_next_sibling('ul')
                                    ul_5 = ul_4.find_next_sibling('ul')
                                    ul_6 = ul_5.find_next_sibling('ul')
                                    ul_7 = ul_6.find_next_sibling('ul')
                                    ul_8 = ul_7.find_next_sibling('ul')
                                    ul_9 = ul_8.find_next_sibling('ul')

                                    Get_headline_from_ul(ul_1,headline_list)
                                    Get_headline_from_ul(ul_2,headline_list)
                                    Get_headline_from_ul(ul_3,headline_list)
                                    Get_headline_from_ul(ul_4,headline_list)
                                    Get_headline_from_ul(ul_5,headline_list)
                                    Get_headline_from_ul(ul_6,headline_list)
                                    Get_headline_from_ul(ul_7,headline_list)
                                    Get_headline_from_ul(ul_8,headline_list)
                                    Get_headline_from_ul(ul_9,headline_list)

                                    Get_info_from_ul(ul_1,detail_list)
                                    Get_info_from_ul(ul_2,detail_list)
                                    Get_info_from_ul(ul_3,detail_list)
                                    Get_info_from_ul(ul_4,detail_list)
                                    Get_info_from_ul(ul_5,detail_list)
                                    Get_info_from_ul(ul_6,detail_list)
                                    Get_info_from_ul(ul_7,detail_list)
                                    Get_info_from_ul(ul_8,detail_list)
                                    Get_info_from_ul(ul_9,detail_list)

                                

                                else:
                                    #print("No Data to Crawl")
                                    sleep(random.uniform(1,2))
                                    continue


                                # 3. find Require+ tu_mo_ta
                                #3.0 find final_requirements_list


                                req_final_lst=[]
                                for headline, detail in zip(headline_list, detail_list):

                                    headline_lower=headline.lower()
                                    detail_lower=detail.lower()

                                    #Especially
                                    detail_list=detail.split('\n')
                                    Sokytu_tren1cau=0
                                    for cau in detail_list:
                                        if len(cau)>200:
                                            Sokytu_tren1cau+=1
                                    
                                    if Sokytu_tren1cau >= 2:
                                        continue

                                    

                                    if any(item in headline_lower for item in key_benefit):
                                        continue

                                    if any(item in detail_lower for item in key_benefit):
                                        continue
                                    
                                    if any(item in headline_lower for item in headline_check_lower_list):
                                        req_final_lst.append(detail)

                                    if any(item in detail for item in key_require):
                                        if detail not in req_final_lst:
                                            req_final_lst.append(detail)


                                if len(req_final_lst) != 0:
                                    final_requirement_string="\n".join(req_final_lst)
                                else:
                                    continue

                                
                                #3.1 find tu_mo_ta from headline_list

                                tu_mo_ta_list= [
                                'Qualifications', 'Requirements','Knowledge, Skills And Abilities', 'Skills And Abilities', 'Experience'
                                ,'Requirements','Qualifications','Qualifications','Requirements','Requirements','Skills And Abilities'
                                ]
                                tu_mo_ta= random.choice(tu_mo_ta_list)
                    

                                #3.4 check duplicate info, length

                                #duplicate info
                                if final_requirement_string not in y:
                                    y.append(final_requirement_string)
                                else:
                                    continue
                                
                                #length
                                if len(final_requirement_string) <200:
                                    continue
                                elif len(final_requirement_string)> 2500:
                                    continue
                                else:
                                    final_requirement_string.replace("\n\n","")

                                #dem so dong

                                if final_requirement_string.count('\n') <= 3:
                                    continue



                                #4 adjust title
                                title_final=adjust_title_final(title_cua_job,job_name)
                                #append to list          
                                job_name_count+=final_requirement_string
                                write_sheet.update(f'A{next_arrow_to_write}:D{next_arrow_to_write}',[[job_name,title_final,tu_mo_ta,final_requirement_string]])
                                sleep(1)
                                next_arrow_to_write +=1 

                            except:
                                print("Couldn't Click or Get info from preview")
                                sleep(random.uniform(1,1.5))
                                continue
                            
            except:
                sleep(5)
                continue
        
        if job_order %2==0:
            next_arrow_to_write_format=next_arrow_to_write-1
            write_sheet.format(f'A{very_first_next}:D{next_arrow_to_write_format}',back_ground)
            sleep(1)
        else:
            pass






#some notice
def Warning_Messenger():
    try:
        write_sheet.update('A1:D1',[['Running...........','................','...........','................']])
    except:
        pass
def Allow_Messenger():
    try:
        write_sheet.update('A1:D1',[[' Job_name',' Job_title','Tu_mo_ta','Requirement']])
    except:
        pass

def Write_news_to_tracking_sheet():
    next=tracking_sheet.col_values(1)
    i=int(len(next)+1)
    for x in range(len(job_list_run)):
        tracking_sheet.update_cell(i+x,1,today)
        tracking_sheet.update_cell(i+x,2,job_list_run[x])
        sleep(1)

#write one-time SUMMARY
def Write_Summary():
    Master_tracking_sheet=Master_spread_sheet.worksheet("Job_tracking_by_day")
    all_job_run_in_the_day=len(Master_spread_sheet.worksheet("Job_tracking_by_day").col_values(1)[1:])

    next=Master_tracking_sheet.col_values(3)
    i=int(len(next)+1)
        
    Master_tracking_sheet.update(f'C{i}:F{i}',[[today, all_job_run_in_the_day, start_time, end_time]])



time_start()
start_time = datetime.now().strftime("%H:%M:%S")

Master_spread_sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1bcSBKfA0zWQBT1xYri9cj44Jc28Eh-iHtV9YnZNkx4Y/edit?usp=sharing')

job_list = Master_spread_sheet.worksheet("Job_tracking_by_day").col_values(4)[1:]

# always need
title_check_list=Master_spread_sheet.worksheet('accepted_title').col_values(1)[1:]
title_check_list=[x for x in title_check_list if x!= '']


# check headline + detail (false positive)
key_benefit=Master_spread_sheet.worksheet('key_words').col_values(6)[1:]
key_benefit=[x for x in key_benefit if x!= '']


#check headline (true positive)
headline_check_lower_list=Master_spread_sheet.worksheet('accepted_title').col_values(2)[1:]
headline_check_lower_list=[x for x in headline_check_lower_list if x!= '']


# check detail (true positive)
key_require=Master_spread_sheet.worksheet('key_words').col_values(2)[1:]
key_require=[x for x in key_require if x!= '']




today = date.today().strftime("%d"+'-'+'%m')

#list google sheet to write result(New) (1,2,3)
list_spreadsheet_write=['https://docs.google.com/spreadsheets/d/1dioBHBEAgZIFUvpxeFKFF1l4V6nIWraYeqNro_pKrB8/edit?usp=sharing'
]



# job_list = open('input.txt').read().splitlines()
#Only 3 file ket qua
number_account_end=6
number_account_start=4
for number_order in range(number_account_start,number_account_end+1):
    #take 30 very first job from root_file AND OPEN GG SHEET
    if number_order in [1,2]:
        spread_sheet_write=gc.open_by_url(list_spreadsheet_write[0]) #1
        job_list_run=job_list[:25]
    
    elif number_order in [3,4]:
        spread_sheet_write=gc.open_by_url(list_spreadsheet_write[0]) #2
        job_list_run=job_list[:25]

    elif number_order in [5,6]:
        spread_sheet_write=gc.open_by_url(list_spreadsheet_write[0]) #3
        job_list_run=job_list[:25]


    # job_list_run=job_list[:30]
    for job in job_list_run:
        job_list.remove(job)
    if len(job_list_run)==0:
        sleep(10)
        break

    print('running: '+ str(len(job_list_run)))
    print(job_list_run)
    print('remain: '+ str(len(job_list)))
    print(job_list)
    
    
    tracking_sheet=spread_sheet_write.worksheet('List job')
    #pick or create new worksheet bases on url_CTV and today_sheet
    today_sheet=f"output_{today}"
    try:
        spread_sheet_write.add_worksheet(title=today_sheet, rows=2000, cols=20)
    except:
        pass
    finally:
        write_sheet=   spread_sheet_write.worksheet(f"output_{today}")
    
    #log in by order
    driver=create_driver(number_order)
    sleep(int(random.uniform(10,20)))
    login()
    # cookie='Cookies_Linkedin_Backup.pkl'
    # Load_cookie(cookie)



    
    #1 get data for each job(/30 job) and put all of it into list
    Warning_Messenger()
    sleep(1)
    RunFile(job_list_run,f'output_{number_order}.csv')
    sleep(5)
    driver.close()
    sleep(1)
    #### Write_to_data_raw_sheet()
    Allow_Messenger()
    sleep(1)
    Write_news_to_tracking_sheet()

    sleep(3)
        

time_end()
end_time = datetime.now().strftime("%H:%M:%S")
