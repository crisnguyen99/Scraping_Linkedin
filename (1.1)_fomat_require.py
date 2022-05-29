import gspread
from datetime import date
from datetime import datetime
from google.oauth2.service_account import Credentials
from time import sleep
from datetime import datetime, timedelta


today='16-05'

#authorize google sheet api
scopes = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file('lamwork-linkedin-connect.json',scopes=scopes)
gc = gspread.authorize(credentials)

#Read data from sheet
url_spreadsheet='https://docs.google.com/spreadsheets/d/11PAOxJDi239lcDwN2sN2Mii0UkndehgjkRkRLUtKTrs/edit?usp=sharing'
workbook_format=gc.open_by_url(url_spreadsheet)
sheet_input= workbook_format.worksheet('input_format')
sheet_output=workbook_format.worksheet('output_format')

job_name_unique= sheet_output.col_values(1)[1:]
name_list=       sheet_input.col_values(1)[1:]
title_list=      sheet_input.col_values(2)[1:]
tu_mo_ta_list=   sheet_input.col_values(3)[1:]
req1_list=       sheet_input.col_values(4)[1:]



job_name_result_list=[]
job_cleaned_data_list=[]
for i in range(len(job_name_unique)):
    unique_name=job_name_unique[i]
    list_content=[]
    for name, title, mo_ta, req1 in zip(name_list, title_list, tu_mo_ta_list,req1_list):
        if name==unique_name:
            if req1 != '':
                req1_1=req1.replace('###','\n').replace('. ','\n').strip()
                # req1_1=req1.replace('. ','\n').strip()
                    
                content= title+' '+ mo_ta+ '\n' + '\n' + req1_1+   '\n'+'----'
                list_content.append(content)

            else:
                continue
    if len(list_content)>45:
        list_content_limit=list_content[:40]
    else:
        list_content_limit=list_content
    cleaned_data= '\n'.join(list_content_limit)
    job_name_result_list.append(unique_name)
    job_cleaned_data_list.append(cleaned_data)



for i in range(len(job_name_unique)):
    job_name_final=job_name_unique[i]
    for job_name_result, data_result in zip(job_name_result_list,job_cleaned_data_list):
        if job_name_final==job_name_result:
            try:
                sheet_output.update_cell(i+2,2,data_result)  
                sleep(1)
            except:
                sheet_output.update_cell(i+2,2,"Need a check")  
                sleep(1)




# sheet_input.clear()
print('done')