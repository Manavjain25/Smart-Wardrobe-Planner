from pprint import pprint
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

def data(cloth,pageno):
    if cloth=="Shirt":
        r="n%3A1968093031"
    elif cloth=="T-shirt":
        r="n%3A1968120031"
    elif cloth=="Jeans":
        r="n%3A1968076031"
    elif cloth=="Shorts":
        r="n%3A1968097031"

    url = "https://www.amazon.in/s?i=apparel&rh="+r+"&fs=true&page="+str(pageno)+"&qid=1614256093&ref=sr_pg_"+str(pageno)
    print(url)
    page = requests.get(url,headers = headers)
    soup = BeautifulSoup(page.content)
    a=[]
    for d in soup.findAll('div', attrs={'class':'a-section aok-relative s-image-tall-aspect'}):
        image = d.find_all('img',alt=True)
        for i in image:
            a.append(i['src'])
    
    
    return a

    # print(a)
    # print(len(a))
  # print(soup)

# data("Jeans",10)

#"https://www.amazon.in/s?i=apparel&rh=n%3A1968107031&fs=true&qid=1614256093&ref=sr_pg_2" (Blazer)
#"https://www.amazon.in/s?i=apparel&rh=n%3A1968120031&fs=true&qid=1614769214&ref=sr_pg_1"(T-shirt)
#"https://www.amazon.in/s?i=apparel&rh=n%3A1968097031&dc&fs=true&qid=1614769439&ref=sr_nr_n_7"(shorts)
#"https://www.amazon.in/s?i=apparel&rh=n%3A1968076031&dc&fs=true&qid=1614769595&ref=sr_nr_n_3" (jeans)
#"https://www.amazon.in/s?i=apparel&rh=n%3A1968248031&dc&fs=true&qid=1614769696&ref=sr_nr_n_13"(ethnic)