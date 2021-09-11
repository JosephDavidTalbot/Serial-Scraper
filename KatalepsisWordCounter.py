import requests, bs4, webbrowser, os, time, string, unicodedata, sqlite3
from sqlite3 import Error

def parseKata(kataurl):
    curUrl = kataurl
    res = session.get(kataurl)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    if not os.path.exists(os.path.abspath(ficFile)):
        os.makedirs(ficFile)
    conn = None
    try:
        conn = sqlite3.connect(ficFile+'\\katalepsis.db')
    except Error as e:
        print(e)
        return
    
    db = conn.cursor()
    db.execute(""" CREATE TABLE IF NOT EXISTS chapters (
                id integer PRIMARY KEY,
                title text UNIQUE NOT NULL,
                url text UNIQUE NOT NULL,
                content text NOT NULL,
                wordcount integer NOT NULL,
                datePosted text,
                book integer
                ); """)
    conn.commit()
    idCounter = 0 #Chapter ID is zero-indexed and represents order of posting.
    finalPage = False
    

    while (not finalPage):
        chapter=soup.select('.entry-content')[0]
        
        chapterString=chapter.getText()

        chapterTitle = str(soup.select('.entry-title')[0].getText())
        
        book = chapterTitle
        book = book.split('.')[0]
        book = book.split()[-1]
        

        wordcountString = chapterString.split()
        chapterWordcount = len(wordcountString)

        datePosted = soup.find('time').attrs['datetime']

        print(chapterTitle + ' Date Posted: '+ datePosted+' Wordcount: ' + str(chapterWordcount))
        blob = (str(idCounter),chapterTitle,curUrl,chapterString,str(chapterWordcount),datePosted,book,)
        db.execute("INSERT OR IGNORE INTO chapters(id, title, url, content, wordcount, datePosted, book) values (?,?,?,?,?,?,?);", blob)
        idCounter += 1
        # +','+
        # str(idCounter)+','+chapterTitle+','+chapterString+','+str(chapterWordcount)+','+datePosted+','+str(isBonus)+','+str(volume)
        # storyFile.write(chapterString)

        tempURL = soup.select('.entry-content p a')
        for i in range(0, len(tempURL), 1) :
            temp = tempURL[i]
            if("Next" in str(temp)):
                nextURL=str(tempURL[i].get('href'))
                #nextURL=nextURL.replace('.wordpress.com','.net')
                break
        if(curUrl == nextURL):
            finalPage = True
            break
        else:
            #print(nextURL)
            curUrl = nextURL
            tempRes = session.get(nextURL)
            soup = bs4.BeautifulSoup(tempRes.text, "html.parser")

            
    conn.commit()
    conn.close()

        





#Main

#sburl=input()
kataurl="https://katalepsis.net/2019/02/02/mind-correlating-1-1/"
ficFile = ".\\Kata"
start = time.time()
print('Starting...\n\n')
session = requests.Session()
session.get(kataurl)
parseKata(kataurl)
print('All done!')
end = time.time()
print('Elapsed time: '+(str(end - start)))
