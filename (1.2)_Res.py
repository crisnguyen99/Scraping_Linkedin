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
import re

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
    job_title_12= jobname.replace(' & ',' %26 ').replace(',',' ').replace('/',' ').replace('-',' ').split()
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
                                                #  /html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[1]/div/div[1]/div[1]/div[2]/div[1]/a
                                                #  /html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[1]/div/div[1]/div[1]/div[2]/div[1]/a


    x.click()
    

#lọc
def Get_info_from_ul (input):
    all_li = input.find_all('li')
    all_li_list = [each_string.get_text().strip() for each_string in all_li]
    li_list_purify= [x for x in all_li_list if len(x) >48]
    # li_list_adjust = [each_string +'###' for each_string in li_list_purify]
    # detail = ''.join(li_list_adjust).strip()
    detail = '\n'.join(li_list_purify)
    return detail

def keyword_purify_1(detail):
    # detail_1=detail.lower()
    if any(item in detail for item in key_words_list):
        detail="---"
    return detail

def Sorting_2(lst):
    lst2 = sorted(lst, key=len)
    return lst2

def remove_short_detail_purify_3(detail):
    if len(detail) <= 300 :
        detail= '---'

    if detail.count('\n') <=2:
        detail= '---'

    return detail

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


#loc Require
def finding_number_exp(exp_sentence):
    exp_sentence=exp_sentence.replace("'",'')
    numbs=re.findall(r'\b[0-9]*',exp_sentence )
    numbs=[x for x in numbs if x != '']
    if len(numbs) >= 2:
        numb_first=int(numbs[1])
        if numb_first>1:
            exp= " years"
        elif numb_first<=1:
            exp= " year"
            
        if numbs[0] < numbs[1]:
            numb_exp="-".join(numbs[:1]) +exp
        else:
            numb_exp=numbs[0]+exp
        
    elif len(numbs) == 1:
        if '+'in exp_sentence:
            numb_exp=numbs[0]+'+ years'
        else:
            if int(numbs[0])==1:
                numb_exp=numbs[0]+' year'
            else:
                numb_exp=numbs[0]+' years'
            
    else:
        numb_exp="---"
        
    return numb_exp

def finding_degree_in(major_sentence):
    
    try:
        sent_list=major_sentence.split(" in ")

        right_part_1=sent_list[1].lower().split(",")
        major_1=right_part_1[0].title()

        right_part_2=sent_list[1].lower().split(" and ")
        major_2=right_part_2[0].title()

        right_part_3=sent_list[1].lower().split(" or ")
        major_3=right_part_3[0].title()
        
        
        lst=[major_1,major_2,major_3]
        lst_major = sorted(lst, key=len)
        
        major_min =lst_major[0].replace("(","").replace(")","").replace("Preferred","").replace("The ","").replace("A ","").replace("An ","").replace(" And","").replace(" Or","")
        wrong_major=['ndustry',"iscipline",'Subject','elate']
        
        if any(item in major_min for item in wrong_major):
            major_min="---"
        
        if len(major_min) >=24:
            major_min="---"
            
        major_list=major_min.split(' ')
        if len(major_list) >= 4:
            major_min="---"
        

    except:
        if "MBA" in major_sentence:
            major_min="MBA"
        else:
            major_min="---"

    return major_min   


def finding_maj_from(require):
    major_sentence="---"
    each_req_split=require.split('\n')

    for sentence in each_req_split:
        if any(item in sentence for item in key_major):
            major_sentence= sentence
            break

    major= finding_degree_in(major_sentence)
    return major

def finding_exp_from(require):
    exp_sentence="---"
    each_req_split=require.split('\n')

    for sentence in each_req_split:
        if any(item in sentence for item in key_exp):
            exp_sentence= sentence
            break

    numb_exp=finding_number_exp(exp_sentence)
    return numb_exp


