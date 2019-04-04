from sqlalchemy import create_engine
from shutil import copyfile
from langdetect import detect                   # Detect language
from nltk.corpus import stopwords
from keras.preprocessing import image           # F Preprocessing
from scipy.misc import imread, imresize, imshow # F filter_images
from hashlib import md5
from PIL import Image # To resize the cover images.
import unidecode # To remove accents
import scipy
import shutil           # To remove folders
import re
import os
import os.path # To check if the cover image file exists
import git              # To clone and download the csv files
import urllib.request   # Download images
import pandas as pd
import numpy as np      # F remove_dupes
import glob             # grab only jpegs
import cv2              # F preprocess



def hamming_distance(image, image2):
    score = scipy.spatial.distance.hamming(image, image2)
    return score

def cover_resize(image_files, width=98, height=149):
    for cover in image_files:
        img = Image.open(cover)
        img = img.resize((width, height), Image.ANTIALIAS)
        img.save(cover)

def remove_cover_images(img):
    '''Receives a list of image filenames
    and removes the files in storage'''
    for i in img:
        os.remove(i)

def preprocess(img):
    '''Function that gets an image filename, loads it and preprocess it:
        - Converts it to grayscale
        - Resizes it and flattens it by row and columns
        - Calculates the px to px change in intensity
        Returns a 3d array of the preprocessed image'''
    try:
        img = imread(img)
    except:
        print('Image not found', img)
        pass
    # Take the average of the 3 channels to convert to grayscale
    gray = np.average(img, weights = [0.299, 0.587, 0.114], axis=2)

    ## ------ difference_score
    # Resize
    height=30
    width=30
    # Flatten by row
    row_res = cv2.resize(gray, (height, width), interpolation=cv2.INTER_AREA).flatten()
    # Flatten by col
    col_res = cv2.resize(gray, (height, width), interpolation=cv2.INTER_AREA).flatten("F")

    # Gradient direction based on intensity
    # Difference is a 1-D boolean array
    # where True refers to a change in intensity from 1 px to another
    difference_row = np.diff(row_res)
    difference_col = np.diff(col_res)
    # Look for change in intensities
    # True for it does, False for it doesnt change
    difference_row = difference_row > 0
    difference_col = difference_col > 0
    difference = np.vstack((difference_row, difference_col)).flatten()

    return difference

def file_hash(array):
    '''Returns a hash in hex'''
    return md5(array).hexdigest()

def get_hash(image_files):
    ds_dict={}
    duplicates =[]
    hash_ds=[]
    for image in image_files:
        # Change to gray, resize to array (1,900) and compute the intensity gradient.
        ds=preprocess(image)
        # Hash_ds is a list of lists, where each list is "ds"
        hash_ds.append(ds)
        # Hash the ds variable to hexa to be used next as a dict key
        filehash = md5(ds).hexdigest()
        if filehash not in ds_dict:
            ds_dict[filehash] = image
        else:
            duplicates.append((image,ds_dict[filehash]))
    return duplicates, ds_dict, hash_ds

def get_gradient_intensity(image_list):
    '''ds_dict is a dictionary with the image name as key and
    its gradient intensity as value'''
    ds_dict = {}
    duplicates = []
    for image in image_list:
        # Get the intensity gradient
        ds = preprocess(image)
        if image not in ds_dict:
            ds_dict[image] = ds
        else:
            duplicates.append((image, ds_dict[image]))
    return duplicates, ds_dict

def separate_filename(s, stopwrd = False, ccase = False):
# s = "Pride and Prejudice by Jane Austen"
# returns ("Pride and Prejudice", "Jane Austen")
# Or ("Pride Prejudice", "Jane Austen")
# Or ("pride prejudice", "jane austen")
    pattern_country = re.compile(r" by ")
    stop_words = stopwords.words('english')
    sep = len(s)
    r = pattern_country.search(s)
    if r:
        sep = min(r.start(),sep)
        title = s[:sep].strip()
        author = s[sep+4:].strip()
    else:
        print('separate_filename: by not found in ',s)
        title = s.lower()
        author = ''

    # Convert to lower case
    if ccase:
        title = title.lower()
        author = author.lower()

    # remove stop words
    if stopwrd:
        title = ' '.join(list(filter(lambda c: c not in stop_words, title.split())))

    return (title,author)

