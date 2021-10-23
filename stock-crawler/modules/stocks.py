def get_stocks(__history_collection):
  data = []
  pipeline = [
    {
      '$group': {
        '_id': ["$name", "$country"],
        'name': { '$first': "$name" },
        'country': { '$first': "$country" }
      }
    }, {
      '$project': {
        '_id': 0,
        'name': 1,
        'country': 1
      }
    }
  ]
  histories = __history_collection.aggregate(pipeline)
  for history in histories:
    data.append({
      'name': history.get('name'),
      'country': history.get('country')
    })
  return data
