import firebase_admin
from firebase_admin import credentials, firestore
import sys

docId = "4"

cred = credentials.Certificate('./ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

def set_string(name, markdown):
    db.document(f"topics/{docId}/articles/{name}").set({"name": name, "markdown": markdown})

def update_string(name, markdown):
    db.document(f"topics/{docId}/articles/{name}").update({"name": name, "markdown": markdown})

def read_markdown(filename):
    with open(filename) as f:
        return f.read()

if __name__ == '__main__':
    article_name = sys.argv[1].split('.')[0]
    markdown = read_markdown(sys.argv[1])
    if sys.argv[2] == "add":
        set_string(article_name, markdown)
    elif sys.argv[2] == "update":
        update_string(article_name, markdown)

