import csv
import random
import gspread
from google.oauth2.service_account import Credentials
from time import sleep
import re

#authorize google sheet api
scopes = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
path_to_json='C:/Users/Manh Cam/AppData/Local/Programs/Python/Python39/Lib/site-packages/gspread/lamwork-linkedin-connect.json'
credentials = Credentials.from_service_account_file(path_to_json,scopes=scopes)
gc = gspread.authorize(credentials)





#format them 
def random_value_word():
    tu_mo_ta= ['Responsibilities','Main Duties','Key Responsibilities','Responsibilities','Duties','Duties and Responsibilities','Responsibilities','Responsibilities','Accountabilities']
    random_word= random.choice(tu_mo_ta)
    return random_word

def Concat(title, Major, Exp):

    tu_mo_ta=random_value_word()
    if Major=='---' or Major=='':
        if Exp=='---' or Exp=='':
            frst_line=title+" "+ tu_mo_ta                                   
        else:
            frst_line=title+" "+ tu_mo_ta+ " / "+ Exp                       
    else:
        if Exp=='---' or Exp=='':
            frst_line=title+" "+ tu_mo_ta+ " / "+ Major                     
        else:
            frst_line=title+" "+ tu_mo_ta+ " / "+ Major+ " - "+ Exp         


    return frst_line

    
i_o_url=gc.open_by_url('https://docs.google.com/spreadsheets/d/1Epz60ThQ6-etQhHlvfMAG79qpMnLW_eqlrr1H4YVyDU/edit?usp=sharing')

read_sheet=i_o_url.worksheet('input')
write_sheet=i_o_url.worksheet('output')


distinct_name_list= write_sheet.col_values(1)[1:] #(<30)

name_list=           read_sheet.col_values(1)[1:] #>1000
title_list=          read_sheet.col_values(2)[1:] #>1000
Duties_list=         read_sheet.col_values(3)[1:] #>1000
Major_list=          read_sheet.col_values(4)[1:] #>1000
Prac_Exp_list=       read_sheet.col_values(5)[1:] #>1000


next_line=2

for distinct_name in distinct_name_list: # loop 30
    contents_for_distinct_name=[]
    for name, title, Duties, Major, Exp in zip(name_list,title_list,Duties_list,Major_list,Prac_Exp_list):
        if distinct_name== name:
            if Duties != "":
                Duties=Duties.replace('###','\n').replace('. ','\n').strip()
                # Duties=Duties.replace('. ','\n').strip()

                frst_line=Concat(title, Major, Exp)
                rest_line="\n"+ "\n"+Duties+ "\n"+ "---"

                a_content= Concat(title, Major, Exp) +rest_line
                contents_for_distinct_name.append(a_content)
                if len(contents_for_distinct_name)>=43:
                    break
    
    contents_sum='\n'.join(contents_for_distinct_name)

    #write to sheet
    write_sheet.update_cell(next_line,2,contents_sum)
    next_line+=1
    sleep(1)


print('done')