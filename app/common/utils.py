def transform_mongo_document(doc: dict):
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc
