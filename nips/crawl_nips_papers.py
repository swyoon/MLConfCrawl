import requests
from bs4 import BeautifulSoup
import os

if __name__=='__main__':
    nips_year = 2016
    nips_year_text = ''
    NIPS_URL = 'http://papers.nips.cc/'
    PAPER_DOWNLOAD_DIR = 'pdf/'
    CSV_NAME = 'NIPS' + str(nips_year)+'.csv'
    DOWNLOAD = True

    if not os.path.exists(PAPER_DOWNLOAD_DIR):
        os.makedirs(PAPER_DOWNLOAD_DIR)

    r = requests.get(NIPS_URL)
    soup = BeautifulSoup(r.text, 'html.parser')

    for li in soup.find_all('ul')[1].find_all('li'):
        if str(nips_year) in str(li.text):
            to_paper_list = li.a['href']

    paper_list_url = NIPS_URL + to_paper_list[1:]
    soup = BeautifulSoup(requests.get(paper_list_url).text, 'html.parser')

    l_papers = []
    for idx, li in enumerate(soup.find_all('ul')[1].find_all('li')):
        row = []
        paper_url = NIPS_URL + li.a['href'][1:]
        print "######", paper_url
        soup = BeautifulSoup(requests.get(paper_url).text, 'html.parser')
        # print soup.body

        paper_title = soup.find_all('h2', class_='subtitle')[0].text
        print paper_title
        l_authors = [ t.text for t in soup.find_all('li', class_='author')]
        s_authors =  ';'.join(l_authors)
        print s_authors
        if s_authors == '':
            s_authors = '-'

        present_type = [t.text.split(':')[1].strip() for t in soup.find_all('h3') if 'Type' in t.text][0]
        print present_type

        abstract = soup.find_all('p', class_='abstract')[0].text
        print abstract

        try:
            paper_pdf_url = NIPS_URL + soup.find_all('a', string='[PDF]')[0]['href'][1:]
            pdf_file_name = paper_pdf_url.split('/')[-1]
            pdf_file_id = pdf_file_name.split('-')[0]
            print pdf_file_name
            if DOWNLOAD:
                with open(PAPER_DOWNLOAD_DIR + pdf_file_name, 'wb') as f:
                    f.write(requests.get(paper_pdf_url).content)
        except:
            pdf_file_name = '-'
            pdf_file_id = '-'

        row.append(str(idx))  # starts with 0
        row.append(pdf_file_id)
        row.append(present_type)
        row.append(paper_title)
        row.append(s_authors)
        row.append(abstract)

        l_papers.append(row)

    l_headers = ['no','id','type','title','authors','abstract']
    l_papers.insert(0, l_headers)

    with open(CSV_NAME, 'w') as f:
        for row in l_papers:
            f.write(','.join(row).encode('utf-8'))
            f.write('\n')

