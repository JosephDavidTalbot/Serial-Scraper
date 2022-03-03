import requests, bs4, webbrowser, os, time, string, unicodedata, sqlite3, threading
from sqlite3 import Error
from SQLiteToEpub import *

def parseRR(url):
    if(url == ''):
        return
    session = requests.Session()
    res = session.get(url)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    urlArray = url.split('/')
    name = urlArray[-1].replace('-',' ').title()
    db_path = ".\\"+name+"\\wordcount.db"
    #print(name)

    #bookHTML = ""
    
    conn = None

    if not os.path.exists(".\\"+name):
        os.makedirs(".\\"+name)

    try:
        conn = sqlite3.connect(".\\"+name+"\\wordcount.db")
    except Error as e:
        print(e)
        return
    
    db = conn.cursor()
    db.execute(""" CREATE TABLE IF NOT EXISTS chapters (
                id integer PRIMARY KEY,
                title text NOT NULL,
                url text UNIQUE NOT NULL,
                content text NOT NULL,
                wordcount integer NOT NULL,
                datePosted text
                ); """)
    conn.commit()
    idCounter = 0 #Chapter ID is zero-indexed and represents order of posting.
    finalPage = False

    curUrl = 'https://www.royalroad.com' + soup.select('td a')[0]['href']
    #print(curUrl)
    db.execute("select count(*) from chapters")
    is_empty = db.fetchall()[0][0]
    if(is_empty > 0):
        db.execute("select max(id), url from chapters where id = (select max(id) from chapters)")
        latest = db.fetchall()[0]
        idCounter = latest[0]
        curUrl = latest[1]

    res = session.get(curUrl)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    nextButton = soup.select('div .nav-buttons div')[1]
    try:
        nextURL = 'https://www.royalroad.com' + nextButton.select('a')[0]['href']
        curUrl = nextURL
        tempRes = session.get(nextURL)
        soup = bs4.BeautifulSoup(tempRes.text, "html.parser")
    except:
        finalPage = True
        print("Up to date on "+name+"!")
        return
    

    while (not finalPage):
        chapter=soup.select('.chapter-content')[0]
        #bookHTML += chapter

        #chapterString=chapter.getText()
        chapterString=str(chapter)
        chapterTitle = soup.select('h1')[0].getText()
        wordcountString = chapter.getText().split()
        chapterWordcount = len(wordcountString)
        datePosted = soup.find('time').attrs['datetime']

        #print(chapterTitle + '. Date Posted: '+ datePosted+'. Wordcount: ' + str(chapterWordcount))
        blob = (str(idCounter),chapterTitle,curUrl,chapterString,str(chapterWordcount),datePosted)
        db.execute("INSERT OR IGNORE INTO chapters(id, title, url, content, wordcount, datePosted) values (?,?,?,?,?,?);", blob)
        idCounter += 1

        nextButton = soup.select('div .nav-buttons div')[1]
        #print(nextButton)
        #if('button' in nextButton):
        #if(curUrl == nextURL):
        try:
            nextURL = 'https://www.royalroad.com' + nextButton.select('a')[0]['href']
            curUrl = nextURL
            tempRes = session.get(nextURL)
            soup = bs4.BeautifulSoup(tempRes.text, "html.parser")
        except:
            finalPage = True
            break

            
    conn.commit()
    db.execute("Select sum(wordcount), count(wordcount), avg(wordcount), min(wordcount), max(wordcount) from chapters")
    row = db.fetchall()[0]
    #print(row)
    print(name+':\nTotal wordcount: '+str(row[0])+'.    Chapters: '+str(row[1])+'.    Average Words Per Chapter: '+str(row[2])+'.    Minimum Wordcount: '+str(row[3])+'.    Maximum Wordcount: '+str(row[4])+'\n')
    conn.close()
    parseSQLite(db_path,name)





#Main

configFile = open(".\\config.txt", 'a', encoding='utf-8')
configFile.close()
configFile = open(".\\config.txt", 'r', encoding='utf-8')
config = configFile.read()
configFile.close()
configFile = open(".\\config.txt", 'a', encoding='utf-8')

entering = True

while(entering):
    print(config)
    print('Input the URL of the story to be scraped:')
    url = input()
    if(url == ''):
        entering = False
        print('Now scanning...')
    else:
        configFile.write(url+'\n')
configFile = open(".\\config.txt", 'r', encoding='utf-8')
config = configFile.read()
configFile.close()
start = time.time()
print('Starting...\n\n')

stories = config.split('\n')
downloadThreads = []

for story in stories:
    downloadThread = threading.Thread(target=parseRR, args=(story,))
    downloadThreads.append(downloadThread)
    downloadThread.start()
    time.sleep(0.5)

for downloadThread in downloadThreads:
    downloadThread.join()

#session = requests.Session()
#session.get(url)
#parseRR(url)
print('All done!')
end = time.time()
print('Elapsed time: '+(str(end - start)))
