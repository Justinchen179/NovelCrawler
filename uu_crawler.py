#!/usr/bin/env python3
import os
import requests as rq
from bs4 import BeautifulSoup

if not os.path.isdir('./books'):
    os.mkdir('./books')


def GetSoupByURL(url):
    response = rq.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    return soup


def GetHomeSoup():
    url = "https://tw.uukanshu.com/"
    return GetSoupByURL(url)


def GetBookSoupByID(book_id, page=1):
    url = "https://tw.uukanshu.com/t/%s/%d/" % (book_id, page)
    return GetSoupByURL(url)


def GetBookSoupByIDByPAGE(book_id, page):
    url = "https://tw.uukanshu.com/b/%s/%d.html" % (book_id, page)
    print(url)
    return GetSoupByURL(url)


def GetCotnent(soup, book_title):
    content = soup.select('div.contentbox p')
    title = soup.select('div.h1title h1')
    titles = title[0]

    book_content = ""
    book_content += titles.string + "\n"
    for row_content in content:
        if(row_content.string != None):
            book_content += row_content.string + "\n"
        else:
            book_content += row_content.text + "\n"
    with open("books/%s.txt" % book_title, "a+", encoding='UTF-8') as book_file:
        book_file.write(book_content)


if __name__ == '__main__':

    books = []

    home_soup = GetHomeSoup()
    newbooks = home_soup.select('.lmxstj li a')
    for newbook in newbooks:
        book_title = newbook.text
        book_id = newbook.get("href").split("/")[-2]
        books.append({
            "id": book_id,
            "title": book_title
        })

    for book in books:
        id = book["id"]
        title = book["title"]
        soup = GetBookSoupByID(id)
        zhangjie = soup.select('div.zhangjie ul li a')
        for page in zhangjie:
            page_number = int(page['href'][page['href'].find('/#')+2:])
            print(page_number)
            page_soup = GetBookSoupByIDByPAGE(id, page_number)
            GetCotnent(page_soup, title)
