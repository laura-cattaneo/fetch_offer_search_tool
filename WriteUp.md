# Offer Search Tool Write Up
A brief summary of the approach, as well as discussion around assumptions I made and challenges I faced. 

## Approach
In order to build a tool that allows users to intelligently search for offers via text input from the users, I created a multi-step solution.  

First, using the 3 datasets provided, I built a final dataset with embeddings of each offer that is used by the search tool. While building the search tool, I experimented with the raw embeddings and dimension reduced embeddings (specifically using pca and tsne), but found the best results with the raw embeddings. On this small dataframe I did not have processing speed issues, but I recognize that at scale this may not hold.  
The work to create the final dataframe including the embeddings can be found in the Data_Prep.ipynb notebook. To replicate it, a new user will need to change the paths. 

Prior to merging the datasets, I did extensive exploratory data analysis to understand how to best merge, and what columns I might need. I also tried to understand each column since a data dictionary was not provided. The column 'RECEIPTS' in the brand_category.csv file remains a mystery to me. After manual review I wondered if the number may have something to do with the brand category, as it seemed like lower numbers were more often associated with drinks, but a quick clustering attempt did not reveal anything. I therefore ignored the column and moved on.  

My approach to finding offers that are relevant to the search type (category, brand or retailer) is multi-fold. First, I wanted to narrow the space down to the rows most relevant to the search word. For example, if a user searches 'sports drinks' in the category type, then I want to find all relevant offers as well as offers that are similar to sports drinks offers, like carbonated soft drinks offers.  
In order to find the search term in the search type (category, brand or retailer), I use levenshtein distance. I experimented with different cutoffs for maximum distance, as well as fuzzy search alternatives, but decided only to use the rows that perfectly match the search term. This introduces a large limitation in my approach, but I decided to focus on returning the most similar offers instead of tuning the search mechanism.  

Once I had the rows that match the search term, I looped through the embeddings (extracted in the Date_Prep.ipynb notebook) of these rows and compared them to all the other rows in the dataframe. This allows me to find the most similar offers to the offers for the search term. For example, when considering a retailer, a user may be interested in deals at Target like the "Beyond Steak™ Plant-Based seared tips, 10 ounce at Target" but I want the tool to also return a simlar deal like "Beyond Steak™ Plant-Based seared tips, 10 ounce at H-E-B". I chose 0.65 as a cutoff for the cosine similarity value based on manual review. With more time I could get a slightly less arbitrary and hopefully more scientific answer by checking distributions, speaking with internal stakeholders, surveying customers, etc.   



## Limitations
My approach does not allow for misspelled (or punctuated) categories or search terms.  

I chose to treat the category search, brand search, and retailer search separately, since a user has to select the search type and the search word only looks in this type. In a traditional search engine I'd want to make a solution that allows for all 3 simultaneously.

I take a conservative approach to offers returned. I would rather return too many offers than too few. My manual review suggests that while it's not perfect, finding similar embeddings does return offers in similar categories, brands, and retailers. For example, along with all of the offers for 'carbonated soft drinks', I return an offer for sports drinks, and (erroneously) cooking baking.  

## Future Work
Beyond addressing the above limitations, I'd like to do more robust experimentation on which model to use to gather the embeddings. It may not make a difference, but I chose the universal sentence encoder because I have previously had success using it on contact center sentences in my role at Calabrio.  
I'd also like to return to the dimension reduction work and see if a model besides principal component analysis may work better. 