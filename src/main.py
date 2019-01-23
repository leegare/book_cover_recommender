from sqlalchemy import create_engine
from myfunk import * #get_cover, insert_db
import pandas as pd
import os
from time import time
import warnings
warnings.filterwarnings('ignore')

if __name__ == "__main__":
    print("Welcome to book cover recommender.")
    path = os.getcwd()[:-3]
    print('Path: ',path,'\n',os.listdir(path))

    # Initialize database connection
    try:
        # Engine: common interface to the database from SQLAlchemy
        engine = create_engine('postgresql://postgres:capstone@35.197.77.78:5432/postgres')
        print("Database found.")
    except:
        print("No database available.")
        quit()

    # Get book listings
    df = pd.read_csv(path+'/data/external/books.csv', index_col=0)
    print('Book dataframe size:',df.shape)

    insert_db(df, 'books', engine)

    print('insert_db done')

    # Subset
    data = df.head(10).copy()

    # Get cover images
    # staroot = time()
    os.chdir(path+'data/raw/covers')
    data['cover'] = data.apply(lambda row: get_cover(row), axis=1)
    print('downloading', data.shape[0], 'book covers')

    # insert_db(data, 'books_subset', engine)




    print('Program complete')
