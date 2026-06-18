import json

from models import topics

with open("output/topicsSave.json", "r") as f:
    json.dumps(topics.model_dump(),f, indent=4)