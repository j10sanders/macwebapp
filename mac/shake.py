import xml.etree.ElementTree as ET

def speeches(act, result):
    speech = act.findall('SCENE/SPEECH')
    for tag in speech:
        speakers = tag.findall('SPEAKER')
        lines = tag.findall('LINE')
        for speaker in speakers:
            if speaker.text == 'ALL':
                pass
            elif speaker.text.title() in result:
                result[speaker.text.title()] += len(lines)
            else:
                result[speaker.text.title()] = len(lines)
    return result

def parse_play(tree):
    if len(tree) == 1: # It's an error
        return tree
    if len(tree) == 0:
        return ["Error: no argument for XML tree"]
    result = {}
    for child in tree:
        if child.tag == "ACT": 
            speeches(child, result)
    return sorted(result.items(), key=lambda char: char[1], reverse=True)