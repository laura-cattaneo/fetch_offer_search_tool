#!/usr/bin/env python

######################################################################
# Imports
######################################################################
import os, argparse, sys, logging, platform, ast
import json
import texthero as hero 
import pandas as pd
from scipy.spatial.distance import cosine
from textdistance import levenshtein
pd.set_option('display.max_colwidth', 100)

######################################################################
# Constants
######################################################################
SVersion = "v1.0.0"
SInfo = """
{} some parameter example 
""".format(os.path.basename(__file__))
copyright = "Laura's Fetch Data Task"


######################################################################
# Option Parser
######################################################################
def ParseOptions(args):
    """
    Parse the options using argparse
    """
    p=argparse.ArgumentParser(description="{}".format(SInfo))
    p.add_argument("t",help="Search Type to use. Must select from 'Category', 'Brand', or 'Retailer'",type=str)
    p.add_argument("s",help="Search term of interest",type=str)
    options=p.parse_args(args)
    #print("Exit ParseOptions")
    return options


######################################################################
# Option Verifier
######################################################################
def getOptions(args):
    """
    Obtain and validate options beyond what argparse provides. 
    """ 
    d_opt=vars(ParseOptions(args))
    term_options = ['CATEGORY', 'BRAND', 'RETAILER']
    d_opt["t"] = d_opt["t"].upper()

    if d_opt["t"] not in term_options:
        logging.warning("Search term entered is not 1 of the 3 options. Try again with either 'Category', 'Brand', or 'Retailer'")
        sys.exit(1)
    
    #print("Exit Data Verification")
    return d_opt      


######################################################################
# Functions
######################################################################
def run_search(odic, df_final):
    arbitrary_cutoff = 0.65
    # ^ I did manual review to determine this is where I wanted to cutoff. 
    # With more time I would have run all data, looked at distributions, and chosen a more scientific cutoff. 
    type_search = odic['t']
    search_term = odic['s']

    search_term = hero.clean(pd.Series(search_term))
    df_final = df_final[df_final[type_search].notna()]
    df_final['search'] = df_final.apply(lambda x: levenshtein.distance(x[type_search],  search_term[0]), axis=1)

    df_final_offers = pd.DataFrame()

    if len(df_final[df_final['search'] == 0]) > 0:
        for index, row in df_final[df_final['search'] == 0].iterrows():
            comparison = row['use']
            df_final_sim = df_final
            df_final_sim['similarity'] = df_final_sim.apply(lambda row: 1 - cosine(row['use'], comparison), axis=1)
            df_final_sub = df_final_sim[df_final_sim['similarity']>= arbitrary_cutoff]

            df_final_offers = pd.concat([df_final_offers, df_final_sub])
            
        df_final_offers['use'] = df_final_offers['use'].astype(str)
        df_final_offers = df_final_offers.sort_values(by = 'search')
        df_final_offers = df_final_offers.drop_duplicates(subset = ['use'])
        df_final_offers1 = df_final_offers.sort_values(by = ['search', 'similarity'], ascending= [True, False])
    else:
        logging.warning(f"\nYour search term ({odic['s']}) is not in the search type, includes punctuation, is misspelled, or doesn't exist in the offers data."
                        "\nChecking your spelling, remove punctuation, try a new search term, or change your type - "
                        f"maybe your search term ({odic['s']}) is in a different search type (instead of in {odic['t']})")
        logging.warning("\nFor example, target will not show up in Brand, but will show up in Retailer.")
        sys.exit(1)
    return df_final_offers1

######################################################################
# Main
######################################################################
def main(args):
    odic =getOptions(args)
    logging.info(f"Command Line Options: {json.dumps(odic,default=str,indent=2)}")
    file = os.path.dirname(os.path.abspath(__file__))
    # Hoping to make this useable regardless of the machine it is run on.
    platform_type = '\\' if platform == 'Windows' else '/'
    data = pd.read_csv(file+platform_type+'SearchData.csv')
    data['use'] = data['use'].apply(ast.literal_eval)

    results = run_search(odic, data)
    print(results[['OFFER', odic['t'], 'search', 'similarity']])
    logging.info(results[['OFFER', odic['t'], 'search', 'similarity']])
    print('done')

######################################################################
# Entry Point
######################################################################
if __name__ == '__main__':
    print("{}\n{}: {}".format(copyright,os.path.basename(__file__),SVersion))
    main(sys.argv[1:])