def crt_url_prm(url,prm):
    lst=[]
    for i in prm:
        ky=i
        vl=prm[i]
        lst.append(str(ky)+"="+str(vl))
    prm_str='&'.join([str(elem) for elem in lst])   
    url=url+"?"+prm_str   
    return (url)