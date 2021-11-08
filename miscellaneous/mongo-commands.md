# Mongo Commands

```bash

docker-compose up -d mongo
docker-compose logs -f --tail 50 mongo

docker-compose exec mongo bash


echo 'db.runCommand("ping").ok' | mongo 127.0.0.1:27017/stocks --quiet

docker-compose exec mongo bash -c \
  "echo 'db.runCommand(\"ping\").ok' | mongo 127.0.0.1:27017/stocks --quiet"


mongo --host 127.0.0.1 --port 27017
mongo --host 127.0.0.1 --port 27017 -- stocks

use admin;
db.auth("root", "admin");

show dbs;

db.runCommand({connectionStatus: 1});
show roles;

use stocks;
show collections;

db.getCollectionNames();

db.history.find({});
db.history.find({"_id": ObjectId("615e73041061f9ca09c75f6e")}).pretty();


db.history.createIndex({ name: -1 })

db.history.getIndexes()

db.history.dropIndex({ name: -1 })


# find a history by name and order by date desc
db.history.find({ name : "itub4" }).sort({ date: -1 }).pretty().skip(0).limit(1);


# find all last histories grouping by name and order by date desc
db.history.aggregate(
  [
    {
      $sort: { date: -1 }
    }, {
      $group: {
        _id: "$name",
        object_id: { $first: "$_id" },
        name: { $first: "$name" },
        price: { $first: "$price" },
        date: { $first: "$date" }
      }
    }, {
      $project: {
        _id: "$object_id",
        name: 1,
        price: 1,
        date: 1
      }
    }
  ]
)

db.history.aggregate(
  [
    {
      $match: { country: "br" }
    }, {
      $sort: { date: -1 }
    }, {
      $group: {
        _id: ["$name", "$country"],
        object_id: { $first: "$_id" },
        name: { $first: "$name" },
        country: { $first: "$country" },
        price: { $first: "$price" },
        date: { $first: "$date" }
      }
    }, {
      $project: {
        _id: "$object_id",
        name: 1,
        country: 1,
        price: 1,
        date: 1
      }
    }
  ]
)


# find all stocks and group by name
db.history.aggregate(
  [
    {
      $group: {
        _id: "$name",
        name: { $first: "$name" }
      }
    }, {
      $project: {
        _id: 0,
        name: 1
      }
    }
  ]
)

db.history.aggregate(
  [
    {
      $group: {
        _id: ["$name", "$country"],
        name: { $first: "$name" },
        country: { $first: "$country" }
      }
    }, {
      $project: {
        _id: 0,
        name: 1,
        country: 1
      }
    }
  ]
)


# find all stocks by name, grouping by name and date
db.history.aggregate(
  [
    {
      $match: { "name": "itub4" }
    }, {
      $project: {
        _id: "$object_id",
        name: 1,
        country: 1,
        price: 1,
        date: {
          $dateToString: {
            format: "%Y-%m-%d", date: {
              $dateFromString: { dateString: "$date" },
            },
          },
        },
      }
    }, {
      $group: {
        _id: ["$name", "$date"],
        name: { $last: "$name" },
        country: { $last: "$country" },
        price: { $last: "$price" },
        date: { $last: "$date" },
      }
    }, {
      $project: {
        _id: "$object_id",
        name: 1,
        country: 1,
        price: 1,
        date: 1
      }
    }, {
       $sort: { name: 1, date: -1,  },
    }
  ]
)

```
