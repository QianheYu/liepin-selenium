import os, csv, showdata
# testdata = {'job':'猎聘','num':1, 'calagory':'a', 'where':'北京', 'time':1, 'salary':1, 'createtime':1}
#
# def test():
#     with open('data.csv', 'w', newline='') as csvfp:
#         csvdata = csv.writer(csvfp)
#         while True:
#             csvdata.writerow(list(testdata.values()))
#             csvdata.writerow(['Spam'] * 5 + ['Baked Beans'])
#             csvdata.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

def start(queue, single, processpid):
    processpid['savedata'] = os.getpid()
    print('savedata已启动')
    with open('data.csv','w', newline='') as fp:
        csvdata = csv.DictWriter(fp, ['job', 'salary', 'where', 'time', 'catagory', 'num', 'createtime', 'companyname', 'properties', 'scale', 'industry'])
        csvdata.writeheader()
        while single['spider']:
            data = queue.get()
            data.update(data['company'])
            del data['company']
            csvdata.writerow(data)
            # print(data)
        else:
            single['savedatastate'] = True
            # showdata.draw()
            print('stop savedata')

if __name__ == '__main__':
    # test()
    pass
