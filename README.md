# CINEMA - PythonProject


### 무엇인가요
여러 영화의 정보를 모아서 한번에 보여줄 수 있도록 만든  어플리케이션입니다.

### 사용기술
사용 기술로는 Python, Flask, Sqlite3, Scrapy, Selenium, Ajax 입니다.

Python을 통하여 내부 코드 및, 컨트롤러를 작성해주었고

Flask 를 통하여 웹 어플리케이션을 구성하였으며,

Scrapy 를 통하여 여러 사이트의 정보를 모았으며,

Selenium 을 통해 동적 페이지의 리스펀스를 가져왔으며,

Sqlite 를 통하여 크롤링 한 데이터를 저장하였고,

Ajax 를 통하여 index 페이지의 동적페이징을 구현하였습니다.

### 사용법

Python 3.7 , windws10 


설치
```bash 
pip install flask
pip install scrapy
pip install selenium
pip install sqlite3
pip install pywin32
```

Flask 실행

```bash
PythonProject> python flask11_5.py
```

크롤링 실행

4개의 크롤러중,  megabox_c와 movie_info 는 셀레니움을 사용하는  크롤러입니다.

http://chromedriver.chromium.org/downloads

크롬 웹드라이버, 혹은 사용하시는 웹 드라이버를 구하시고,

아래의 코드의 패스에 웹드라이버 경로를 입력해줘야합니다.
```python
path = '../chromedriver.exe'
options = webdriver.ChromeOptions()
```

만약 추가적으로 생성되는 웹 페이지가 보기싫으시다면

movie.movie의 middleware.py 수정

주석된 코드를 풀어주면 될것입니다.

```python
path = '/Desktop/PythonProject/chromedriver.exe'
options = webdriver.ChromeOptions()
# 추가적인 페이지 생성
#options.add_argument('headless')
options.add_argument('window-size=1200x600')

```


```bash
PythonProject\movie\movie> scrapy crawl movie_info 
PythonProject\movie\movie> scrapy crawl naver_c
PythonProject\movie\movie> scrapy crawl movie_c
PythonProject\movie\movie> scrapy crawl daum_c
PythonProject\movie\movie> scrapy crawl megabox_c
```
순서대로 kobis에서 영화정보를 긁는것,
네이버 영화 크롤
cgv 크롤
다음 영화 크롤
메가박스 크롤 입니다.

kobis.co.kr 의 크롤링 중, 많은 데이터라서 오류가 난다면,

movie.movie의 middleware.py 수정

```python
if request.url == 'http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do':
    driver.get(request.url)
    
    #이부분의 검색 조건을 수정해주거나,
    driver.find_element_by_xpath('//*[@id="sPrdtYearS"]/option[100]').click()
    driver.implicitly_wait(1000)
    driver.find_element_by_xpath('//*[@id="sPrdtYearE"]/option[103]').click()
    driver.implicitly_wait(1000)
    driver.find_element_by_xpath('//*[@id="searchForm"]/div[1]/div[5]/button[1]').click()
    driver.implicitly_wait(1000)
    #이곳 까지 수정.
    
    #이곳에서 시작 -종료 페이징을 설정
    driver.execute_script("goPage('669');return false;")
    driver.implicitly_wait(1000)
    page_list = driver.find_element_by_xpath('//*[@id="pagingForm"]/div/ul').find_elements_by_tag_name('li')
    
    #이후 범위를 추가적으로 주어서 범위를 제한
    for i in range(669, 767):
        print("page :", i)
        for num in range(1, 10):
            element = driver.find_element_by_xpath(
                '//*[@id="content"]/div[4]/table/tbody/tr[' + str(num) + ']/td[1]/span/a')
            driver.execute_script("arguments[0].click();", element)
            driver.implicitly_wait(1000)
    
            spider.addInfoResponse(
                HtmlResponse(driver.current_url, body=driver.page_source, encoding='utf-8', request=request))
    
            exitel = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/a[2]/span')
            driver.execute_script("arguments[0].click();", exitel)
            driver.implicitly_wait(1000)
    
        driver.execute_script("goPage('" + str(i + 1) + "');return false;")
        driver.implicitly_wait(1000)

```
