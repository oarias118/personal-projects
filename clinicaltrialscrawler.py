from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import urllib.request
import csv

specialFields = ['Estimated Primary Completion Date', 'Estimated Enrollment', 'Estimated Completion Date', 'Estimated Primary Completion Date', 'Primary Completion Date', 'Enrollment', 'Completion Date', 'Target Follow-Up Duration', 'Biospecimen', 'Sampling Method', 'Study Population', 'Study Arm (s)', 'Study Group/Cohort (s)']

def scrape(trial):
    with urllib.request.urlopen('https://clinicaltrials.gov/ct2/show/record/' + trial) as url:
        s = url.read()
    soup = bs(s, "html.parser")
    trialdict = {}
    table = soup.find_all("tr")

    for row in table:
        if row.th and row.td != "None" and row.th['class'][0] != 'header2':
            label = row.th.get_text().replace(u'ICMJE',u'').replace(u'\xa0', u'').strip()
            if "submitted" in label:
                label = label[0:label.index("   (submitted")]
            try:
                cell = row.td.get_text().replace(u'\xa0', u' ').replace(u'\n', u' ').replace(u'≥', u'>=').replace(u'≤', u'<=').replace(u'∙', u';').strip()
                if cell == '':
                    cell = "Not Provided"
            except:
                cell = ' '
            if len(cell) > 32750:
                cell = cell[0:32750]
                cell = cell + '...'

            trialdict[label] = cell

    for field in specialFields:
        if field not in trialdict:
            trialdict[field] = ' '

    return trialdict

driver = webdriver.Chrome()
dictArray = []

for page in range(0, 1427):
    driver.get("https://clinicaltrials.gov/ct2/crawl/" + str(page))
    trials = driver.find_element_by_tag_name('tbody').find_elements(By.TAG_NAME, 'a')
    for trial in trials:
        dictArray.append(scrape(trial.text))
        print(trial.text)


with open('clinicaltrials.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = sorted(list(dictArray[0].keys()))
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter= ',')
    writer.writeheader()
    for x in dictArray:
        writer.writerow(x)
