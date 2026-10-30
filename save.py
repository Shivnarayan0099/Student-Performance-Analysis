
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from pymongo import MongoClient

df = pd.read_csv("StudentPerformanceFactors.csv")

print("Dataset loaded successfully")
print("Total rows:", len(df))

df = df.drop_duplicates().copy()

for col in df.columns:
    if df[col].isnull().any():
        if df[col].dtype == "object":
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())

print("Data cleaning completed")

clean_df = df.copy()

for col in clean_df.select_dtypes(include="object").columns:
    encoder = LabelEncoder()
    clean_df[col + "_encoded"] = encoder.fit_transform(
        clean_df[col].astype(str)
    )

print("Data encoding completed")

print("\nStudent Performance Summary")
print("Total students:", len(clean_df))
print("Average exam score:", round(clean_df["Exam_Score"].mean(), 2))
print("Highest exam score:", clean_df["Exam_Score"].max())
print("Average attendance:", round(clean_df["Attendance"].mean(), 2))

uri = "mongodb+srv://shiv********_db_user:********@cluster0.oyu5ybe.mongodb.net/"

client = None

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    client.admin.command("ping")

    db = client["StudentPerformanceDB"]
    collection = db["students"]

    records = clean_df.to_dict("records")

    collection.delete_many({})

    if records:
        collection.insert_many(records)

    print("\nData saved successfully in MongoDB")
    print("Records inserted:", len(records))
    print("Total records in MongoDB:", collection.count_documents({}))

except Exception as e:
    print("Error:", e)

finally:
    if client is not None:
        client.close()

print("\nProgram completed")
