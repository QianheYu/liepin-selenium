from bs4 import BeautifulSoup
import threading
import requestPage
import random, time
import acquire
import os
import thread

x_lock = threading.Lock()
y_lock = threading.Lock()

detailpageurls = []
spidersingle = True

class listpage(requestPage.Browser):

    def start_url(self, starturl):
        self.get_page(starturl, self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response, 'lxml')
        joblist = soup.find('div', 'main').find('ul', 'super-jobs job-lists')
        urls = joblist.find_all('a','ellipsis')[::2]
        with acquire.acquire(x_lock, y_lock):
            detailpageurls.extend(urls)
        # print(urls)
        nextpage = soup.find('div', 'searchResultPagination').find_all('a')[-1]
        # print(nextpage['href'])
        # print('*'*50)
        delay = random.randrange(25, 45)
        time.sleep(delay)
        if spidersingle == True:
            self.follow(nextpage['href'], self.parse)




class detailpage(requestPage.Browser):
    def __init__(self, browser, queue):
        super(detailpage, self).__init__(browser)
        self.queue = queue
    def start_url(self):

        urls = []
        while True:
            with acquire.acquire(y_lock, x_lock):
                if len(detailpageurls):
                    alabels = detailpageurls
                    urls.extend(alabels)
                    detailpageurls.clear()
            # print('url数：%d' % len(urls))
            if len(urls):
                self.get_page(urls[0]['href'], self.parse)
                del urls[0]
                time.sleep(random.randrange(0,4))
            else:
                # print('等待3秒...')
                time.sleep(3)

    def parse(self, response):
        # print(self.queue)
        global detailpageurls
        soup = BeautifulSoup(response, 'lxml')
        jobtitle = soup.find('div','job-brief wrap')
        jobdescribe = soup.find('div', 'job-desc').find('p')
        company = soup.find('div', 'company-address').find('div', 'company-desc')
        companyinfo = {}
        companyinfolist = company.find_all('p')
        companyinfo['companyname'] = company.find('a').text


        companyinfo['properties'] = companyinfolist[0].text[3::]
        companyinfo['scale'] = companyinfolist[1].text[3::]
        companyinfo['industry'] = companyinfolist[2].text[3::]
        # companyinfo.update({'companyname':company.find('a').text, 'properties':companyinfolist[0].text[3::], 'scale':companyinfolist[1].text[3::], 'industruy':companyinfolist[2].text[3::]})
        item = {}
        item['job'] = jobtitle.find('h1','job-name').text
        item['salary'] = jobtitle.find('span','salary').text
        item['where'] = jobtitle.find('span', 'where').text
        item['time'] = jobtitle.find('span', 'time').text
        item['catagory'] = jobtitle.find('span','catagory').text
        item['num'] = jobtitle.find('span', 'num').text
        item['createtime'] = jobtitle.find('span', 'create-time').text
        item['company'] = companyinfo
        self.queue.put(item)
        # print(dataprocess.processing)
        # print(processing.get())

def startlistpagespider():
    print('listspider已运行')
    browser = listpage("Firefox")
    browser.start_url('https://campus.liepin.com/sojob/')

def startpagespider(queue):
    print('pagespider已运行')
    browser = detailpage("Firefox", queue)
    browser.start_url()


def startspider(queue, single, processpid):
    processpid['spider'] = os.getpid()
    listpagespider = threading.Thread(target=startlistpagespider)
    listpagespider.start()
    getdetailpage = threading.Thread(target=startpagespider, args=(queue,))
    getdetailpage.start()
    while single['spider']:
        pass
    else:
        global spidersingle
        spidersingle = False
        listpagespider.join()
        getdetailpage.join()
        print('stop spider')
        single['spiderstate'] = True


if __name__ == '__main__':
    listpagespider = threading.Thread(target=startlistpagespider)
    listpagespider.start()
    getdetailpage = threading.Thread(target=startpagespider)
    getdetailpage.start()
