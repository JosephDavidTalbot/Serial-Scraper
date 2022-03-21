# Serial Scraper
 Scrapes the contents of a web serial into a SQLite database, to then run complicated queries on it.

 Began life as an answer to the question "What's the wordcount of 'The Gods Are Bastards' by D.D. Webb?" before I realized that, with the power of the many SQL courses I've had to take in college, I could potentially ask and answer MUCH more complicated and interesting questions than that. So I looked up the Python SQLite documentation, put on a pot of coffee, and three hours later, this baby was born.

 After a few months, I realized that this technique could be refined into something actually useful, and so the RoyalRoad scraper was born. It's kind of like an RSS reader, in that it stores a list of your subscribed stories, but instead of alerting you to updates, you instead have to run it yourself on a semi-regular basis, with the upside of the scraper compiling EPUB files of the stories on your behalf.
