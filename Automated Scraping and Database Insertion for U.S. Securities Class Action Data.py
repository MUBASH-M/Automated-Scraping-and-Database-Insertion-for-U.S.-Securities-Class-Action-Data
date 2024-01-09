from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from urllib.parse import quote_plus
import sqlalchemy as db

connection_string = (
    'Driver={ODBC Driver 17 For SQL Server};'#use the driver in your system
    'SERVER=189.123.23.2;'#use your server
    'Database=Case_Research_Data;'#use you data base
    'UID=user1;'#use your username
    'PWD=#####;'#use your password
    'Trusted_Connection=no;'
)

connection_uri = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
    
# Create and return the SQLAlchemy engine
engine = db.create_engine(connection_uri, fast_executemany=True)
# Main Page cookies

#replace the cookies and headers with yours
cookies = {
    '_ga_T3TCVYGVLZ': 'GS1.1.1703761464.7.1.1703764939.60.0.0',
    '_ga': 'GA1.1.382775564.1703313931',
    'JSESSIONID': '91C6A5263DF2BD1185DE76B652089640',
    'uid': '20534',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://securities.stanford.edu/index.html',
    # 'Cookie': '_ga_T3TCVYGVLZ=GS1.1.1703761464.7.1.1703764939.60.0.0; _ga=GA1.1.382775564.1703313931; JSESSIONID=91C6A5263DF2BD1185DE76B652089640; uid=20534',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
}


target_strings=["COURT:","DOCKET #:","JUDGE:","DATE FILED:","CLASS PERIOD START:","CLASS PERIOD END:"]
df_cols=["COURT","DOCKET","JUDGE","DATE FILED","CLASS PERIOD START","CLASS PERIOD END","Case Status","Page Number"]


for i in range(219,220): 
    temp=[]
    #i+=1
    print(i)
    pagenum=i
    response = requests.get(f'https://securities.stanford.edu/filings.html?page={i}', cookies=cookies, headers=headers)
    
    soup = BeautifulSoup(response.content,'html.parser')
    
    table = soup.find('table')
    
    if table:
        rows = table.find_all('tr')
        for row in rows:
            datalist=[]
            columns = row.find_all(['th', 'td'])
            row_data = [column.get_text(strip=True) for column in columns]
            #print(row_data)
            #print(row_data[0])
            #datalist.append(row_data)
            if row_data[0] == 'Filing Name': #and i == 1:
                row_data.insert(0, 'Standford ID')
                row_data.extend(df_cols)
                temp.append(row_data)
                #print(row_data[0])
                #print(temp)
            else:
                #print(row_data)
                onclick_value = row.get('onclick', '')
                match = re.search(r'id=(\d+)', onclick_value)
                if match:
                    id = match.group(1)

                #replace the cookies and headers with yours
                cookies = {
                    '_ga_T3TCVYGVLZ': 'GS1.1.1703761464.7.1.1703764943.56.0.0',
                    '_ga': 'GA1.1.382775564.1703313931',
                    'JSESSIONID': '91C6A5263DF2BD1185DE76B652089640',
                    'uid': '20534',
                }

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Referer': 'https://securities.stanford.edu/filings.html',
                    # 'Cookie': '_ga_T3TCVYGVLZ=GS1.1.1703761464.7.1.1703764943.56.0.0; _ga=GA1.1.382775564.1703313931; JSESSIONID=91C6A5263DF2BD1185DE76B652089640; uid=20534',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                }

                params = {
                'id': f'{id}',
                }

                row_data.insert(0, id)
                detail_response = requests.get('https://securities.stanford.edu/filings-case.html', params=params, cookies=cookies, headers=headers)

                detail_soup = BeautifulSoup(detail_response.content,'html.parser')
                #datas=detail_soup.find_all('p')
            
                datas=detail_soup.find_all('section', {'id': 'fic'})
                for data in datas:
                    report = data.find_all("strong",string=target_strings)
                    for result in report:
                        if result:
                            #finalout={(lambda x:x.replace("#","").replace(":","").strip())(result.text):result.next_sibling}
                            row_data.append(result.next_sibling)
                            
                        else:
                            pass
                casesdatas=detail_soup.find_all('p')
                for i, casedata in enumerate(casesdatas):
                    casesdatas[i] = f'{casedata}'
                    #print(casesdatas[i])
                for casedata in casesdatas:
                    soup = BeautifulSoup(casedata, 'html.parser')

                    # Find and decompose the <span class="icon-check"></span> element
                    icon_check_span = soup.find('span', class_='icon-check')
                    if icon_check_span:
                        icon_check_span.decompose()

                        # Remove extra spaces and tags
                        cleaned_html = str(soup).replace(' ', '').replace('<p>', '').replace('</p>', '').replace('<strong>', '').replace('</strong>', '')
                        cleaned_html = re.sub(r'\s+', ' ', cleaned_html.replace('\n', '')).replace('CaseStatus: ', '')
                        soup = BeautifulSoup(cleaned_html, 'html.parser')
                        span_tag = soup.find('span')
                        # Get the text before <span>
                        substring_before_span = cleaned_html.split(str(span_tag))[0]
                        row_data.append(substring_before_span.strip())
                        #print(cleaned_html)
                        #print(substring_before_span.strip())
                #datalist.append(id)
                row_data.append(pagenum)
                temp.append(row_data)
                #print(temp)
            
            
        #df=pd.DataFrame(temp,columns=df_cols)
#print(temp)
    df = pd.DataFrame(temp[1:], columns=temp[0])
    df.columns = df.columns.str.replace(' ', '_')

    table_name = 'your desitination table name'
    # Insert data into the database table
    df.to_sql(table_name, engine, if_exists='append', index=False)

    # Close the database connection
    engine.dispose()
    print(f"'{pagenum}' inserted") 
print('done')        #del df


