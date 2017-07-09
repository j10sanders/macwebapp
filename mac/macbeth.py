import xml.etree.ElementTree as ET

def speeches(act, result):
    speech = act.findall('SCENE/SPEECH')
    for x in speech:
        speakers = x.findall('SPEAKER')
        lines = x.findall('LINE')
        for speaker in speakers:
            if speaker.text == 'ALL':
                pass
            elif speaker.text.title() in result:
                result[speaker.text.title()] += len(lines)
            else:
                result[speaker.text.title()] = len(lines)
    return result

def acts(tree):
    result = {}
    for child in tree:
        if child.tag == "ACT": 
            speeches(child, result)
    return sorted(result.items(), key=lambda char: char[1], reverse=True)