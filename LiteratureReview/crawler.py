from pandas._config.config import reset_option
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import sys
import time
import pandas as pd
import re


kernel_conference = ['WWW', 'Assets', 'assets', 'ASSETS', 'CHI', 'chi', 'UbiComp', 'UIST', 'MSR']

def translate(name):
    interval = 3
    url = "https://translate.google.cn/?sl=" + 'en' + "&tl=" + 'zh-CN' + "&op=translate"
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument('--disable-infobars')
    options.add_argument('--blink-settings=imagesEnabled=false') 
    browser = webdriver.Chrome(executable_path="./chromedriver", options = options)
    browser.get(url)
    time.sleep(interval)
    input_element = browser.find_element_by_tag_name('textArea')

    df = pd.read_excel(name)
    df['Cabstract'] = ''
    for i in range(len(df['abstract'])):
        input_element.clear()
        input_element.send_keys(df.loc[i, 'abstract'])
        time.sleep(interval)
        result_elements = browser.find_elements_by_tag_name('span')
        print(result_elements[87].get_attribute('innerText'))
        df.loc[i, 'Cabstract'] = result_elements[87].get_attribute('innerText')
        time.sleep(interval)
    df.to_excel(name, encoding = 'utf-8', index = False)


def minus(name, name1):
    df = pd.read_excel(name)
    df1 = pd.read_csv(name1)
    # print(len(df1['title']))
    # print(df1['title'])
    df['flag'] = 0
    for i in range(len(df['title'])):
        # if type(df.loc[i, 'abstract']) != str or len(df.loc[i, 'abstract']) < 30:
        #     df.loc[i, 'flag'] = 1
        # print(df.loc[i, 'title'] + '.')
        if df.loc[i, 'title'] + '.' in df1['title'].values.tolist():
            print('wow')
            df.loc[i, 'flag'] = 1
    temp_df = df[df.flag == 0]
    temp_df = temp_df.drop('flag', axis = 1)
    temp_df.to_excel('acm_filtered_abs3.xlsx', encoding = 'utf-8', index = False)


def select_conf(conference):
    global kernel_conference
    for item in kernel_conference:
        if item + ' \'' in conference:
            if item[0] != conference[0] or ' EA \'' in conference:
                return 0
            if item == 'Assets' or item == 'ASSETS' or item == 'assets':
                return 1
            else:
                return 2
    return 0

def select_page(conference):
    if type(conference) != str:
        return 1
    nums = re.findall('\d+', conference)
    if len(nums) != 2:
        return 1
    if int(nums[1]) - int(nums[0]) <= 3:
        return -1
    elif int(nums[1]) - int(nums[0]) < 6:
        return 0
    return 1
    

def scratch_filter(name, name1):
    df = pd.read_excel(name)
    df1 = pd.read_excel(name1)
    df['flag'] = df['journal'].apply(select_conf)
    df['flag'] = df['flag'] + df['pages'].apply(select_page)
    temp_df = df[df.flag >= 2]
    temp_df = temp_df.drop('flag', axis = 1)
    # print(temp_df)
    if name != name1:
        temp_df = temp_df.append(df1)
    temp_df = temp_df.drop_duplicates(subset = 'title', keep = 'first')
    temp_df.to_excel('./acm_filtered_abs30.xlsx', index = False, encoding = 'utf-8')


def scratch_abstract(name):
    df = pd.read_excel(name)
    browser = webdriver.Chrome(executable_path="./chromedriver")
    for i in range(len(df['url'])):
        # if i < 25:
        #     continue
        try:
            url = df.loc[i, 'url']
            print(url)
            browser.get(url)
            abstract = browser.find_element_by_class_name('hlFld-Abstract').find_element_by_tag_name('p').get_attribute('innerText')
            df.loc[i, 'abstract'] = abstract
        except:
            continue
    df.to_excel('acm_filtered_abs3.xlsx', encoding = 'utf-8', index = False)

