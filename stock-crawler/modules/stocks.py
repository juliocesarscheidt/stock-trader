def get_stocks(__history_collection, offset=0, limit=50):
    print("offset", offset)
    print("limit", limit)

    data = []
    pipeline = [
        {"$sort": {"date": 1}},
        {
            "$group": {
                "_id": ["$name", "$country"],
                "name": {"$first": "$name"},
                "country": {"$first": "$country"},
            }
        },
        {"$project": {"_id": 0, "name": 1, "country": 1}},
        {"$skip": offset},
        {"$limit": limit},
    ]
    histories = __history_collection.aggregate(pipeline)
    for history in histories:
        data.append({"name": history.get("name"), "country": history.get("country")})
    return data


def count_stocks(__history_collection):
    data = 0
    pipeline = [
        {"$sort": {"date": 1}},
        {
            "$group": {
                "_id": ["$name", "$country"],
                "name": {"$first": "$name"},
                "country": {"$first": "$country"},
            }
        },
        {"$count": "name"},
        {"$project": {"counter": "$name"}},
    ]
    histories = __history_collection.aggregate(pipeline)
    for history in histories:
        data = int(history["counter"])
    return data
