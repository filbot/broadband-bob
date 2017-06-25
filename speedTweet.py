#!/usr/bin/python
import os
import sys
import csv
import datetime
import time

# https://pypi.python.org/pypi/twitter
import twitter

def test():

        # run speedtest-cli
        # https://pypi.python.org/pypi/speedtest-cli/
        print 'running test'
        a = os.popen("/usr/local/bin/speedtest-cli --simple").read()
        print 'ran'
        #split the 3 line result (ping,down,up)
        lines = a.split('\n')
        print a
        ts = time.time()
        date =datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        #if speedtest could not connect set the speeds to 0
        if "Cannot" in a:
                p = 100
                d = 0
                u = 0
        #extract the values for ping down and up values
        else:
                p = lines[0][6:11]
                d = lines[1][10:14]
                u = lines[2][8:12]
        print date,p, d, u
        #save the data to file for local network plotting
        out_file = open('./speed-data.csv', 'a')
        writer = csv.writer(out_file)
        writer.writerow((ts,p,d,u))
        out_file.close()

        #Twitter credentials
        TOKEN=""
        TOKEN_KEY=""
        CON_SEC=""
        CON_SEC_KEY=""

        my_auth = twitter.OAuth(TOKEN,TOKEN_KEY,CON_SEC,CON_SEC_KEY)
        twit = twitter.Twitter(auth=my_auth)

        #Try to tweet if speedtest couldnt even connect. Probably wont work if the internet is down
        if "Cannot" in a:
                try:
                        tweet="Hey why is my internet down?"
                        twit.statuses.update(status=tweet)
                except:
                        pass

        # Broadband Service Product Name: Internet 45
        # Downstream Speed Range: 24.1 Mbps - 45 Mbps
        # Upload Speed Range: 3 Mbps - 6 Mbps
        # https://www.att.net/speedtiers
        elif eval(d)<24:
                print "trying to tweet"
                try:
                        tweet="Hey, @ATT, why is my internet speed " + str(int(eval(d))) +"Mbps down when I pay for 45Mbps down? #slowinternet #poorservice #speedtest"
                        twit.statuses.update(status=tweet)
                except Exception,e:
                        print str(e)
                        pass
        return

if __name__ == '__main__':
        test()
        print 'completed'
