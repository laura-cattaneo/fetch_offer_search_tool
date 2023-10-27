# Offer Search Tool Usage Instructions
search(.py) is used to find offers in the Fetch app. The command line tool requires a user to enter two arguments - a search type and a search term along preceded by 'python' and the script name.  
The first argument, the search type (-t) is the type of search term the user is looking for and must be either 'Category', 'Brand', or 'Retailer'. If the category is misspelled, the user is asked to resubmit the name.  
The second argument, the search term (-s), is the item, brand name, or retailer name the user is interested in finding offers for. Be sure to enter this term in quotations like "example term", otherwise the system will not work. If the search term does not exist in the search type the tool will prompt the user to retry the search. 

The tool returns the most relevant offers and the cosine similarity of the offer to the search term.  

Please see the WriteUp.md file for a discussion of my problem approach, assumptions, and future work.  

## Installation
The required packages are listed in the fetch.yml file. If using conda you can create an environment using the command: 'conda env create -f fetch.yml' and then 'conda activate fetch_env'  

If you are using pip, I recommend using python 3.9, and then the following packages:  
- ipython==8.15, ipykernel==6.25 (only needed if you want to run the notebooks)
- textdistance==4.2.1, gensim==3.8.1, texthero==1.1.0, tensorflow==2.14.0, tensorflow-hub==0.15.0
Note: I struggled to get texthero to install, unless I installed gensim first and used python 3.9 (nothing higher). 


## Execution
Execute the search(.py) script specifying the 't' and 's' parameters explained below.

usage: search.py [-h] t s  
Example: python search.py category "tea"  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; python search.py retailer "Target"
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; python search.py brand "Casey's General Store"

positional arguments:  
  t &nbsp;&nbsp;&nbsp; Search Type to use. Must select from 'Category', 'Brand', or 'Retailer'  

  s &nbsp;&nbsp;&nbsp; Search term of interest enclosed in quotations "example search term"

optional arguments:  
  -h, --help &nbsp;&nbsp;&nbsp; show this help message and exit

