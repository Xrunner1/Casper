CREATE TABLE IF NOT EXISTS 'user'
(
  'uid' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  'pwdhash' TEXT NOT NULL,
  'name' TEXT NOT NULL,
  'create_date' INTEGER
)
