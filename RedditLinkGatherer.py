from googlesearch import search
from calendar import monthrange
import datetime
import sqlite3
import re
import os
import urllib.parse
import argparse
# to search

class RedditLinkGatherer():
    def __init__(self,redditLink:str,startYear:str,queryDelay :int,requery:bool=False,startMonth:int=1) -> None:
        if not re.match(r"r/([^\s/]+)", redditLink):
            raise ValueError('The link you provided was not a subreddit')
        self.redditLink=urllib.parse.urljoin('https://www.reddit.com', redditLink)
        try:
            os.remove('./.google-cookie')
        except:
            pass
        tmpDate=datetime.date.today()
        self.currentYear=tmpDate.year
        self.currentMonth=tmpDate.month
        self.currentDay=tmpDate.day
        self.startYear=startYear
        self.startMonth=startMonth
        self.queryDelay=queryDelay
        self.requery=requery
        self.con = sqlite3.connect(f'{redditLink[2:]}.db')
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS gatheredLinks(sub TEXT, link TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS searchedDates(sub TEXT, dateString TEXT)")
        
    def filterLink(self,link):
        return "comments" in link
    
    def insertDateToDB(self,year,month,day):
        self.cur.execute(f"""
                         INSERT INTO searchedDates(sub,dateString)
                         VALUES ("{self.redditLink}","{year}/{month}/{day}");
                         """)
        self.con.commit()
        
    def insertLinkToDB(self,link):
        self.cur.execute(f"""
                         INSERT INTO gatheredLinks(sub,link)
                         VALUES ("{self.redditLink}","{link}");
                         """)
        self.con.commit()
        
    def fetchLink(self,link):
        results=self.cur.execute(f"""
                        SELECT link
                        FROM gatheredLinks
                        WHERE sub="{self.redditLink}"  AND link="{link}"
                         """)
        return results.fetchone()
    
    def fetchDate(self,year,month,day):
        results=self.cur.execute(f"""
                        SELECT dateString
                        FROM searchedDates
                        WHERE sub="{self.redditLink}" AND dateString="{year}/{month}/{day}"
                         """)
        return results.fetchone()
        
    def queryLinks(self,year,month,day):
        # Avoid putting the current day into the database so we can still monitor it on that day
        if not (self.currentDay==day and self.currentMonth==month and self.currentYear == self.startYear) and (self.fetchDate(self.startYear,month,day) == None):
            self.insertDateToDB(year,month,day)
        return search(f'site:{self.redditLink} before:{year}/{month}/{day}', 
                      pause=self.queryDelay,
                      safe='on'
                      )
      
    
    def gatherLinks(self):
        while self.currentYear+1 != self.startYear:
            for month in range(self.startMonth,12+1):
                dayRange=monthrange(self.startYear,month)
                for day in range(1,dayRange[1]+1):
                    if self.currentDay<day and self.currentMonth==month and self.currentYear == self.startYear:
                        return
                    
                    if self.fetchDate(self.startYear,month,day) != None and not self.requery:     
                        continue
                    
                    for query in self.queryLinks(self.startYear,month,day):
                        if self.fetchLink(query) == None and self.filterLink(query):
                            print(f'[NEW LINK] - {query}')
                            self.insertLinkToDB(query)
                        else:
                            print(f'[EXISTING/FILTERED LINK] - {query}')
                            continue
            self.startYear+=1
    
    def storeLink(self):
        pass
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(
                    prog='Reddit Link Gatherer',
                    description='Creates a sqlite database of links from a subreddit using google querys',
                    )
    parser.add_argument('subreddit')
    parser.add_argument('-y', '--year',required=True,type=int)      
    parser.add_argument('-m', '--month',default=1,type=int)
    parser.add_argument('-d', '--delay',default=2,type=int)
    parser.add_argument('-r', '--requery', action='store_true')

    args = parser.parse_args()
    
    print(args)
    gatherer=RedditLinkGatherer(args.subreddit,args.year,args.delay,requery=args.requery,startMonth=args.month)
    gatherer.gatherLinks()