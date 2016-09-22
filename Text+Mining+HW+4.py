
# coding: utf-8

# In[1]:

import twitter

def oauth_login():
   
    #define twitter API app credentials 
    
    CONSUMER_KEY = 'jfrYegHout1Ysl17jvBD5vJzU'
    CONSUMER_SECRET = 'uW7v5O1jIRgNYeD20InorRxjjvt2TNRUpWGdCLuScr00JX4qQh'
    OAUTH_TOKEN = '14551746-iq4AbAXRI5ZBN1GkZoyaLjdf3MFD0YoLX4rEvkLFb'
    OAUTH_TOKEN_SECRET = 'X1RcW3EGFvkorrrRoyjNPQD0fTMTO0Tzl08QhIMp2YUUa'
    
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

# Sample usage
twitter_api = oauth_login()    

# Nothing to see by displaying twitter_api except that it's now a
# defined variable

print (twitter_api)


# In[2]:

import json
#define twitter search function 
def twitter_search(twitter_api, q, max_results=1000, **kw):  

    search_results = twitter_api.search.tweets(q=q, count=200, **kw)
    
    statuses = search_results['statuses']
    
    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval. See
    # https://dev.twitter.com/docs/rate-limiting/1.1/limits
    # for details. A reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.
    
    # Enforce a reasonable limit
    max_results = min(1000, max_results)
    
    for _ in range(5): # 5*200 = 1000
        print "Length of statuses", len(statuses)
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: # No more results when next_results doesn't exist
            break
            
        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=') 
                        for kv in next_results[1:].split("&") ])
        
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']
        
        if len(statuses) > max_results: 
             break
            
        
            
    return statuses

# Sample usage

twitter_api = oauth_login()

q = "@HillaryClinton"
Clinton_results = twitter_search(twitter_api, q)  

q = "@realDonaldTrump"
Trump_results = twitter_search(twitter_api, q )  
        
# Show one sample search result by slicing the list...
print (json.dumps(Clinton_results[0], indent=1))
print (json.dumps(Trump_results[0], indent=1))


# In[3]:

with open('C:\Users\Public\Documents\Python Scripts\Clinton.json', 'w') as outfile:
    json.dump(Clinton_results, outfile) #save to file
    
with open('C:\Users\Public\Documents\Python Scripts\Trump.json', 'w') as outfile:
    json.dump(Trump_results, outfile)    #save to file


# In[19]:

import json
 
with open('C:\Users\Public\Documents\Python Scripts\Clinton.json', 'r') as f:
    line = f.readline() # read only the first tweet/line
    tweet = json.loads(line) # load it as Python dict
    print(json.dumps(tweet, indent=4)) # pretty-print


# In[22]:

with open('C:\Users\Public\Documents\Python Scripts\Trump.json', 'r') as f:
    line = f.readline() # read only the first tweet/line
    tweet = json.loads(line) # load it as Python dict
    print(json.dumps(tweet, indent=4)) # pretty-print


# In[15]:

import re
 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens



# In[ ]:

import nltk
nltk.download() 


# In[16]:

from nltk.corpus import stopwords
import string
 
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']
stop += ['.',',','"',"'",'!','?','td',':',';','de',"it's",'en','RT','@HillaryClinton','@realDonaldTrump','I','This','A','amp','\u2026','ud83c','ud83d','In',]


# In[20]:

import operator 
from collections import Counter
fname = 'C:\Users\Public\Documents\Python Scripts\Clinton.json'
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        tweet = json.loads(line)
        
        # Create a list with all the hashtags
        terms_hash = [term for term in preprocess(tweet['text']) 
              if term.startswith('#')]
      
        # Update the counter
        count_all.update(terms_hash)
      
    # Print the first 20 most frequent hashtags
     
    print(count_all.most_common(20))
   
  


# In[23]:

fname = 'C:\Users\Public\Documents\Python Scripts\Clinton.json'
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        tweet = json.loads(line)
        
        # Create a list of 20 most common words, excluding stop words
        terms_stop = [term for term in preprocess(tweet['text']) 
            if term not in stop and
            not term.startswith(('#','By','ha','Has'))]
        
        # Update the counter
        count_all.update(terms_stop)
      
    # Print the first 20 most common words
     
    print(count_all.most_common(20))


# In[ ]:

fname = 'C:\Users\Public\Documents\Python Scripts\Trump.json'
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        tweet = json.loads(line)
        
        # Create a list with all the hashtags
        terms_hash = [term for term in preprocess(tweet['text']) 
              if term.startswith('#')]
      
        # Update the counter
        count_all.update(terms_hash)
      
    # Print the first 20 most frequent hashtags
     
    print(count_all.most_common(20))


