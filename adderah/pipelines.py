import sqlite3

from .items import Item


create_script = """CREATE TABLE IF NOT EXISTS 
items (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    price FLOAT,
    seller VARCHAR,
    in_stock VARCHAR,
    description VARCHAR,
    category VARCHAR,
    subcategory VARCHAR,
    url VARCHAR
);
CREATE TABLE IF NOT EXISTS images (
    item_id INTEGER,
    path VARCHAR,
    url VARCHAR,
    FOREIGN KEY (item_id) REFERENCES items (id)
);
CREATE TABLE IF NOT EXISTS shipping (
    item_id INTEGER,
    direction VARCHAR,
    method VARCHAR,
    duration VARCHAR,
    price FLOAT,
    FOREIGN KEY (item_id) REFERENCES items (id)
);
"""


class AdderahPipeline:

    def __init__(self):

        self.conn = sqlite3.connect("adderah.db")
        self.cr = self.conn.cursor()
        self.cr.executescript(create_script)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item: Item, spider):

        self.cr.execute(
            """INSERT INTO 
               items (
                    name,
                    price,
                    seller,
                    in_stock,
                    description,
                    category,
                    subcategory,
                    url
               ) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, 
            (
                item.name,
                item.price,
                item.seller,
                item.in_stock,
                item.description,
                item.category,
                item.subcategory,
                item.url,
            )
        )

        self.conn.commit()

        self.cr.executemany(
            "INSERT INTO images (item_id, path, url) VALUES (?,?,?)",
            [
                (self.cr.lastrowid, image['path'], image['url']) 
                for image in item.images
            ]
        )

        self.cr.executemany(
            """INSERT INTO 
                shipping (
                    item_id, direction, method, duration, price
                ) 
                VALUES (?,?,?,?,?)
            """,
            [
                (
                    self.cr.lastrowid, 
                    s.direction, 
                    s.method, 
                    s.duration,
                    s.price
                ) 
                for s in item.shipping
            ]
        )

        self.conn.commit()

        return item
