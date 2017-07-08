import xml.etree.ElementTree as ET

def speeches(act, values):
    speech = act.findall('SCENE/SPEECH')
    for x in speech:
        speakers = x.findall('SPEAKER')
        lines = x.findall('LINE')
        for s in speakers:
            if s.text == 'ALL':
                pass
            elif s.text.title() in values:
                values[s.text.title()] += len(lines)
            else:
                values[s.text.title()] = len(lines)
    return values

def acts(tree):
    values = {}
    for child in tree:
        if child.tag == "ACT": 
            speeches(child, values)
    return values