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

# xpath解析
tree = etree.HTML(response)

# 解析音标
print("爬取音标......")
yinbiao_en = tree.xpath('//*[@class="phonetic-transcription"][1]/b/text()')[0]
yinbiao_am = tree.xpath('//*[@class="phonetic-transcription"][2]/b/text()')[0]
fp.write('### ***'+word+'***\n')
fp.write('#### Phonetic symbols'+'\n')
fp.write('Britain **'+yinbiao_en+'**      '+'America **'+yinbiao_am+'**\n')

# 解析词义
print("爬取词义......")
meanings_list = tree.xpath('//*[@id="cont-collins"]/div/ul/li')
fp.write('#### Meanings'+'\n')
for meanings in meanings_list:
    try:
        cixing = meanings.xpath('./h4/div/span[1]/text()')[0]
        translation1 = meanings.xpath('./h4/div/span[3]/text()')
        translation2 = meanings.xpath('./h4/div/span[3]/b/text()')[0]
        if len(translation1) == 1:
            translation = translation2 + translation1[0]
        if len(translation1) == 2:
            translation = translation1[0] + translation2 + translation1[1]
    except:
        continue
    fp.write('*'+cixing+'*\n')
    fp.write(translation+'\n\n')

# 解析例句
print("爬取例句......")
examples_list = tree.xpath('//*[@id="cont-sample"]/div/div[2]/ol/li')
fp.write('#### Examples of use'+'\n')
count = 0
for examples in examples_list:
    label = examples.xpath('./label/text()')[0]
    example_list = examples.xpath('./div/p[1]/span')
    ex = ""
    for example in example_list:
        ex = ex+example.xpath('./text()')[0]
    fp.write(label+'. '+ex+'\n')
    count = count + 1
    if count == 10:
        break

# 爬取结束
fp.write('\n---\n')
fp.close()
driver.quit()
print("爬取成功！！！")