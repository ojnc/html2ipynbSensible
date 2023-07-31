import re
import datetime
import time
import sys

from bs4 import BeautifulSoup
import json
import urllib.request

def doMarsa(URL,prefix):
    # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11'\
    #            '(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    #            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    #            'Accept-Encoding': 'none',
    #            'Accept-Language': 'en-US,en;q=0.8',
    #            'Connection': 'keep-alive'}
    # req = urllib.request.Request(url, headers=headers)

    page = urllib.request.urlopen(URL)
    text = page.read()

    soup = BeautifulSoup(text, 'lxml')

    create_nb = {'nbformat': 4, 'nbformat_minor': 2, 
                  'cells': [], 'metadata': 
                 {"kernelspec": 
                  {"display_name": "Python 3", 
                   "language": "python", "name": "python3"
      }}}


    def get_data(soup, content_class):
        for pre in soup.find_all('pre', 
                                 attrs={'class': content_class}):
            
            code_chunks = pre.find_all('code')
            
            for chunk in code_chunks:
                cell_text = ' '
                cell = {}
                cell['metadata'] = {}
                cell['outputs'] = []
                cell['source'] = [chunk.get_text()]
                cell['execution_count'] = None
                cell['cell_type'] = 'code'
                create_nb['cells'].append(cell)


    get_data(soup, "language-python")

    with open(prefix+"marsja.ipynb","w",encoding="utf-8") as jynotebook:
        jynotebook.write(json.dumps(create_nb))

    create_nb

####### MAIN ######
if __name__ == '__main__':

  start_time = time.time()

  if len(sys.argv) !=3:
    print("Invoke as: python marsja.py URL PREFIX\n",file=sys.stderr,flush=True)
    exit(1)

  doMarsa(sys.argv[1],sys.argv[2]) ## URL PREFIX

  print("\n%s Jai Hind! %5.2f seconds --- \n"
        % (time.strftime("%Y-%m-%d %H:%M"),(time.time() - start_time)),file=sys.stderr,flush=True)