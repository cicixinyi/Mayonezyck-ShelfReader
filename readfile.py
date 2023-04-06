# import pandas as pd
from openpyxl import *
import Book,BookList
import json
#df = pandas.read_csv('example.csv', names=['call number','x','title','barcode','xx','xxx','xxxx'])

#d = pd.read_excel('shelflist.xlsx', header=None)
#print(d)

# 打开【shelflist.xlsx】工作簿
def readfile(filename):
    list_wb = load_workbook(filename)
    # 获取活动工作表
    list_ws = list_wb.active

    # 在第一行前插入一行 做header
    list_ws.insert_rows(idx=1)

    # header + 清除没用的列
    list_ws['A1'].value = 'Call number'
    list_ws.delete_cols(2,1) # start from the second colomn, delect one colomn
    list_ws['B1'].value = 'Title'
    list_ws['C1'].value = 'Barcode'
    list_ws.delete_cols(4,3) # start from the 4th colomn, delect three colomns

    # 保存到【shelflist1.xlsx】 可以和【shelflist.xlsx】对比
    #list_wb.save('shelflist1.xlsx')

    # 创建书本字典
    book_info = {}

    # 从第二行开始读取【shelflist1.xlsx】的信息
    for row in list_ws.iter_rows(min_row=2, values_only=True):    
        barcode = row[2] 
        book_info[barcode] = {
            'barcode': barcode,
            'title': row[1],
            'call number': row[0],
            'version': row[3]
            }
        #print(book_info[barcode]['barcode'],'\n')
    list = BookList.BookList(book_info)
    bookdic = {}
    currentbook = list.getHead()
    while currentbook is not None:
        bookdic[currentbook.getBarcode()] = currentbook
        currentbook = currentbook.next_book
    print(bookdic)
    return list, bookdic


#print(readfile('shelflist.xlsx'))
