# -*- coding: utf-8 -*-
import scrapy
import openpyxl
import js2xml


class IndeedSpider(scrapy.Spider):
    name = 'indeed'
    allowed_domains = ['www.indeed.co.uk/jobs?q=&l=Gloucester']
    start_urls = ['https://www.indeed.co.uk/jobs?q=&l=Gloucester']

    def parse(self, response):
#        print("Cool Success!")

        scripts = response.xpath("//script/text()")
        foundkeys = scripts[6].extract()

        jstree = js2xml.parse(foundkeys)

#        print(js2xml.pretty_print(jstree))

        brackets = jstree.xpath('//bracketaccessor')

        untidy_keys = brackets[0].xpath('//text()')

        copy_keys = untidy_keys[5:-11] # filing rough edges!

#        print(untidy_keys)
#        print(tidier_keys)

        keyring = [] # make a keyring!

        for each in range(0, len(copy_keys),2):
            keyring.append(copy_keys[each])
#            print(copy_keys[each])

#        print(keyring)

        for each_key in keyring:
        	# sponsored jobs
        	job = response.xpath("//div[@data-jk='{0}']".format(each_key))

        	jobtitle = response.xpath("//div[@data-jk='{0}']/a/text()".format(each_key)).extract()
        	job_desc_link = response.xpath("//div[@data-jk='{0}']/a/@href".format(each_key)).extract()
        	company_info = response.xpath("//div[@data-jk='{0}']/div/div/span/a/text()".format(each_key)).extract_first()
        	company_link = response.xpath("//div[@data-jk='{0}']/div/div/span/a/@href".format(each_key)).extract_first()
        	location = response.xpath("//div[@data-jk='{0}']/div/span/text()".format(each_key)).extract_first()
        	salary = response.xpath("//div[@data-jk='{0}']/table/tr/td/div/span[@class='salary no-wrap']/text()".format(each_key)).extract_first()
        	summary = response.xpath("//div[@data-jk='{0}']/div[3]/table/tr/td/span/text()".format(each_key)).extract_first()

        	if jobtitle == []:
        		# wasn't sponsored jobs then
        		jobtitle = response.xpath("//div[@data-jk='{0}']/h2/a/text()".format(each_key)).extract()
        	
        	if job_desc_link == []:	
        		job_desc_link = response.xpath('//h2[@id="jl_{0}"][@class="jobtitle"]/a/@href'.format(each_key)).extract_first()

        	if company_info == None:
        		company_info = response.xpath("//div[@data-jk='{0}']/div[@class='companyInfoWrapper']/div/span/text()".format(each_key)).extract()

        	if location == None:
        		location = response.xpath("//div[@data-jk='{0}']/div/div[@class='location']/text()".format(each_key)).extract_first()

        	if salary == None:
        		salary = response.xpath("//div[@data-jk='{0}']/div[3]/table/tr/td/div/span/text()".format(each_key)).extract_first()

        	if summary == None:
        		summary = response.xpath("//div[@data-jk='{0}']/table/tr/td/div/span[@class='summary']/text()".format(each_key)).extract_first()

        	print(jobtitle)
        	print(job_desc_link)
        	print(company_info)
        	print(company_link)
        	print(location)
        	print(salary)
        	print(summary)
        	print("-----")
 