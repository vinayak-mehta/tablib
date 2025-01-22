""" Tablib - JSON Support
"""
import tablib


def serialize_objects_handler(obj):
    import decimal
    from uuid import UUID

    if isinstance(obj, (decimal.Decimal, UUID)):
        return str(obj)
    elif hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        return obj


class JSONFormat:
    title = 'json'
    extensions = ('json', 'jsn')

    @classmethod
    def export_set(cls, dataset):
        """Returns JSON representation of Dataset."""
        import json

        return json.dumps(
            dataset.dict, default=serialize_objects_handler, ensure_ascii=False
        )

    @classmethod
    def export_book(cls, databook):
        """Returns JSON representation of Databook."""
        import json

        return json.dumps(
            databook._package(), default=serialize_objects_handler, ensure_ascii=False
        )

    @classmethod
    def import_set(cls, dset, in_stream):
        """Returns dataset from JSON stream."""
        import json

        dset.wipe()
        dset.dict = json.load(in_stream)

    @classmethod
    def import_book(cls, dbook, in_stream):
        """Returns databook from JSON stream."""
        import json

        dbook.wipe()
        for sheet in json.load(in_stream):
            data = tablib.Dataset()
            data.title = sheet['title']
            data.dict = sheet['data']
            dbook.add_sheet(data)

    @classmethod
    def detect(cls, stream):
        """Returns True if given stream is valid JSON."""
        import json

        try:
            json.load(stream)
            return True
        except (TypeError, ValueError):
            return False
