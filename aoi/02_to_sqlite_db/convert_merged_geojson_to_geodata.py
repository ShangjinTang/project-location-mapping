#!/usr/bin/env python3

import argparse
import json
import os
import sys
from pathlib import Path

from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def main(args):
    db_file = Path(args.output_file)

    db_file.parent.mkdir(parents=True, exist_ok=True)

    if db_file.exists():
        os.remove(db_file)
    db_file.touch()

    engine = create_engine(f"sqlite:///{db_file}?charset=utf8", echo=True)

    Base = declarative_base()

    class GeodataPolygon(Base):
        __tablename__ = args.table_name
        id = Column(Integer, primary_key=True)
        tag = Column(String(), nullable=True)
        polygon = Column(String())
        bbox = Column(String())

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    with open(args.input_file, encoding="utf-8") as f:
        json_data = json.load(f)

    for feature in json_data["features"]:
        coordinates = feature["geometry"]["coordinates"]
        bbox = [
            min(coord[0] for coord in coordinates[0]),
            min(coord[1] for coord in coordinates[0]),
            max(coord[0] for coord in coordinates[0]),
            max(coord[1] for coord in coordinates[0]),
        ]
        geodata = GeodataPolygon(
            tag=feature["properties"].get("tag"),
            polygon=json.dumps(coordinates[0]),
            bbox=json.dumps(bbox),
        )

        session.add(geodata)

    session.commit()
    session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--input_file",
        required=True,
        help="input geojson file path",
    )

    parser.add_argument(
        "-o",
        "--output_file",
        required=True,
        help="output sqlite3 database file path",
    )

    parser.add_argument(
        "--table_name",
        default="geodata_aois",
        help="table name in output sqlite3 database",
    )

    try:
        args = parser.parse_args()
        main(args)
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
