from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup

try:
    html = urlopen('https://study.163.com/course/courseLearn.htm?courseId=1209346809#/learn/video?lessonId=1279117770&courseId=1209346809')
    soup = BeautifulSoup(html,'lxml')

except HTTPError as e:
    print(e)

except URLError as e:
    print(e)

else:
    print("It worked!")
    print(soup.title.text)