from pymongo import MongoClient
from pprint import pprint

# Use client = MongoClient('mongodb://localhost:27017') for specific ports!
# Connect to the default port on localhost for the mongodb server.
client = MongoClient("mongodb://localhost:27017")

# Create or open the video_store database on server.
db = client["291db"]

def main(db):
    '''
    create cursor to the dbs required and create indexes for elements we will use commonnly
    create aggregation pipeline and fill in based on query reqs
    print out the data
    '''
    # Create or open the collection in the db
    count = 0
    nbasics = db["name_basics"]
    tprincipals = db["title_principals"]
    tbasics = db["title_basics"]
    nbasics.create_index('nconst')
    nbasics.create_index('primaryName')
    tbasics.create_index('tconst')
    tprincipals.create_index('nconst')

    member = input('Enter a cast/crew member: ')
    


    query_stages= [#pipeline for aggregation
        {'$match': {'primaryName': { '$regex': member, '$options':'i' } }},#case insentive search
        {'$lookup': {'from':'title_principals','localField':'nconst','foreignField': 'nconst','as':'jobs'}},#join table
        {'$lookup': {'from':'title_basics','localField':'jobs.tconst','foreignField': 'tconst','as':'movies'}},#join table
        {'$project':{'primaryName':1 ,'movies':1,'primaryProfession':1,'jobs':1,'_id': 0,}},#return title, movie, and job details
        ]   

    # results = collection.find({"genres": 'Crime' })
    results = nbasics.aggregate(query_stages)
    print('_'*100)

    for r in results:
        #print out results
        if len(member) == 1:
            print('No matches Found')
            break
        if r['primaryName'].lower()==member.lower():
            print('Cast/Crew Name:',r['primaryName'],'\n')
            print('Professions:',','.join(r['primaryProfession']),'\n'+'.'*100)
            movies = r['movies']
            for i in movies:
                # print(i['primaryTitle'])
                for x in r['jobs']:
                    if x['tconst'] == i['tconst']:
                        if x['characters']==None and x['characters']==None:
                            count+=1
                            break
                        else:
                            print('Primary Title:',i['primaryTitle']) 
                            print('Job;',x['job'])
                            if x['characters']!=None:
                                print('character(s):',', '.join(x['characters']))
                            else:
                                print('character(s):',x['characters'])

                            print('\n')
                            count+=1
            print("_"*100,'\n')


    if count==0:#no matches
        print('No Cast Member Matched Input Provided By User')

        
main(db)

# https://stackoverflow.com/questions/34598563/mongodb-print-pretty-with-pymongo





