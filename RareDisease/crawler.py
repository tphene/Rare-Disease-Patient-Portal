import newspaper
import google
import re
from bs4 import BeautifulSoup


therapists = ['Physiotherapist', 'respiratory therapist', 'Hematologist']
for p in therapists:
    search_results = google.search(p+" salary department of labor", stop=1, lang="en")
    print("*"*30)
    print(p.upper())
    print("_"*15)
    for link in search_results:
        #print(link)
        data = newspaper.Article(url=link)
        data.download()
        text=data.html
        soup = BeautifulSoup(text, 'html.parser')
        rows = soup.find_all('p')
        for tr in rows:
            if 'The median annual wage' in str(tr):
                print(str(tr).split(" ")[-4])
                break
        break
