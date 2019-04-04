from sqlalchemy import create_engine
from shutil import copyfile
from langdetect import detect # Detect language
import shutil # To remove folders
import re
import os
import git # To clone and download the csv files
import urllib.request # Download images
import pandas as pd

def get_cover(row):
    punctuation_pattern = r"[^\w\s]"
    title = re.sub(punctuation_pattern,'',row.title).strip()
    auth = re.sub(punctuation_pattern,'',row.authors).strip()
    filename = title+' by '+auth+'.jpg'
    try:
        urllib.request.urlretrieve(row.image_url,filename)
    except:
        print('image url not found: ', row.image_url)
        filename = 'Img not found'
    return filename


def insert_db(df, name, engine):
    df.to_sql(name, engine, if_exists="replace")

    return None


def download_data_from_goodbooks(path):
    '''Function that uses git module to download the csv files from
    github.com/zygmuntz/goodbooks-10k.git'''

    try:
        os.mkdir(path+'data/external')
    except:
        pass
    os.chdir(path+'data/external')

    try:
        git.Git(path+'data/external').clone("https://github.com/zygmuntz/goodbooks-10k.git")
        os.chdir(path+"data/external/goodbooks-10k")
    except:
        print("Goodbooks-10k not found: No data available")

# Move the data csv files to the external folder.
    for file in os.listdir():
        if file[-3:] == 'csv':
            print(file)
            os.rename(os.getcwd()+'/'+file, path+"data/external/"+file)

# Remove goodbooks folder
    shutil.rmtree(os.getcwd())
    print("Files downloaded: ",os.listdir(path+"data/external"))


def preprocess_goodbooks(path):
    '''Preps and cleans the external csv files'''
## ---- books.csv
    # Load csv file from goodbooks-10k
    cols = ['book_id','isbn', 'authors', 'original_publication_year',
           'title', 'language_code', 'image_url', 'average_rating', 'ratings_count']
    df = pd.read_csv(path+'/data/external/books.csv', usecols=cols, index_col=0)

    # Remove books that dont have ISBN
    df.dropna(subset=['isbn'], inplace=True)

    # Unify the language_code
    df.loc[df.language_code.str.startswith('en', na=False),'language_code'] = 'en'

    # Correct the missing language_code:
    df_lang = df.loc[df.language_code.isnull()].title.apply(lambda x: detect(x))
    df.loc[df_lang.index,'language_code'] = df_lang

    # Get the index with english titles only
    df = df.loc[df.language_code=='en']

    # Drop the language_code column
    df.drop('language_code', axis=1, inplace=True)

    # Rename column original_publication_year to year
    df.rename(columns={'original_publication_year': 'year'}, inplace=True)

    # Set invalid years to 0
    df.loc[df.year<0,'year'] = 0

    # Set Nan's to 0
    df['year'] = df['year'].fillna(0)

    # Convert to int
    df.year = df.year.astype(int)

    # Set authors and title to lower case and remove punctuation
    df['authors'] = df.authors.apply(lambda x: re.sub('[\\\,\:\"]', '', str(x.lower())))
    df['title'] = df.title.apply(lambda x:re.sub('[\\\,\.\:\"]', '', str(x.lower())))

    # Save file
    df.to_csv(path+'/data/processed/books.csv')
    print("Preprocessed", df.shape[0], 'books')

## ---- book_tags.csv
    df = pd.read_csv(path+'data/external/book_tags.csv')
    df.rename(columns={'goodreads_book_id':'book_id'}, inplace=True)
    df.set_index('book_id', inplace=True)

    # Save file
    df.to_csv(path+'/data/processed/book_tags.csv')
    print("Preprocessed", df.shape[0], 'book_tags')

## --- tags.csv
    copyfile(path+'/data/external/tags.csv', path+'/data/processed/tags.csv')
## --- ratings.csv
    copyfile(path+'/data/external/ratings.csv', path+'/data/processed/ratings.csv')
## --- to_read.csv
    copyfile(path+'/data/external/to_read.csv', path+'/data/processed/to_read.csv')
