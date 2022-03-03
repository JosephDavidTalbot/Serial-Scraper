import os, time, datetime, string, unicodedata, sqlite3, ebooklib, dateparser
from sqlite3 import Error
from ebooklib import epub
from datetime import datetime

def parseSQLite(db_path, title):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
    except Error as e:
        print(e)
        return
    
    db = conn.cursor()
    #db.execute()
    
    #Select titles and chapter text for each chapter from the database
    db.execute("select id, title, content, datePosted from chapters")
    chapters = db.fetchall()
    conn.close()

    #Set up epub
    book = epub.EpubBook()
    book.set_identifier(title)
    book.set_title(title)
    book.set_language('en')

    #For each chapter, insert into epub
    book_chapters = ['nav']
    for chapter in chapters:
        #print('Adding chapter '+str(chapter[0]))
        tempFile = str(chapter[0])+'.html'
        temp = epub.EpubHtml(title=chapter[1], file_name=tempFile, lang='en')
        #print(type(temp))
        #timestamp = datetime.strptime(chapter[3], '%Y-%m-%dT%H:%M:%S.%fZ')
        timestamp = dateparser.parse(chapter[3])
        timestamp = "Posted on "+timestamp.strftime("%A, %B %e, %Y. %I:%M%p")
        tempString = '<html><body><h1>'+chapter[1]+'</h1><h3><em>'+timestamp+'</em></h3>'+chapter[2]+'</body></html>'
        temp.content = tempString
        book_chapters.append(temp)
        #print(temp.content)
        book.add_item(temp)
    
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    style = 'BODY {color: white;}'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    book.toc = book_chapters
    book.spine = book_chapters
    #for item in book.get_items():
        #if item.get_type() == ebooklib.ITEM_DOCUMENT:
            #print('NAME : ', item.get_name())
            #print('CONTENT: ', item.get_content())
    epub.write_epub('.\\'+title+'\\'+title+'.epub', book, {})
    print("Epub for "+title+" successfully baked!")
        





#Main


#start = time.time()
#print('Starting...\n\n')
#parseSQLite(".\\PGTE\\wordcount.db")
#print('All done!')
#end = time.time()
#print('Elapsed time: '+(str(end - start)))
