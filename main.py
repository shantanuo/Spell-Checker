import hunspell
from bs4 import BeautifulSoup
import requests
import re
from flask import Flask, render_template, request
import csv, nltk

app = Flask(__name__)

spellchecker = hunspell.HunSpell(
    "./marathi_words_updates.oxt_FILES/dicts/mr_IN.dic",
    "./marathi_words_updates.oxt_FILES/dicts/mr_IN.aff",
)

spellchecker_split = hunspell.HunSpell(
    "./marathi_words_updates.oxt_FILES/dicts/mr_IN.dic",
    "./marathi_words_updates.oxt_FILES/dicts/mr_IN_split.aff",
)
words = list()

@app.route('/')
def index():
    return render_template("index.html")

from collections import defaultdict
mydict = defaultdict(list)

with open("marathi_bigram_count.txt", newline='') as f:
    for row in csv.reader(f, delimiter = ' '):
        mydict[row[0].strip()].append(row[1].strip())

def mycheck(myword):
    matches = re.findall('[१२३४५६७८९०1234567890]',  myword[1])
    if spellchecker.spell(myword[1]) is False and len(myword[1]) > 2 and len(matches) < 1:
        try:
            if len(myword[1]) > 12:
                word_result = {
                    'original_word': myword[1],
                    'corrected_word': spellchecker_split.suggest(myword[1])
                }
            else:
                word_result = {
                    'original_word': myword[1],
                    'corrected_word': spellchecker.suggest(myword[1])
                }

            result = mydict[myword[0]]

            list_one_updated = list()
            for i in word_result['corrected_word']:
                if i in result:
                    list_one_updated.append(i)

            for i in word_result['corrected_word']:
                if i not in result:
                    list_one_updated.append(i)

            import Levenshtein
            words.append({'original_word': myword[1], 'corrected_word': (list_one_updated[0], Levenshtein.distance(myword[1], list_one_updated[0])) })
                    
            return
        except:
            pass


@app.route('/process', methods=['POST', 'GET'])
def process():
    if request.method == 'POST':
        from collections import defaultdict
        mydict = defaultdict(list)

        with open("marathi_bigram_count.txt", newline='') as f:
            for row in csv.reader(f, delimiter = ' '):
                mydict[row[0].strip()].append(row[1].strip())
                
        url = request.form['url']
        print(url)
        headers = requests.utils.default_headers()
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        words.clear()
        p = re.compile(r"[^\u0900-\u097F\n]")
        for line in text.splitlines():
            cleaned = p.sub(" ", line)
            if cleaned.strip():
                mycheck(('NULL', cleaned.split()[0]))
                for i in nltk.bigrams(cleaned.split()):
                    mycheck(i)
#        words1 = list({v['original_word']:v for v in words}.values())
#        words2 = sorted(words1, key=lambda x: x['corrected_word'][1])

        from collections import Counter
        ctr = Counter(((item['original_word'], *item['corrected_word']) for item in words))

        words2 = sorted([
            {'original_word': ow, 'corrected_word': (*cw, count)} for (ow, *cw), count in ctr.items()
            ], key=lambda item: item['corrected_word'][1])

        return render_template("success.html", words=words2)
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

