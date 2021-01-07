# 1. MAke a request to the ebay.com and get a page
# 2. Collect data from each detail page
# 3. Collect all items to details pages of each page
# 4. write scrap data to csv file.
import csv

import requests
from bs4 import BeautifulSoup

def get_page(url):
    response = requests.get(url)

    if not response.ok:
        print("server responded", response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

def get_detail_data(soup):
    #title
    #price
    #sold_quantity

    try:
        title = soup.find('h1', id='itemTitle').text.replace('Details about  \xa0','')
    
    except:
        title = ''
    #print(title)

    try:
        try:   
            p = soup.find('span', id='prcIsum').text.strip()
        except:
            p = soup.find('span', id='prcIsum_bidPrice').text.strip()
        currency , price = p.split(' ')
    except:
        currency= ''
        price = ''
    #print(currency)
    #print(price)
    try:
        sold = soup.find('span', class_='vi-qtyS-hot-red').find('a').text.strip().split(' ')[0]
    except:
        sold = ''
    #print(sold)

    data={
        'title': title,
        'currency': currency,
        'price' : price,
        'total sold' : sold
    }
    return data

def get_index_data(soup):
    try:
        links = soup.find_all('a', class_='s-item__link')
    except:
        links = []
    #print(link)
    urls= [item.get('href') for item in links]
    
    return urls

def write_csv(data, url):
    with open('output.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)

        row = [data['title'],data['price'],data['currency'],data['total sold'],url]

        writer.writerow(row)

    
def main():
    url='https://www.ebay.com/b/Wristwatches/31387/bn_2408451'
    products = get_index_data(get_page(url))

    for link in products:
        data = get_detail_data(get_page(link))
        write_csv(data, link)


if __name__=='__main__':
    main()