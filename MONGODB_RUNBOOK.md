# MongoDB runbook

This project stores workflow output in MongoDB. The current save logic writes into the database `KnowledgeExtractor` and the collection `articles`.

## 1. Start MongoDB

If MongoDB is not already running, start it with:

```bash
mongod --dbpath /data/db
```

If you use systemd, this also works:

```bash
sudo systemctl start mongod
```

Verify that it is running:

```bash
ps -ef | grep '[m]ongod'
```

And confirm the server responds:

```bash
mongosh --eval 'db.runCommand({ ping: 1 })'
```

## 2. Open the MongoDB shell

```bash
mongosh
```

Then switch to the project database:

```javascript
use KnowledgeExtractor
```

## 3. Check the articles collection

List collections:

```javascript
show collections
```

Count saved records:

```javascript
db.articles.countDocuments()
```

View the latest records:

```javascript
db.articles.find().sort({ _id: -1 }).limit(5).pretty()
```

## 4. Test records from the app

Run your workflow or the save step, then inspect the database from Python:

```bash
python - <<'PY'
from output.save import db
print("total documents:", db.articles.count_documents({}))
for doc in db.articles.find().sort([('_id', -1)]).limit(5):
    print(doc)
PY
```

## 5. Optional cleanup

Remove all test records if needed:

```javascript
db.articles.deleteMany({})
```

> The app currently sets `is_processed: false` as a default field for each inserted document.
