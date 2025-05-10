import fasttext
import psycopg2

# Connect to Supabase PostgreSQL (replace with your credentials)

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Adeboyin1+",  # 👈 Replace this
    host="db.ajvppqxabvjgpwftfqlk.supabase.co",
    port="5432"
)
cursor = conn.cursor()

# Create and write training data from surah_theme and verse_theme
with open("themes.txt", "w", encoding="utf-8") as f:
    # Fetch Surah Themes
    cursor.execute("SELECT surah_theme FROM Surahs")
    for row in cursor.fetchall():
        theme = row[0].strip()
        f.write(f"__label__{theme.replace(' ', '')} {theme}\n")

    # Fetch Verse Themes
    cursor.execute("SELECT verse_theme FROM Verses")
    for row in cursor.fetchall():
        theme = row[0].strip()
        f.write(f"__label__{theme.replace(' ', '')} {theme}\n")

# Train the FastText model
model = fasttext.train_supervised("themes.txt", epoch=25, lr=1.0, wordNgrams=2)

# Save the model
model.save_model("fasttext_model.bin")
print("FastText model trained and saved as fasttext_model.bin")
