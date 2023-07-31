# How to convert HTML to Jupyter Notebook IPYNB with all the Author’s text
This is an utility that worked very well in converting  HTML to Jupyter Notebook IPYNB with all the Author's text for 3 SAP blogs I tried

Will be very helpful for many blogs with the current thrust in Data Science and Data Engineering; reader wishes to try but copy paste painful
Without lots of comments (read markdown) only code is almost useless!


Did a lot of searching and found NOTHING that met my needs
Nearest was https://www.marsja.se/converting-html-to-a-jupyter-notebook/
His notebook is in https://github.com/marsja/jupyter/blob/master/convert_html_jupyter_notebook_tutorial.ipynb

I converted that to marsja.py adapted for SAP Blogs where code is
inside pre tags as you can see in the HTML files

marsja,py works but gives a notebook with only code cells;
to my mind not too helpful; uses beautifulsoup and lxml packages 

Please head to my repository https://github.com/ojnc/html2ipynbSensible

My html2ipynbsensible.py gives exactly what most people need
A python notebook with lots of markup

I used the excellent package html2text which you need to install 
pip install html2text
Documentation in https://fossies.org/linux/html2text/docs/usage.md

2nd package you do not need to install is py2nb https://github.com/williamjameshandley/py2nb/blob/master/py2nb
Wonderful compact but delivered as a python script
I had to copy paste in my program
Have informed Author about the 3 Issues that compelled me to copy


I ran 4 commands


### APL1 Hands-On Tutorial: Automated Predictive (APL) in SAP HANA Cloud
python html2ipynbSensible.py "https://blogs.sap.com/2020/07/27/hands-on-tutorial-automated-predictive-apl-in-sap-hana-cloud/" APL1

### PAL1 Hands-On Tutorial: Leverage SAP HANA Machine Learning in the Cloud through the Predictive Analysis Library
#### Author has CODE as images
#### He has provided the ipynb
python html2ipynbSensible.py "https://blogs.sap.com/2021/02/25/hands-on-tutorial-leverage-sap-hana-machine-learning-in-the-cloud-through-the-predictive-analysis-library/" PAL1

### APL2 Multiclass Classification with APL (Automated Predictive Library)
python html2ipynbSensible.py "https://blogs.sap.com/2022/04/01/multiclass-classification-with-apl-automated-predictive-library/" APL2

### APL2 as bare code by marsja.py
python marsja.py "https://blogs.sap.com/2022/04/01/multiclass-classification-with-apl-automated-predictive-library/" APL2

The output files are in this repository
You should examine at least APL1 if you wish to use and adapt

Github has excellent jupyter notebook rendition
See these
## output of html2ipynbsensible.py
APL1FINAL.ipynb
APL2FINAL.ipynb

## output of marsja.py ONLY CODE no FUN!
APL2marsja.ipynb


## executed with editing just user ML_USER and connection MYHANACLOUD 
runAPL1FINAL.ipynb
runAPL2FINAL.ipynb
runAPL2marsja.ipynb

my saved connection is MYHANACLOUD and saved user ML_USER

Not fortunate enough to have Cloud BTP access and I have a P-ID
so I used HANA EXPRESS in my personal docker
https://blogs.sap.com/2023/07/20/my-success-with-hana-express/

I hope many use this utility which I wrote definite for my self

For external notebooks where HTML is not as "nice" as SAP Blogs
you can adapt the python program by looking at the HTML.txt
Find how the code cells are organized in the HTML
Skill in Python REGEX will help a lot
