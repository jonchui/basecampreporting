import datetime

try:
    import cElementTree as ET
except ImportError:
    from elementtree import ET

def parse_basecamp_xml(xml_string):
    nodes = ET.fromstring(xml_string).getchildren()
    parsed = parse_tree(nodes)
    return parsed

def parse_tree(nodes):
    parsed = {}
    for node in nodes:
        tag_name = normalize_tag_name(node.tag)
        if not node.getchildren():
            #It's a single, non-nested item
            parsed[tag_name] = parse_single_node(node)
        else:
            parsed[tag_name] = parse_tree(node.getchildren())
    return parsed

def parse_single_node(node):
    if 'type' in node.keys():
        return cast_value(node.text, node.get('type'))
    else:
        return unicode(node.text.strip())

def normalize_tag_name(tag_name):
    return unicode(tag_name.replace("-", "_").strip())

def cast_value(text_value, type_hint):
    CASTING = {
        'date': cast_to_date,
        'datetime': cast_to_datetime,
        'integer': cast_to_integer,
    }
    return CASTING[type_hint](text_value)

def cast_to_date(value):
    year = int(value[0:4])
    month = int(value[5:7])
    day = int(value[8:10])
    return datetime.date(year=year, month=month, day=day)    

def cast_to_datetime(value):
    year = int(value[0:4])
    month = int(value[5:7])
    day = int(value[8:10])
    hour = int(value[11:13])
    minute = int(value[14:16])
    second = int(value[17:19])
    return datetime.datetime(year=year, month=month, day=day,
                             hour=hour, minute=minute, second=second)

def cast_to_integer(text_value):
    return int(text_value)

if __name__ == "__main__":
    from tests.test_parser import *
    unittest.main()
