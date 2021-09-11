import requests, bs4, webbrowser, os, time, string, unicodedata, sqlite3
from sqlite3 import Error

def parseTGAB(tgaburl):
    curUrl = tgaburl
    res = session.get(tgaburl)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    conn = None
    try:
        conn = sqlite3.connect(".\\TGAB\\wordcount.db")
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
                isBonus integer,
                book integer,
                volume integer
                ); """)
    conn.commit()
    idCounter = 0 #Chapter ID is zero-indexed and represents order of posting.
    volume = 0 #Volume starts at 0 but is one-indexed.
    # This allows Volume 1 Prologue to work as intended without special code.
    finalPage = False
    

    while (not finalPage):
        soup.find('div', id="jp-post-flair").decompose()
        chapter=soup.select('.entry-content')[0]
        # chapter.find('div', id="jp-post-flair").decompose()
        chapterString=chapter.getText()

        chapterTitle = str(soup.select('.entry-title')[0].getText())
        if('Prologue' in chapterTitle):
            volume += 1
            print('Begin Volume '+str(volume))
        isBonus = 0
        book = None
        if('Bonus' in chapterTitle):
            isBonus = 1
        else:
            if('Prologue' not in chapterTitle):
                if('Epilogue' not in chapterTitle):
                    book = chapterTitle.replace('-',' ')
                    book = book.split()[0]
            
                

        wordcountString = chapterString.split()
        chapterWordcount = len(wordcountString)

        datePosted = soup.find('time').attrs['datetime']

        print(chapterTitle + ' Date Posted: '+ datePosted+' Wordcount: ' + str(chapterWordcount))
        blob = (str(idCounter),chapterTitle,curUrl,chapterString,str(chapterWordcount),datePosted,str(isBonus),book,str(volume))
        db.execute("INSERT OR IGNORE INTO chapters(id, title, url, content, wordcount, datePosted, isBonus, book, volume) values (?,?,?,?,?,?,?,?,?);", blob)
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
tgaburl="https://tiraas.wordpress.com/2014/08/20/book-1-prologue/"
start = time.time()
print('Starting...\n\n')
session = requests.Session()
session.get(tgaburl)
parseTGAB(tgaburl)
print('All done!')
end = time.time()
print('Elapsed time: '+(str(end - start)))
