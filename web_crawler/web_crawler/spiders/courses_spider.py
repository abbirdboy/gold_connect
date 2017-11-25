import scrapy

class CoursesSpider(scrapy.Spider):
    name = "courses"
    start_urls = [
    'https://my.sa.ucsb.edu/public/curriculum/coursesearch.aspx'
    ]

    def parse(self, response):
        subject_area = response.css('select#ctl00_pageContent_courseList > option ::attr(value)').extract()[0]
        quarter = response.css('select#ctl00_pageContent_quarterList > option ::attr(value)').extract()[0]
        course_level = response.css('select#ctl00_pageContent_dropDownCourseLevels > option ::attr(value)').extract()[2]
        # print(response.headers.getlist('Set-Cookie'))
        # print(response.headers.getlist('Set-Cookie'))
        cookie = response.headers.getlist('Set-Cookie')[0].decode().split(';')[0].split('=')
        return scrapy.FormRequest.from_response(
            response,
            formdata={'ctl00$pageContent$courseList': subject_area,
            'ctl00$pageContent$quarterList': quarter,
            'ctl00$pageContent$dropDownCourseLevels': course_level,
            'ctl100$pageContent$searchButton.x': '47',
            'ctl100$pageContent$searchButton.y': '5',
            },
            cookies={cookie[0]:cookie[1]},
            headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,it;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length':'2911',
            'Host': 'my.sa.ucsb.edu',
            'Origin': 'https://my.sa.ucsb.edu',
            'Referer': 'https://my.sa.ucsb.edu/Public/curriculum/coursesearch.aspx',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Scrapy/1.4.0 (+http://scrapy.org)',

            },
            dont_click=True,
            # callback=self.parse_results
        )

    def parse_results(self, response):
        print(str(response.url))
        print("This is the response status: %d" % response.status)
        print("printing headers")
        print(response.headers)
        filename = response.url.split("/")[-1] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        # for i in response.css('td#CourseTitle ::text').extract():
        #     print(i)
        # self.html_file.write(response.body.decode("utf-8"))
