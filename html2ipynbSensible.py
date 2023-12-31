import re
import datetime
import time
import sys

from urllib.request import Request, urlopen
import html2text
# https://fossies.org/linux/html2text/docs/usage.md

##################### py2nb  START ###################
# https://github.com/williamjameshandley/py2nb/blob/master/py2nb
import os
import nbformat.v4

ACCEPTED_CHARS = ['#-', '# -']
MARKDOWN_CHARS = ['#|', '# |']
ACCEPTED_CHARS.extend(MARKDOWN_CHARS)

def new_cell(nb, cell, markdown=False):
    """ Create a new cell

    Parameters
    ----------
    nb: nbformat.notebooknode.NotebookNode
        Notebook to write to, as produced by nbformat.v4.new_notebook()

    cell: str
        String to write to the cell

    markdown: boolean, optional, (default False)
        Whether to create a markdown cell, or a code cell
    """
    cell = cell.rstrip().lstrip()
    if cell:
        if markdown:
            cell = nbformat.v4.new_markdown_cell(cell)
        else:
            cell = nbformat.v4.new_code_cell(cell)
        nb.cells.append(cell)
    return ''

def str_starts_with(string, options):
    for opt in options:
        if string.startswith(opt):
            return True


def convert(script_name):
    """ Convert the python script to jupyter notebook"""
    with open(script_name,"r",encoding="utf-8") as f:
        markdown_cell = ''
        code_cell = ''
        kernelspec=dict(display_name= "Python 3", 
                        language= "python", 
                        name= "python3",)
        nb = nbformat.v4.new_notebook()
        nb.metadata['kernelspec'] = kernelspec
        for line in f:
            if str_starts_with(line, ACCEPTED_CHARS):
                code_cell = new_cell(nb, code_cell)
                if str_starts_with(line, MARKDOWN_CHARS):
                    # find the first occurence of |
                    # and add the rest of the line to the markdown cell
                    markdown_cell += line[line.index('|') + 1:]
                else:
                    markdown_cell = new_cell(nb, markdown_cell, markdown=True)
            else:
                markdown_cell = new_cell(nb, markdown_cell, markdown=True)
                code_cell += line

        markdown_cell = new_cell(nb, markdown_cell, markdown=True)
        code_cell = new_cell(nb, code_cell)

        notebook_name = os.path.splitext(script_name)[0] + '.ipynb'
        nbformat.write(nb, notebook_name)

##################### py2nb  FINIS ###################

def downLoad(myURL,prefix): 

  # orih=open("kpHTML.txt","w",encoding="utf-8")
  outh=open(prefix+"HTML.txt","w",encoding="utf-8") 
  request_site = Request(myURL, headers={"User-Agent": "Mozilla/5.0"})

  with urlopen(request_site) as response:
    print("result code: " + str(response.getcode()))
    html_content = response.read()
    encoding = response.headers.get_content_charset('utf-8')
    html_text = html_content.decode(encoding)
    # print(html_text,file=orih,flush=True)
    # orih.close()
  
  print(html_text,file=outh,flush=True)
  outh.close()

  inph=open(prefix+"HTML.txt","r",encoding="utf-8")
  orih=open(prefix+"KEEP1.txt","w",encoding="utf-8") 
  outh=open(prefix+"FINAL.py","w",encoding="utf-8") 

  html=inph.read()

  text_maker = html2text.HTML2Text()
  text_maker.ignore_links = True
  text_maker.ignore_images = True
  text_maker.escape_snob = True
  text_maker.skip_internal_links = True
  text_maker.ignore_tables = True
  text_maker.single_line_break = True
  text_maker.mark_code = True
  text_maker.wrap_links = True
  text_maker.ul_item_mark = "-"


  # text_maker.ignore_links=True
  # text_maker.bypass_tables=True
  # text_maker.ignore_tables=True

  text_maker.body_width=132
  text=text_maker.handle(html)

  print(text,file=orih,flush=True)

  outarr=[]
  inparr=text.split('\n')
  skip=False
  out=False

  for onestr in inparr:
    onestr=re.sub(r'\s+$','',onestr)
    if len(onestr) > 0:
      outarr.append(onestr)
      # print(onestr,file=outh,flush=True)

  code=False  
  mark=True   #markdown cell

  for onestr in outarr:    
    if re.search(r'Alert Moderator',onestr) != None:
      break
    if re.search(r'^\[code',onestr) != None:
      code=True
      mark=False
      continue
    if re.search(r'^\[/code',onestr)!= None:
      code=False
      mark=True
      continue
    if code:
      onestr=re.sub(r'^\s{4}','',onestr)
      print(onestr,file=outh,flush=True)
      continue
    if mark:
      print("#| "+onestr,file=outh,flush=True)
      continue

  outh.close()
  inph.close()

  convert(prefix+"FINAL.py")


  outh.close()
  inph.close()

  # convert("myTEXT.py")

####### MAIN ######
if __name__ == '__main__':

  start_time = time.time()

  if len(sys.argv) !=3:
    print("Invoke as: python html2ipynbSensible.py URL PREFIX\n",file=sys.stderr,flush=True)
    exit(1)

  downLoad(sys.argv[1],sys.argv[2]) ## URL PREFIX

  print("\n%s Jai Hind! %5.2f seconds --- \n"
        % (time.strftime("%Y-%m-%d %H:%M"),(time.time() - start_time)),file=sys.stderr,flush=True)