#long_run
def RunFile(job_list,output_file):
    clear_f= open(output_file,'w', encoding="ascii")
    clear_f.close()
    next=write_sheet.col_values(1)
    next_arrow_to_write=int(len(next)+1)

    job_order=0
    for job_name in job_list:
        job_order+=1
        if job_order %2==0:
            back_ground= {"backgroundColor": {"red": 0.74,"green": 0.87,"blue": 0.4}}

        next=write_sheet.col_values(1)
        very_first_next=int(len(next)+1)
        next_arrow_to_write=int(len(next)+1)


        
        sleep(random.uniform(6,12))
        jobnamesplit= job_name.lower().replace(' of ','').replace(' and ','').replace('-',' ').replace(' & ','').replace(',','').replace('/','').split()
        check=[]
        y=['------']
        job_name_count=""
        job_count_limit=45000
        
    

        #set limitation for VIP job
        # job_title_value=['Manager', 'Engineer' , 'Specialist', 'Analyst', 'Director', 'Developer','Lead','Engineering']
        # job_title_value=[ x.lower() for x in job_title_value  ]

        # if any(item in job_title_value for item in jobnamesplit):
        #     job_count_limit=43*10000
        #     job_count_limit_2=43
        # else:
        #     job_count_limit=int(random.choice([25,26,30,35,43]))*10000
        #     job_count_limit_2=int(random.choice([25,25,30,35,43]))





        #create a list included All page
        list_page_search=Create_All_page_search(job_name,8)

        for page_search in list_page_search:
            #check limit per page
            if len(job_name_count) >= job_count_limit:
                break 

            # if job_name_count_2 >= job_count_limit_2:
            #     break 
            


            try:
                driver.get(page_search)
                sleep(random.uniform(2,3)) 

                #1 Scroll
                driver.set_window_size(400,800)
                
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

                    # if job_name_count_2 >= job_count_limit_2:
                    #     break 

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

                                if len(info_loc)==1:
                                    #1
                                    ul_1 = info_div.find('ul')
                                
                                    detail_1 = Get_info_from_ul(ul_1)
                                    detail_2 = "---"
                                    detail_3 = "---"
                                elif len(info_loc) ==2:
                                
                                    ul_1 = info_div.find('ul')
                                    ul_2 = ul_1.find_next_sibling('ul')

                                    detail_1 = Get_info_from_ul(ul_1)
                                    detail_2 = Get_info_from_ul(ul_2)
                                    detail_3 = "---"
                                elif len(info_loc) >= 3:
                                    #1
                                    ul_1 = info_div.find('ul')
                                    ul_2 = ul_1.find_next_sibling('ul')
                                    ul_3 = ul_2.find_next_sibling('ul')

                                    detail_1 = Get_info_from_ul(ul_1)
                                    detail_2 = Get_info_from_ul(ul_2)
                                    detail_3 = Get_info_from_ul(ul_3)
                                else:
                                    sleep(random.uniform(1,2))
                                    continue
                                # 3. Check detail

                                #3.0 CHECK REQUIRE
                                require= "---"
                                major="---"
                                numb_exp="---"

                                de_list= [detail_1,detail_2,detail_3]
                                for de in de_list:
                                    if any(item in de for item in key_require):
                                        require=de

                                major=finding_maj_from(require)
                                numb_exp= finding_exp_from(require)



                            

                                # 3.1check key words (3 method : any, [], for loop sub_string)

                                detail_1=keyword_purify_1(detail_1)
                                detail_2=keyword_purify_1(detail_2)
                                detail_3=keyword_purify_1(detail_3)


                                #3.2 take max_strings
                                lst = [detail_1,detail_2,detail_3]
                                lst2=Sorting_2(lst)
                                detail_max=lst2[-1]
                                detail_sub_max=lst2[-2]

                                #3.3 remove substandard detail
                                detail_max=remove_short_detail_purify_3(detail_max)
                                detail_sub_max=remove_short_detail_purify_3(detail_sub_max)

                                #3.4 check duplicate info
                                x= detail_max+detail_sub_max
                                if x not in y:
                                    y.append(x)
                                else:
                                    continue

                                #4 adjust title
                                title_final=adjust_title_final(title_cua_job,job_name)

                                #append to list                   
                                job_name_count+= detail_max
                                # job_name_count_2+=1

                                write_sheet.update(f'A{next_arrow_to_write}:F{next_arrow_to_write}',[[job_name,title_final,detail_max,major,numb_exp,require]])
                                sleep(1)
                                next_arrow_to_write +=1 

                            except:
                                print("Could not click")
                                sleep(random.uniform(1,1.5))
                                continue
            except:
                sleep(5)
                continue

        if job_order %2==0:
            next_arrow_to_write_format=next_arrow_to_write-1
            write_sheet.format(f'A{very_first_next}:D{next_arrow_to_write_format}',back_ground)
            sleep(1)            

#some notice
def Warning_Messenger():
    try:
        write_sheet.update('A1:F1',[['Running...........','................','................','Loading...........','................','................']])
    except:
        pass

def Allow_Messenger_n_Note_the_last_row():
    try:
        write_sheet.update('A1:F1',[['(no adjust) Job_name','(no adjust) Job_title','Duties ',    'Major ','Prac_Exp ','Requiment']])
        # write_sheet.format('A1:F1',back_ground)
    except:
        pass

    # last=len(write_sheet.col_values(1))
    # write_sheet.update(f'D{last}:F{last}',[["end","end","end"]])

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

job_list = Master_spread_sheet.worksheet("Job_tracking_by_day").col_values(1)[1:]
key_words_list=Master_spread_sheet.worksheet('key_words').col_values(1)[1:]
key_words_list=[x for x in key_words_list if x!= '']

############################################################################ key_words_list=[x.lower() for x in key_words_list]

key_require=Master_spread_sheet.worksheet('key_words').col_values(2)[1:]
key_require=[x for x in key_require if x!= '']


# tach thong tin tu require
key_exp= Master_spread_sheet.worksheet('key_words').col_values(8)[1:]
key_exp=[x for x in key_exp if x!= '']
key_major=Master_spread_sheet.worksheet('key_words').col_values(9)[1:]
key_major=[x for x in key_major if x!= '']





title_check_list=Master_spread_sheet.worksheet('accepted_title').col_values(1)[1:]
title_check_list=[x for x in title_check_list if x!= '']
today = date.today().strftime("%d"+'-'+'%m')

#list google sheet to write result(New) (1,2,3)
list_spreadsheet_write=['https://docs.google.com/spreadsheets/d/15irl8JbxbPBLHma5pucKJtdDuAF69a8txKn_KwC-dAc/edit?usp=sharing'
]



# job_list = open('input.txt').read().splitlines()
#Only 3 file ket qua

#1 bi loi
number_account_end  =5
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
        sleep(150)
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
    sleep(int(random.uniform(10,30)))
    login()
    # cookie='Cookies_Linkedin_Backup.pkl'
    # Load_cookie(cookie)
    sleep(10)

    

    
    #1 get data for each job(/30 job) and put all of it into list
    Warning_Messenger()
    sleep(1)
    RunFile(job_list_run,f'output_{number_order}.csv')
    sleep(5)
    driver.close()
    sleep(1)
    #### Write_to_data_raw_sheet()
    Allow_Messenger_n_Note_the_last_row()
    sleep(1)
    Write_news_to_tracking_sheet()

    sleep(3)
        

time_end()
end_time = datetime.now().strftime("%H:%M:%S")

#write some info to Master Tracking
# Write_Summary()