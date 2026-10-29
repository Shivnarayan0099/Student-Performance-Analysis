
from pymongo import MongoClient

uri = "YOUR_MONGODB_CONNECTION_URI"

client = MongoClient(uri)

db = client["StudentPerformanceDB"]
collection = db["students"]

records = clean_df.to_dict("records")

if collection.count_documents({}) == 0:
    if records:
        collection.insert_many(records)
        print("Data saved successfully")
        print("Total records inserted:", len(records))
else:
    print("Data already exists in MongoDB")

print("Total records:", collection.count_documents({}))

client.close()
