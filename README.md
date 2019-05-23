# Book Cover Recommender:
#### Capstone project ~ Work in Progress

## Introduction

In average the reader will base their purchase decision by looking at the cover for about 3 to 5 seconds. A book’s cover design determines the purchase eight out of ten times **[1]**. Jonny Geller, a literary agent, believes that “it is absolutely crucial if a book is to become a big best selling book you have to be able to communicate the core idea easily”**[2]**. Enter the book's cover! This is because a book cover is a key piece of the puzzle, it's the first visual contact between the book and the reader and first impressions matter.

In this project I will analyze over 10,000 book covers from a public database to detect the underlying patterns. Then, use this information to recommend books to customer similar to the book's cover and see if judging a book by its cover isn't a sin after all.  

A good recommendation would be to select at least k books to user x that is within his list of books the user wants to read.  

## The repository:

In the Data folder: 
- External: Contains the csv files downloaded from the github repo **[3]**:
    - Books.csv: book_id, isbn, authors, year, title and average_rating
    - Ratings.csv: User_id, Book_id, Rating. 
    - Book_tags: Book_id, tag_id, count
    - Tags.csv: Tag_id, tag_name
    - To_read.csv: User_id, Book_id 
- Raw: Contains the csv files ready to be preprocessed. 
- Interim: Contains the data prepped to be explored and visualized. 
- Processed: Contains the csv files and covers ready to be analyzed. 
    
In the notebooks folder:
1. **data_collection.ipynb**: 
    - Extracts the csv files from the github repo. 
        - I will use three of them: The books table, the ratings table and to_read table.
        - The files are then stored in the data/external folder.
    - An initial preprocessing function selects relevant data and stores it in the data/raw folder. 
        - Only books that are in english. 
        - Cleans the data. 
        - Selects features that are relevant to this study.
    - Consolidates database
        - Ensure the csv files hold accurate information and refer to their cover image files. 
    - Saves the modified files in the data/raw folder

2. **preprocessing.ipynb**: 
    - Preprocess the data from /raw/books.csv and ratings.csv files 
    - It updates the books.csv file with the cover's info and saves the file in the data/processed folder. 

3. **similarity_metric_1.ipynb**: 
    - Defines a hash metric to be compared within the image covers. 
    - Builds the recommender system. 

## The dataset


## Preprocessing: 

- The function *preprocess_goodbooks* cleans the data from the Interim folder and saves it in the data/raw folder. 
- Downloads the book covers through the *get_cover* function and saves them in the data/raw/covers folder. 
- The book cover images will be resized to the standard size of 149x98
- To reduce the dimensionality of the data set, and avoid running into “memory error”, we will filter out rarely rated books and rarely rating users.

## MODELING: 
The advantages of using a content-based recommender system (CBRS) are: 
1. No need for data on other users
2. Able to recommend to users with unique tastes. 
3. Able to recommend new and unpopular items. 
4. Explanations for recommended items. 

Disadvantages would be that 
1. People might have multiple interests. 
2. Cold-start problem for new users. 


I will start by building an item profiles for every user, containing books rated or shown interest by the user. 

To build the user profiles using a weighted average of rated item profiles. 
I will normalize the ratings for each user by subtracting user's mean rating. Then the profile weight would be normalized rating / number of books with that feature. 

## EDA
Heatmap of Ratings Matrix - Users x Items
Distribution of ratings per user: average number of books per user 
Distribution of ratings per book: support distribution
Distribution of books to read per user. 

## Evaluation

To confirm the validity of this study I will use collaborative filtering using data from the ratings table. This mode of recommender system is when the user is recommended items that people with similar tastes and preferences liked in the past. 

## References

[1] - How to Write a Good Book Description
https://www.ingramspark.com/blog/

[2] - What Makes a Bestseller? | Jonny Geller | TEDxOxford
https://www.youtube.com/watch?v=mD-uP2BsVy4&list=WL&index=73

[3] - goodbooks-10k
https://github.com/zygmuntz/goodbooks-10k