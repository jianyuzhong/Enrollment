from bs4 import BeautifulSoup
import pandas as pd
from config import logger,config_region
from models.SchoolGroup import SchoolGroup
import pandas as pd
class Spider:
    _instance = None
    def get_html_content(self,file_path:str,file2_path:str):
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
        table= soup.select(f'table[width="{config_region.school_width}"]')#青羊873
        logger.debug(f'{len(table)}')
        name_address_dic=self.get_html2_content(file2_path)
        enrollment_info=[]
        count=0
        school2=[]
        trs=table[0].select('tr')
        group_schools_dic=self.get_school(trs)
        all_data=[]
        for group_code, school_group in group_schools_dic.items():
            school2_string = '\n'.join(f"{school['name']}({school['code']})" for school in school_group.school2)
            for school in school_group.school1:
                single_data={}
                single_data["code"]=school["code"]
                single_data["name"]=school["name"]
                single_data["school2"]=school2_string  
                address=name_address_dic.get(school["name"])
                if address==None:
                    logger.error(f'{school["name"]}:{school["code"]} no address')
                else:
                    single_data["address"]=address
                single_data["region"]=config_region.name
                all_data.append(single_data)
        df = pd.DataFrame(all_data)
        excel_file = "enrollment_data.xlsx"
        df.to_excel(excel_file, index=False)

        a=1
    
    def get_html2_content(self,file_path:str):
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
        table= soup.select_one(f'table[width="{config_region.school2_width}"]')#清扬 954
        trs=table.select('tr')
        return self.get_school2_by_html2(trs)        

    def get_school2_by_html2(self,trs:list)->list:
        group_schools_dic={}
        count=0
        address=''
        for tr in trs:
            count+=1
            if count==1:
                continue   
            tds=tr.select('td')
            school_name= tds[1].text
            if(len(tds)>3):
                address=tds[3].text
                group_schools_dic[school_name]=address
            else:
                group_schools_dic[school_name]=address

        return group_schools_dic
    def get_school(self,trs:list)->list:
        group_schools_dic={}
        count=0
        group_code='1'
        list_len=len(trs)
        for tr in trs:
            count+=1
            if count==1:
                continue
            tds=tr.select('td')
            if len(tds)==0:
                continue
            if len(tds)==config_region.len_row:  #青羊6
                group_code= tds[0].text
                group_schools_dic[group_code]=SchoolGroup(group_code,None,None)
                group_schools_dic[group_code].code=group_code
                group_schools_dic[group_code].school1=[{"code":tds[config_region.code_index].text,"name":tds[config_region.name_index].text}]
                scool2_code=tds[config_region.code2_index].text
                if scool2_code==None or len(scool2_code)==0:
                    group_schools_dic[group_code].school2=[]
                    continue
                group_schools_dic[group_code].school2=[{"code":scool2_code,"name":tds[config_region.name2_index].text}]
            else:
                # if len(tds)<4:
                #     scool2={}
                #     scool2["code"]= tds[0].text
                #     scool2["name"]=tds[1].text
                #     group_schools_dic[group_code].school2.append(scool2)
                #     continue
                scool1={}
                scool1["code"]=tds[0].text
                scool1["name"]=tds[1].text
                if scool1["code"] !=None and len(scool1["code"])>0:
                    group_schools_dic[group_code].school1.append(scool1)
                    
                if len(tds)>3 and tds[3]!=None:
                    if tds[2].text==None or len(tds[2].text)==0:
                        continue
                    scool2={}
                    scool2["code"]= tds[2].text
                    scool2["name"]=tds[3].text
                    
                    group_schools_dic[group_code].school2.append(scool2)
        return group_schools_dic
              