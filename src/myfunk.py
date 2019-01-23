import re
import urllib.request # Download images
from sqlalchemy import create_engine

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
