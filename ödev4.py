import sqlite3
from collections import Counter


def connect_and_save(text1, text2):
    conn = sqlite3.connect('texts.db')
    cursor = conn.cursor()


    cursor.execute('DROP TABLE IF EXISTS Texts')


    cursor.execute('CREATE TABLE Texts (id INTEGER PRIMARY KEY, text TEXT)')

    # Yeni metinleri ekle
    cursor.execute('INSERT INTO Texts (text) VALUES (?)', (text1,))
    cursor.execute('INSERT INTO Texts (text) VALUES (?)', (text2,))


    conn.commit()
    conn.close()


def load_and_compare_texts():
    conn = sqlite3.connect('texts.db')
    cursor = conn.cursor()

    cursor.execute('SELECT text FROM Texts')
    texts = [text[0].lower() for text in cursor.fetchall()]  # Metinleri küçük harfe çevir
    conn.close()


    words_text1 = Counter(texts[0].split())
    words_text2 = Counter(texts[1].split())


    all_words = set(words_text1).union(words_text2)


    intersection = sum(min(words_text1[word], words_text2[word]) for word in all_words)
    total_words = sum(words_text1[word] + words_text2[word] for word in all_words)
    similarity_score = (2.0 * intersection) / total_words if total_words > 0 else 1.0

    return similarity_score


if __name__ == "__main__":

    text1 = input("İlk metni girin: ")
    text2 = input("İkinci metni girin: ")


    connect_and_save(text1, text2)


    similarity_score = load_and_compare_texts()


    print(f"Similarity Score: {similarity_score:.2f}")


    with open('similarity_status.txt', 'w') as f:
        f.write(f"Similarity score between texts: {similarity_score:.2f}")
