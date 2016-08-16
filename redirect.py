# -*- coding: utf-8 -*-
import requests
import csv
import time
import openpyxl 
import multiprocessing

def worker():
    # set filename with date + time
    timestr = time.strftime("%m-%d-%Y-%H-%M-%S")

    # Set the domain for which the data is for
    #domain = "americansignaturefurniture-com-custom-page-"
    domain = "vcf-shared-pages-"
    filename = str("redirect-output\\"+domain+"redirect-"+timestr+".csv")

    # open file where output is written to
    w = open(filename, 'a+')
    colheader = "Status Code,URL,Status Code,URL,Status Code,URL\n"
    w.write(colheader)

    # Update the source file to crawl for links before running script
    with open('rawdata\\vcf-shared-pages-redirect-test-8-15-16.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            urls = row[0]
            response = requests.get(urls)
            if response.history:
                # if there is a redirect
                print "Request was redirected:"
                #reqredirected = "Request was redirected:"
                #w.write(reqredirected)
                #w.write(",")
                for resp in response.history:
                    # pull in HTTP response code and url that corresponds; follow redirects
                    print resp.status_code
                    status = str(resp.status_code)
                    w.write(status)
                    w.write(",")
                    print resp.url
                    url = str(resp.url)
                    w.write(url)
                    w.write(",")
                # find the final destination for the redirected url; store status code (should be 200 OK)
                print "Final destination:"
                #final = "Final destination:"
                #w.write(final)
                #w.write(",")
                print response.status_code
                destinationstatus = str(response.status_code)
                w.write(destinationstatus)
                w.write(",")
                print response.url
                destinationurl = str(response.url)
                w.write(destinationurl)
                w.write("\n")
            else:
                # no redirect was found; show the url that was crawled and move on
                print "Request was not redirected:"
                #noredirect = "Request was not redirected: "
                #w.write(noredirect)
                print response.status_code
                w.write(str(response.status_code)+",") 
                responseurl = response.url
                print responseurl
                w.write(responseurl)
                w.write("\n")

if __name__ == '__main__':
    p = multiprocessing.Process(target=worker)
    p.start()