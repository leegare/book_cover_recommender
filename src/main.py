from sqlalchemy import create_engine
from myfunk import * #get_cover, insert_db
import pandas as pd
import os
from time import time
import warnings
warnings.filterwarnings('ignore')

def ensure_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)

if __name__ == "__main__":
    print("Welcome to book cover recommender.")
    path = os.getcwd()[:-3]
    print('Path: ',path+'data','\n',os.listdir(path+'data'))

    # Initialize database connection
    try:
        # Engine: common interface to the database from SQLAlchemy
        # Connect to sql_books instance
        engine = create_engine('postgresql://postgres:capstone@35.197.77.78:5432/postgres')
        print("Database found.")
    except:
        print("No database available.")
        quit()

    # Get book listings
    df = pd.read_csv(path+'data/external/books.csv', index_col=0)
    df2 = pd.read_csv(path+'data/external/ratings.csv', index_col=0)
    df3 = pd.read_csv(path+'data/external/to_read.csv', index_col=0)
    df4 = pd.read_csv(path+'data/external/tags.csv', index_col=0)
    df5 = pd.read_csv(path+'data/external/book_tags.csv', index_col=0)

    insert_db(df, 'books', engine)
    insert_db(df2, 'ratings', engine)
    insert_db(df3, 'to_read', engine)
    insert_db(df4, 'tags', engine)
    insert_db(df5, 'book_tags', engine)

    print('insert_db done')

    # Subset
    data = df.head(10).copy()

    # Get cover images

    # start = time()

    os.chdir(path+'data')
    try:
        os.mkdir('covers')
    except:
        pass
    # ensure_directory('./data/covers/')
    os.chdir(path+'data/covers')

    data['cover'] = data.apply(lambda row: get_cover(row), axis=1)
    print('Downloaded', data.shape[0], 'book covers')

    # insert_db(data, 'books_subset', engine)




    print('Program complete')
