from pprint import pprint
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

def data(cloth,brand,size,colour,material):
    
    if cloth=="Shirt":
        r="n%3A1968093031"
    elif cloth=="T-shirt":
        r="n%3A1968120031"
    elif cloth=="Jeans":
        r="n%3A1968076031"
    elif cloth=="Shorts":
        r="n%3A1968097031"
    # %2Cp_89%3A+brand_name
    if brand!="":
        brand_name="%2Cp_89%3A"+brand
    else:
        brand_name=""
        
    if size!="":
        if size=='s':
            size_name='%2Cp_n_size_browse-vebin%3A1975393031'
        elif size=='m':
            size_name='%2Cp_n_size_browse-vebin%3A1975394031'
        elif size=='l':
            size_name='%2Cp_n_size_browse-vebin%3A1975395031'
        else:
            size_name='%2Cp_n_size_browse-vebin%3A1975396031'
    else:
        size=""

    if colour!="":
        if colour=='Black':
                colour_name='%2Cp_n_size_two_browse-vebin%3A1975317031'
        elif colour=='Brown':
            colour_name='%2Cp_n_size_two_browse-vebin%3A1975319031'
        elif colour=='Red':
            colour_name='%2Cp_n_size_two_browse-vebin%3A1975329031'
        elif colour=='Green':
            colour_name='%2Cp_n_size_two_browse-vebin%3A1975321031'
        else:
            colour_name='%2Cp_n_size_two_browse-vebin%3A1975318031'
    else:
        colour_name=""
        # bl - %2Cp_n_size_two_browse-vebin%3A1975317031
        # b -%2Cp_n_size_two_browse-vebin%3A1975319031
        # r - %2Cp_n_size_two_browse-vebin%3A1975329031
        # g - %2Cp_n_size_two_browse-vebin%3A1975321031
        # Blue - %2Cp_n_size_two_browse-vebin%3A1975318031
    if material!="":
        if material=='Cotton':
            material_name='%2Cp_n_material_browse%3A1974776031'
        elif material=='Denim':
            material_name='%2Cp_n_material_browse%3A1974777031'
        elif material=='Linen':
            material_name='%2Cp_n_material_browse%3A1974778031'
        elif material=='Rayon':
            material_name='%2Cp_n_material_browse%3A1974779031'
        else:
            material_name='%2Cp_n_material_browse%3A1974790031'
    else:
        material_name=""
        
    
    url= "https://www.amazon.in/s?i=apparel&rh="+r+brand_name+size_name+colour_name+material_name+"&fs=true&page=1&qid=1614256093&ref=sr_pg_1";
    print(url)
    page = requests.get(url,headers = headers)
    soup = BeautifulSoup(page.content)
    a=[]
    for d in soup.findAll('div', attrs={'class':'a-section aok-relative s-image-tall-aspect'}):
        image = d.find_all('img',alt=True)
        for i in image:
            a.append(i['src'])
    
    
    return a

    # url= "https://www.amazon.in/s?i=apparel&rh="+r+brand_name+size_name+colours+material_name+"&fs=true&page="+str(pageno)+"&qid=1614256093&ref=sr_pg_"+str(pageno)

