from pymongo import MongoClient
from pprint import pprint

# Use client = MongoClient('mongodb://localhost:27017') for specific ports!
# Connect to the default port on localhost for the mongodb server.
client = MongoClient("mongodb://localhost:27017")

# Create or open the video_store database on server.
db = client["291db"]

def main(db):
    # Create or open the collection in the db
    count = 1
    collection = db["title_basics"]
    col = db["title_ratings"]
    min_vote = int(input('Enter a Minimum Vote: '))
    genre_name = input('Enter a genre: ')
    col.create_index("tconst")
    collection.create_index('genre')
    collection.create_index('tconst')


    query_stages= [
        {'$unwind':'$genres'},#seperate by genre
        {'$match': {'genres': { '$regex': genre_name, '$options':'i' } }},#case insentive search
        {'$lookup': {'from':'title_ratings','localField':'tconst','foreignField': 'tconst','as':'ratings'}},#join table
        {'$unwind':'$ratings'},#unwind rating
        {'$sort':{'ratings.averageRating':-1}},#sort by avg score

        {'$project':{'primaryTitle':1 ,'ratings':1,'genres':1,'_id': 0,}},#return title, genre, and rating details
        ]   

    # results = collection.find({"genres": 'Crime' })
    results = collection.aggregate(query_stages)
    for result in results:
        #print results
        num = result['ratings']
        if int(num['numVotes'])>=min_vote and result['genres'].lower()==genre_name.lower():
            print('')

            print('{}|Votes: {}| Rating: {} '.format(result['primaryTitle'],num['numVotes'],num['averageRating']))
            print("_"*100)
            print('')
            

        
main(db)

# https://stackoverflow.com/questions/34598563/mongodb-print-pretty-with-pymongo





