# Book Cover Recommender:
#### Capstone project ~ Work in Progress

## Introduction

In average the reader will base their purchase decision by looking at the cover for about 3 to 5 seconds. A book’s cover design determines the purchase eight out of ten times **[1]**. Jonny Geller, a literary agent, believes that “it is absolutely crucial if a book is to become a big best selling book you have to be able to communicate the core idea easily”**[2]**. Enter the book's cover! This is because a book cover is a key piece of the puzzle, it's the first visual contact between the book and the reader and first impressions matter.

In this project I will analyze over 10,000 book covers from a public database to detect the underlying patterns that can be learnt from the reader. Then, use this information to build a recommender system based solely on the book's cover and see if judging a book by its cover isn't a sin after all.  

## The repository:

In the Data folder: 
- External: Contains the csv files downloaded from the github repo **[3]**:
    - Books.csv: book_id, isbn, authors, year, title and average_rating
    - Ratings.csv: User_id, Book_id, Rating. 
    - Book_tags: Book_id, tag_id, count
    - Tags.csv: Tag_id, tag_name
    - To_read.csv: User_id, Book_id 
- Interim: Contains the csv files ready to be preprocessed. 
- Processed: Contains the csv files and covers ready to be analyzed. 
    
In the notebooks folder:
1. **data_collection.ipynb**: 
    - Extracts the csv files from the github repo. 
    - I will use two of them: The books table and the ratings table.
    - The files are then stored in the data/external folder.
    
2. **preprocessing.ipynb**: 
    - Preprocess the data from /Interim/books.csv and ratings.csv files 
    - It updates the books.csv file with the cover's info and saves the file in the data/interim folder. 

3. **similarity_metric_1.ipynb**: 
    - Defines a hash metric to be compared within the image covers. 
    - Builds the recommender system. 

## The dataset


## Preprocessing

- The function *preprocess_goodbooks* cleans the data and saves it in the data/raw folder. 
- Then it downloads the book covers through the *get_cover* function and saves them in the data/raw/covers folder. 
- The book cover images will be resized to the standard size of 149x98

## EDA


## Evaluation

To confirm the validity of this study I will use collaborative filtering using data from the ratings table. This mode of recommender system is when the user is recommended items that people with similar tastes and preferences liked in the past. 

## References

[1] - How to Write a Good Book Description
https://www.ingramspark.com/blog/

[2] - What Makes a Bestseller? | Jonny Geller | TEDxOxford
https://www.youtube.com/watch?v=mD-uP2BsVy4&list=WL&index=73

[3] - goodbooks-10k
https://github.com/zygmuntz/goodbooks-10k