#! usr/bin/env python

def create_json(objs):
    assert type(objs) == type(dict()), 'Passed object must be a dict with keys "results" and "total"'
    json_skeleton = {'total': objs['total'], 'results': [], 'success': True}
    for obj in objs['results']:
        assert hasattr(obj, 'jsonify'), 'Passed objects must be convertible to json with a jsonify() method'
        json_skeleton['results'].append(obj.jsonify())
    return json_skeleton