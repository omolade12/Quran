from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import fasttext
import psycopg2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = fasttext.load_model("fasttext_model.bin")

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Adeboyin1+",
    host="db.ajvppqxabvjgpwftfqlk.supabase.co",
    port="5432"
)

@app.get("/search")
def search(theme: str, type: str):
    cursor = conn.cursor()
    if type == "surah":
        cursor.execute("SELECT surah_name, revelation_type FROM Surahs WHERE surah_theme ILIKE %s", (f"%{theme}%",))
        surahs = cursor.fetchall()
        result = []
        for name, revelation in surahs:
            cursor.execute("""
                SELECT verse_number, verse_translation FROM Verses
                JOIN Surahs ON Surahs.surah_id = Verses.surah_id
                WHERE Surahs.surah_name = %s
                ORDER BY verse_number
            """, (name,))
            verses = cursor.fetchall()
            result.append({
                "surah_name": name,
                "revelation_type": revelation,
                "verses": [{"number": v[0], "text": v[1]} for v in verses]
            })
        return result
    elif type == "verse":
        cursor.execute("SELECT verse_number, verse_translation, surah_id FROM Verses WHERE verse_theme ILIKE %s", (f"%{theme}%",))
        verses = cursor.fetchall()
        results = []
        for v in verses:
            cursor.execute("SELECT surah_name FROM Surahs WHERE surah_id = %s", (v[2],))
            surah_name = cursor.fetchone()[0]
            results.append({
                "verse_number": v[0],
                "verse_translation": v[1],
                "surah_name": surah_name
            })
        return results

@app.get("/suggest")
def suggest(query: str):
    predictions = model.predict([query], k=5)
    return predictions[0]