def remove_dupes(df, duplicates):
    '''Function that receives a path to the books files
    an a list of tuples as duplicates
    It will select unique books from the list of tuples and delete the cover and remove its instance
    from the dataframe (stored in data/interim) and will save it
    in data/processed'''

    dupes = []
    # Comb the duplicates
    for file_names in duplicates:
        if file_names[0] not in dupes:
            dupes.append(file_names[0])

        if file_names[1] not in dupes:
            dupes.append(file_names[1])

        # Delete cover
    for dupe in dupes:
        if os.path.exists(dupe):
            os.remove(dupe)
    # Remove instance from dataset
    return df.loc[~df.cover.isin(dupes)]


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
        os.mkdir(path+'/data/external')
    except:
        pass
    os.chdir(path+'/data/external')

    try:
        git.Git(path+'/data/external').clone("https://github.com/zygmuntz/goodbooks-10k.git")
        os.chdir(path+"/data/external/goodbooks-10k")
    except:
        print("Goodbooks-10k not found: No data available")

# Move the data csv files to the external folder.
    for file in os.listdir():
        if file[-3:] == 'csv':
            print(file)
            os.rename(os.getcwd()+'/'+file, path+"/data/external/"+file)

# Remove goodbooks folder
    shutil.rmtree(os.getcwd())
    print("Files downloaded: ",os.listdir(path+"/data/external"))


def preprocess_goodbooks(path):
    '''Preps and cleans the external csv files:
        - Selects the relevant columns
        - Remove books that dont have ISBN
        - Unify the language_code
        - Correct the missing language_code
        - Get the index with english titles only
        - Drop the language_code column
        - Assign a logical label name to the current feature
        - Checks the validity of data in feature: years
        - Casting to adequate types
        - Set authors and title to lower case and remove punctuation
        - Saves csv preprocessed files on the raw subfolder
    '''
    ## ---- books.csv
    # Load csv file from goodbooks-10k
    cols = ['book_id','isbn', 'authors', 'original_publication_year',
           'title', 'language_code', 'image_url', 'average_rating', 'ratings_count']
    df = pd.read_csv(path+'/data/external/books.csv', usecols=cols, index_col=0)
    print('Preprocessing {} books'.format(df.shape[0]))

    # Remove books that dont have ISBN
    df.dropna(subset=['isbn'], inplace=True)

    # Unify the language_code
    df.loc[df.language_code.str.startswith('en', na=False),'language_code'] = 'en'
    print('Found {} books officially in english.\nRunning the english detector for the rest'.\
    format(df.loc[df.language_code=='en'].shape[0]))

    # Correct the missing language_code:
    df_lang = df.loc[df.language_code.isnull()].title.apply(lambda x: detect(x))
    df.loc[df_lang.index,'language_code'] = df_lang
    print('Detector found {} more books in english'.format((df_lang=='en').sum()))

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
    punctuation_pattern = r"[^\w\s]"
    df['authors'] = df.authors.apply(lambda x: re.sub(punctuation_pattern, '', unidecode.unidecode(x).lower().strip()))
    df['title'] = df.title.apply(lambda x: re.sub(punctuation_pattern, '', unidecode.unidecode(x).lower().strip()))

    # Save file (will be saved as UTF-8 by default!)
    df.to_csv(path+'/data/raw/books.csv')
    print("Preprocessed", df.shape[0], 'books')

## ---- book_tags.csv
    df = pd.read_csv(path+'/data/external/book_tags.csv')
    df.rename(columns={'goodreads_book_id':'book_id'}, inplace=True)
    df.set_index('book_id', inplace=True)

    # Save file
    df.to_csv(path+'/data/raw/book_tags.csv')
    print("Preprocessed", df.shape[0], 'book_tags')

## --- tags.csv
    copyfile(path+'/data/external/tags.csv', path+'/data/raw/tags.csv')
## --- ratings.csv
    copyfile(path+'/data/external/ratings.csv', path+'/data/raw/ratings.csv')
## --- to_read.csv
    copyfile(path+'/data/external/to_read.csv', path+'/data/raw/to_read.csv')