# In[24]:

fname = 'C:\Users\Public\Documents\Python Scripts\Trump.json'
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        tweet = json.loads(line)
        
        # Create a list of 20 most common words, excluding stop words
        terms_stop = [term for term in preprocess(tweet['text']) 
            if term not in stop and
            not term.startswith(('#','By','ha','Has'))]
        
        # Update the counter
        count_all.update(terms_stop)
      
    # Print the first 20 most common words
     
    print(count_all.most_common(20))


# In[26]:

from collections import defaultdict
 
com = defaultdict(lambda : defaultdict(int))

fname = 'C:\Users\Public\Documents\Python Scripts\Clinton.json'
with open(fname, 'r') as f:
    search_word = '#ImWithHer' #sys.argv[1] # pass a term as a command-line argument
    count_search = Counter()

# f is the file pointer to the JSON data set
    for line in f: 
        tweet = json.loads(line)
        terms_only = [term for term in preprocess(tweet['text']) 
                  if term not in stop 
                  and not term.startswith(('@', 'https'))]
        if search_word in terms_only:
            count_search.update(terms_only)
       

    # Build co-occurrence matrix
    for i in range(len(terms_only)-1):            
        for j in range(i+1, len(terms_only)):
            w1, w2 = sorted([terms_only[i], terms_only[j]])                
            if w1 != w2:
                com[w1][w2] += 1


# In[ ]:

com_max = []
# For each term, look for the most common co-occurrent terms
for t1 in com:
    t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
    for t2, t2_count in t1_max_terms:
        com_max.append(((t1, t2), t2_count))
# Get the most frequent co-occurrences
terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
print(terms_max[:5])
print("Co-occurrence for %s:" % search_word)
print(count_search.most_common(20))# most frequent co-occurences with #ImWithHer


# In[ ]:

fname = 'C:\Users\Public\Documents\Python Scripts\Trump.json'
with open(fname, 'r') as f:
    search_word = '#ImWithHer' #sys.argv[1] # pass a term as a command-line argument
    count_search = Counter()

# f is the file pointer to the JSON data set
    for line in f: 
        tweet = json.loads(line)
        terms_only = [term for term in preprocess(tweet['text']) 
                  if term not in stop 
                  and not term.startswith(('@', 'https'))]
        if search_word in terms_only:
            count_search.update(terms_only)
       

    # Build co-occurrence matrix
    for i in range(len(terms_only)-1):            
        for j in range(i+1, len(terms_only)):
            w1, w2 = sorted([terms_only[i], terms_only[j]])                
            if w1 != w2:
                com[w1][w2] += 1


# In[ ]:

com_max = []
# For each term, look for the most common co-occurrent terms
for t1 in com:
    t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
    for t2, t2_count in t1_max_terms:
        com_max.append(((t1, t2), t2_count))
# Get the most frequent co-occurrences
terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
print(terms_max[:5])
print("Co-occurrence for %s:" % search_word)
print(count_search.most_common(20))# most frequent co-occurences with #ImWithHer


# In[27]:

import vincent
 
with open(fname, 'r') as f:
 count_all = Counter()
 for line in f:
     tweet = json.loads(line)
     tokens = [term for term in preprocess(tweet['text'])
if term not in stop and
 not term.startswith(('#', '@'))]
count_all.update(tokens)
word_freq = count_all.most_common(20)
labels, freq = zip(*word_freq)
data = {'data': freq, 'x': labels}
bar = vincent.Bar(data, iter_idx='x')
bar.to_json('term_freq.json')
print(bar.to_json)


# In[ ]:

import vincent
 
with open(fname, 'r') as f:
 count_all = Counter()
 for line in f:
     tweet = json.loads(line)
     tokens = [term for term in preprocess(tweet['text'])
              if term.startswith('#')]
count_all.update(tokens)
word_freq = count_all.most_common(20)
labels, freq = zip(*word_freq)
data = {'data': freq, 'x': labels}
bar = vincent.Bar(data, iter_idx='x')
bar.to_json('term_freq.json')


# In[28]:

# Tweets are stored in "fname"
with open(fname, 'r') as f:
    geo_data = {
        "type": "FeatureCollection",
        "features": []
    }
    for line in f:
        tweet = json.loads(line)
        if tweet['coordinates']:
            geo_json_feature = {
                "type": "Feature",
                "geometry": tweet['coordinates'],
                "properties": {
                    "text": tweet['text'],
                    "created_at": tweet['created_at']
                }
            }
            geo_data['features'].append(geo_json_feature)
 
# Save geo data
with open('geo_data.json', 'w') as fout:
    fout.write(json.dumps(geo_data, indent=4))

print(geo_data)


# In[ ]:



