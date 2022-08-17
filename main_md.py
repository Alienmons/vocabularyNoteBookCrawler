# -*- coding = utf-8 -*-
# @Time :2022-07-27 15:37
# @Author : Sunday
# @File : main_md.py
# @Software : PyCharm

# 导入包
from selenium import webdriver
from lxml import etree
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# 无头网页
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 开始爬取
word = input("Please enter the word you want to search:")
print("开始爬取......")
url = "https://fanyi.baidu.com/?aldtype=16047#auto/zh/"+word
service = Service(executable_path="D:\google_driver\chromedriver.exe") # 选择谷歌浏览器驱动程序所在路径
driver = webdriver.Chrome(service=service,options=chrome_options)
driver.get(url)
response = driver.page_source

# 打开.md文件
fp = open('vocabularyNoteBook.md','a',encoding='utf-8')
fp.write('### '+word+'\n')

# xpath解析
tree = etree.HTML(response)

# 解析音标
print("爬取音标......")
yinbiao_en = tree.xpath('//*[@id="left-result-container"]/div[2]/div[2]/div[1]/div[2]/div[1]/div/span[1]/b/text()')[0]
yinbiao_am = tree.xpath('//*[@id="left-result-container"]/div[2]/div[2]/div[1]/div[2]/div[1]/div/span[2]/b/text()')[0]
fp.write('#### Phonetic symbols'+'\n'+'['+yinbiao_en+']  ['+yinbiao_am+']\n')

# 解析词义
print("爬取词义......")
meanings_list = tree.xpath('//*[@id="cont-edict"]/div/div')
fp.write('#### Meanings'+'\n')
for meanings in meanings_list:
    # print(type(meanings))
    cixing = meanings.xpath('./p/text()')[0]
    meaning_list = meanings.xpath('./dl')
    for meaning in meaning_list:
        mean = meaning.xpath('./dt/text()')[0]
        translation = cixing + '. ' + mean
        fp.write('- '+translation+'\n')

# 解析例句
print("爬取例句......")
examples_list = tree.xpath('//*[@id="cont-sample"]/div/div[2]/ol/li')
fp.write('#### Examples of use'+'\n')
for examples in examples_list:
    label = examples.xpath('./label/text()')[0]
    example_list = examples.xpath('./div/p[1]/span')
    ex = ""
    for example in example_list:
        ex = ex+example.xpath('./text()')[0]
    fp.write(label+'. '+ex+'\n')

# 爬取结束
fp.close()
driver.quit()
print("爬取成功！！！")