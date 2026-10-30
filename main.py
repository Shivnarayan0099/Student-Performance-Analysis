
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from pymongo import MongoClient
from pymongo.errors import PyMongoError

 
df = pd.read_csv("StudentPerformanceFactors.csv")

print("Dataset loaded successfully")
print("Dataset shape:", df.shape)

print("\nFirst five records:")
print(df.head())

print("\nDataset information:")
df.info()

print("\nStatistical summary:")
print(df.describe())

print("\nMissing values before cleaning:")
print(df.isnull().sum())

print("\nDuplicate records:", df.duplicated().sum())
 
df = df.drop_duplicates().copy()

for col in df.columns:
    if df[col].isnull().any():
        if df[col].dtype == "object":
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("Dataset shape after cleaning:", df.shape)

 
clean_df = df.copy()

for col in clean_df.select_dtypes(include="object").columns:
    encoder = LabelEncoder()
    clean_df[col + "_encoded"] = encoder.fit_transform(
        clean_df[col].astype(str)
    )

print("\nData encoding completed")
 
print("\nStudent performance summary:")

columns = [
    "Hours_Studied",
    "Attendance",
    "Previous_Scores",
    "Exam_Score"
]

print(clean_df[columns].describe().round(2))

print("\nTotal students:", len(clean_df))
print("Average exam score:", round(clean_df["Exam_Score"].mean(), 2))
print("Highest exam score:", clean_df["Exam_Score"].max())
print("Lowest exam score:", clean_df["Exam_Score"].min())
print("Average attendance:", round(clean_df["Attendance"].mean(), 2))


import matplotlib.pyplot as plt

plt.figure(figsize=(9, 5))

plt.scatter(
    df["Hours_Studied"],
    df["Exam_Score"],
    alpha=0.5
)

plt.title("Impact of Study Hours on Exam Performance")
plt.xlabel("Hours Studied per Week")
plt.ylabel("Exam Score")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Connect to MongoDB Atlas
uri = "mongodb+srv://shiv******88_db_user:*******@cluster0.oyu5ybe.mongodb.net"

client = None

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    client.admin.command("ping")

    db = client["StudentPerformanceDB"]
    collection = db["students"]

    records = clean_df.to_dict("records")

    # Insert records only if the collection is empty
    if collection.count_documents({}) == 0 and records:
        collection.insert_many(records)
        print("\nData saved to MongoDB successfully")
        print("Records inserted:", len(records))
    else:
        print("\nCollection already contains records")
        print("No new records inserted")

    print("Total records in MongoDB:", collection.count_documents({}))

except PyMongoError as e:
    print("\nMongoDB connection error:", e)

finally:
    if client is not None:
        client.close()

print("\nProgram completed")
