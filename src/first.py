import requests
import json
import pandas as pd

def rating_ex(x):
    return x['avgRating']
def costForTwo(x):
    return x['costForTwo']/100
def slaString(x):
    return x['slaString']

class chck_res:
    def __init__ (self,strng,lat=17.414482, lng=78.439896):

        self.url_m="https://www.swiggy.com/dapi/restaurants/search"
        self.strng=strng
        self.lat=lat
        self.lng=lng
        self.restro_data={}
    def collect(self):
        return len(self.restro_data)
    def crt_url_prm(self,url,prm):
        lst=[]
        for i in prm:
            ky=i
            vl=prm[i]
            lst.append(str(ky)+"="+str(vl))
        prm_str='&'.join([str(elem) for elem in lst])   
        url=url+"?"+prm_str   
        return (url)  
    
    def crt_url (self,typ,strng):
        if (typ=="suggest"):
            url=self.url_m+"/"+"suggest"
            prm={
                "lat":self.lat,
                "lng":self.lng,
                "str":strng
                }

        if (typ=="restro"):
            url=self.url_m+"/"+"v2_2"
            prm={
                "lat":self.lat,
                "lng":self.lng,
                "str":strng
                }
        return(self.crt_url_prm (url,prm))    
        
    def get_data (self,typ,strng):
        payload=""
        method="GET"
        header={}
        response = requests.request(method, url=self.crt_url(typ,strng), data=payload, headers=header,verify=False)
        return (response)

    def first_select_sugsst (self):
        m=self.get_data ("suggest",self.strng).json()
        return (m['data']['suggestions'][0]['text'])

    def first_select_sugsst_all (self):
        return (self.get_data ("suggest",self.strng).json())

    def getRestroId(self):
        self.restro_data=self.get_data("restro",self.first_select_sugsst())
        m=self.restro_data.json()
        dct={}
        for i in m['data']['restaurants']:
            for n in i['restaurants']:
                dct[n['id']]=n['name']
        return (dct)

    def getRestroIdService(self):
        self.restro_data=self.get_data("restro",self.first_select_sugsst())
        m=self.restro_data.json()
        lst=[]
        for i in m['data']['restaurants']:
            for n in i['restaurants']:
                if (n['unserviceable']==False):
                    l_dct={}
                    l_dct['name']=n['name']
                    l_dct['id']=n['id']
                    l_dct['srch']=self.strng
                    l_dct['fll']=n
                    if ('aggregatedDiscountInfo' in n.keys()):    
                        l_dct['aggregatedDiscountInfo']=n['aggregatedDiscountInfo']                    
                    lst.append(l_dct)
        return (lst)

def answer_me (strng):
    ll=[]
    m_lst=strng.split(",")
    # m_lst=["sandwich","tea"]
    for i in (m_lst):
        kk=chck_res (i)
        kk_2=kk.getRestroIdService ()
        for mm in kk_2:
            ll.append(mm)        
    df=pd.DataFrame(ll,index=range(0,len(ll)))   
    if (len(m_lst)>1):
        df_2=df[df['id'].duplicated()]
    else:
        df_2=df     
    df_2['avgRating']=df_2['fll'].apply (lambda x : rating_ex(x))
    df_2['costForTwo']=df_2['fll'].apply (lambda x : costForTwo(x))
    df_2['slaString']=df_2['fll'].apply (lambda x : slaString(x))    
    df_2['avgRating_flt'] = pd.to_numeric(df_2["avgRating"], downcast="float")
    df_2['costForTwo_flt'] = pd.to_numeric(df_2["costForTwo"], downcast="float")
    df_2=df_2.drop(columns=['fll','srch','avgRating'],axis=1)
    return df_2.to_html(classes='table table-striped')