def scratch_paper(urlPrefix, resNumber, pageSize):
    browser = webdriver.Chrome(executable_path="./chromedriver")
    # browser.get('https://translate.google.cn/')
    # browser.execute_script("window.open('');")
    # browser.execute_script("window.open('');")
    # browser.switch_to_window(browser.window_handles[1])
    maxPage = (resNumber + pageSize - 1) // pageSize
    df = pd.DataFrame({'title': [], 'year': [], 'journal': [], 'url': [], 'pages': [], 'abstract' : []})

    for i in range(maxPage):
        url = urlPrefix + str(i) + '&pageSize=' + str(pageSize)
        browser.get(url)
        res = browser.find_elements_by_class_name('issue-item__content-right')
        for hyperItem in res:
            try:
                item = hyperItem.find_elements_by_class_name('issue-item__title')[0].find_elements_by_class_name('hlFld-Title')[0].find_element_by_tag_name('a')
                title = item.get_attribute('innerText')
                doi = item.get_attribute('href')
                # print(title, doi)
                
                detail = hyperItem.find_elements_by_class_name('issue-item__detail')[0].find_element_by_tag_name('a')
                journal = detail.get_attribute('title')
                details = hyperItem.find_elements_by_class_name('issue-item__detail')[0].find_elements_by_class_name('dot-separator')[0].find_elements_by_tag_name('span')
                year = details[0].get_attribute('innerText')
                pages = details[1].get_attribute('innerText')

                # browser.switch_to_window(browser.window_handles[2])
                # browser.get(doi)
                # abstract = browser.find_element_by_class_name('hlFld-Abstract').find_element_by_tag_name('p').get_attribute('innerText')
                # browser.switch_to_window(browser.window_handles[1])
            except:
                continue
            df = df.append({'title': title, 'year': year, 'journal': journal, 'url': doi, 'pages': pages, 'abstract' : ''}, ignore_index = True)
            # print(df)
        print('Finish page ' + str(i))
    # scratch_abstract(browser, df)
    df.to_excel('./acm_res3.xlsx', encoding = 'utf-8', index = False)

def scratch(url):
    browser = webdriver.Chrome(executable_path="./chromedriver")
    # print(url)
    browser.get(url)
    browser.implicitly_wait(5)
    browser.find_element_by_class_name('more').click()       
    old_len, new_len = 0, len(browser.find_elements_by_class_name('part_middle')) 
    while old_len != new_len:
        browser.implicitly_wait(2)
        old_len = new_len
        js = "var q=document.documentElement.scrollTop=100000"
        browser.execute_script(js)
        time.sleep(2)
        new_len = len(browser.find_elements_by_class_name('part_middle')) 
    res = browser.find_elements_by_class_name('part_middle')
    comments = [item.text for item in res]
    print(len(comments), comments)

if __name__ == '__main__':
    # scratch(sys.argv[1])
    # scratch_paper('https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&AllField=Title%3A%28%22seniors%22+OR+%22senior+people%22+OR+%22senior+citizen%22+OR+%22senior+adult%22+OR+%22senior+individual%22+OR+%22older%22+OR+%22elder%22++OR+%22later+life%22%29+OR+Abstract%3A%28%22seniors%22+OR+%22senior+people%22+OR+%22senior+citizen%22+OR+%22senior+adult%22+OR+%22senior+individual%22+OR+%22older%22+OR+%22elder%22++OR+%22later+life%22%29+OR+Keyword%3A%28%22seniors%22+OR+%22senior+people%22+OR+%22senior+citizen%22+OR+%22senior+adult%22+OR+%22senior+individual%22+OR+%22older%22+OR+%22elder%22+OR+%22later+life%22%29&startPage=', 2448, 50)

    # scratch_paper('https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&SeriesKeyAnd=tochi&AllField=Title%3A%28%22seniors%22+OR+%22senior+people%22+OR+%22senior+citizen%22+OR+%22senior+adult%22+OR+%22senior+individual%22+OR+%22older%22+OR+%22elder%22+OR+%22later+life%22%29+OR+Abstract%3A%28%22seniors%22+OR+%22senior+people%22+OR+%22senior+citizen%22+OR+%22senior+adult%22+OR+%22senior+individual%22+OR+%22older%22+OR+%22elder%22+OR+%22later+life%22%29+OR+Keyword%3A%28%22seniors%22+OR+%22senior+people%22+OR+%22senior+citizen%22+OR+%22senior+adult%22+OR+%22senior+individual%22+OR+%22older%22+OR+%22elder%22+OR+%22later+life%22%29&startPage=0&pageSize=50', 20, 50)
    scratch_filter('./acm_res.xlsx', './acm_res.xlsx')
    # scratch_abstract('./acm_res1.xlsx')
    # minus('./acm_filtered_abs3.xlsx', 'first_round.csv')
    # translate('./acm_filtered_abs3.xlsx')
    # scratch_abstract('./acm_filtered_abs3.xlsx')
    # scratch_paper('https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&AllField=%28Title%3A%28%22mobile%22%29+OR+Abstract%3A%28%22mobile%22%29+OR+Keyword%3A%28%22mobile%22%29%29+AND+%28Title%3A%28%22accessibility%22%29+OR+Abstract%3A%28%22accessibility%22%29+OR+Keyword%3A%28%22accessibility%22%29%29&startPage=', 590, 50)