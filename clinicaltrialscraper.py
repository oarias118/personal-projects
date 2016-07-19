from bs4 import BeautifulSoup as bs
import urllib.request
import csv

with urllib.request.urlopen('https://clinicaltrials.gov/ct2/show/record/NCT00000102') as url:
    s = url.read()

soup = bs(s, "html.parser")
fieldnames = []
trialdic = {}

table = soup.find_all("tr")
for row in table:
    if row.th and row.td != "None" and row.th['class'][0] != 'header2':
        label = row.th.get_text().replace(u'ICMJE',u'').replace(u'\xa0', u'').strip()
        fieldnames.append(label)
        try:
            cell = row.td.get_text().replace(u'\xa0', u' ').replace(u'\n', u' ').strip()
            if cell == '':
                cell = "Not Provided"
        except:
            cell = ' '
        trialdic[label] = cell



with open('clinicaltrials.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter= ',')
    writer.writeheader()
    print(trialdic)
    writer.writerow(trialdic)
