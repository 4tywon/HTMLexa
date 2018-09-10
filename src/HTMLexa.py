
# coding: utf-8

# ## Imports

# In[32]:


from bs4 import BeautifulSoup
import requests
import json
import boto3


# ## Description Parsing

# In[33]:


def pictureSearch(text):
    # Process Text
    searchterms = text.split()
    
    # Get Url
    query = searchterms[0]
    for i in searchterms[1:]:
        query = query + "+"  +i
    url = "https://www.google.com/search?tbm=isch&q=" + query
    
    # Scrape Picture
    s = requests.get(url).text
    
    soup = BeautifulSoup(s, 'html.parser')
    return str(soup.img.get('src'))


def LinkSearch(text):
    searchterms = text.split()
    query = searchterms[0]
    for i in searchterms[1:]:
        query = query + "+"  +i
    url = "https://www.google.com/search?&q=" + query
    s = requests.get(url).text
    soup = BeautifulSoup(s, 'html.parser')
    return str(soup.find("h3").find("a").get("href"))[7:]

    
def TextWrite(text):
    return text


# ## Description Parsing

# In[34]:


def contains(arr, text):
    text = text.lower()
    b = False
    for i in arr:
        b = b or (i in text)
    return b

def componentMap(text):
    comp = "Paragraph"
    Image = ["image", "picture", "pic", "photo"]
    Link = "link"
    Button = "button"
    Header = ["header", "title"]
    Subheader = ["subheader", "subtitle"]
    if contains(Image, text):
        return "Image"
    elif Link in text.lower():
        return "Link"
    elif Button in text.lower():
        return "Button"
    elif contains(Subheader, text):
        return "Subheader"
    elif contains(Header, text):
        return "Header"
    return comp
    
colorDict = {
    'red': 0,
    'orange': 0,
    'yellow': 0,
    'green' : 0,
    'blue' : 0,
    'purple' : 0,
    'black' : 0,
    'white' : 0,
    'gray' : 0,
    'pink' : 0,
    'brown' : 0,
    'navy' : 0
}

def getSize(text):
    size = "normal"
    # WordNet Synset
    small = ["small", "little", "minuscule", "modest", "diminished", "tiny" ]
    large = ["large", "big", "huge", "massive", "prominent", "giant"]
    if contains(small, text):
        size = 'small'
    elif contains(large, text):
        size = 'large'
    return size


def hueSearch(col, text):
    return col

def getCol(text):
    loc = 0
    if 'left' in text.lower():
        return 1
    elif 'right' in text.lower():
        return 2
    return loc

def getColors(text):
    col = None
    def mindistance(x, arr):
        min = len(arr) + 1
        for i in range(len(arr)):
            min = abs(i - x) if abs(i - x) < min else min
        return min
    s = text
    text = text.split()
    d = {'text':[], 'background':[]}
    for i in range(len(text)):
        if text[i].lower() in 'text words':
            d['text'].append(i)
        elif text[i].lower() in 'backgrounds':
            d['background'].append(i)
    colors = dict()
    for i in colorDict.keys():
        if i in s:
            colors[i] = s.find(i)

    if len(colors.keys()) == 0:
        col = ("black", "white")
    elif len(d['text']) == 0:
        col = ('black', list(colors.keys())[0])
    elif len(d['background']) == 0:
        col = (list(colors.keys())[0], 'white')
    elif len(colors.keys()) == 1:
        c = list(colors.keys())[0]
        c1 = colors[c]
        if mindistance(c1, d['text']) < mindistance(c1, d['background']):
            col = (c, 'white')
        else:
            col = ('black', c)
    else:
        c1 = list(colors.keys())[0]
        c2 = list(colors.keys())[1]
        
        if (mindistance(colors[c1], d['text']) + mindistance(colors[c2], d['background'])
           < mindistance(colors[c2], d['text']) + mindistance(colors[c1], d['background'])):
            col = (c1, c2)
        else :
            col = (c2, c1)
    
    return hueSearch(col, text)
    
        
    
def getWeight(text):
    bold = ["bold", "strong", "heavy", "striking"]
    light = ['faint', 'thin', 'skinny', 'light']
    weight = 0
    if contains(bold, text):
        weight = 1
    elif contains(light, text):
        weight = -1
    return weight
    
def getOblique(text):
    oblique = ["italic", "fancy", "tilt"]
    return contains(oblique, text)

def underlined(text):
    underlined = ['underline', 'line']
    return contains(underlined, text)

def TextDesc(text):
    fmt = '{"textColor": "%s","size": "%s", "backgroundColor": "%s","font": { "weight": %s, "oblique": %s,  "underline": %s, }, }'
    size = getSize(text)
    textc, backc = getColors(text)
    weight = getWeight(text)
    ob = getOblique(text)
    underline = underlined(text)
    loc = getCol(text)
    return (fmt % (textc, size, backc, weight, ob, underline), str(loc))

def PicDesc(text):
    fmt = '{"size": "%s"}'
    loc = getCol(text)
    return (fmt % getSize(text), str(loc))


# ## Polymorphic Mappings

# In[99]:


ComponentContMap = {
    "Image" : pictureSearch,
    "Header" : TextWrite,
    "Subheader" : TextWrite,
    "Paragraph" : TextWrite,
    "Link" : LinkSearch,
    "Button": TextWrite
}
ComponentDescMap = {
    "Image" : PicDesc,
    "Header" : TextDesc,
    "Subheader" : TextDesc,
    "Paragraph" : TextDesc,
    "Link" : TextDesc,
    "Button": PicDesc    
}


# ## Create Dictionary

# In[100]:


def NewComponent(raw, _id):
    t = componentMap(raw['description'])

    cont = ComponentContMap[t](raw['content'])
    desc, loc = (ComponentDescMap[t](raw['description']))

    desc = eval(desc)
    if t == "Button":
        desc['link'] = LinkSearch(raw['content'])
    s = '{"type": "%s", "id" : "%s", "description" : %s, "content" : "%s", "column" : %s}' % (t,_id, desc, cont, loc)
    return json.loads(json.dumps(eval(s)))


def NewSite(d):
    s = '{"defaults":{"title": "%s", "defaultColors" :{"primaryColor":"#3286A8", "lighterColor": "", "darkerColor" : "" }},"components":[{"type":"navigation-bar", "id" : "navigation-bar-0"}]}' % d['title']
    return json.loads(json.dumps(s))


# ## S3 Interactions Tool

# In[96]:


AccessKey = "redacted"
SecretKey = "redacted"
def upload(data):
    session = boto3.Session(aws_access_key_id=AccessKey, aws_secret_access_key=SecretKey)
    s3 = session.resource('s3', )
    obj = s3.Object('htmlexa','schema.json')
    obj.put(Body=json.dumps(data))
def download():
    session = boto3.Session(aws_access_key_id=AccessKey, aws_secret_access_key=SecretKey)
    s3 = session.resource('s3')
    obj = s3.Object('htmlexa','schema.json')
    return json.loads(obj.get()['Body'].read())


# ## S3 Updates

# In[91]:


def processinfo(d):
    intent = d['intent']
    d = d['body']
    r = ''
    if intent == 'CreateSite':
        _new = NewSite(d)
        upload(_new)
    elif intent == 'AddComponent':
        n = componentMap(d['description'])
        current = json.loads(json.dumps(eval(str(download()))))
        comp = current['components']
        lastnum = -1
        for i in comp:
            if i["type"] == n:
                lastnum = int(i["id"].split("-")[-1])
        _new = NewComponent(d, n + "-" + str(lastnum + 1))
        d["id"] = _new["id"]
        current["components"].append(_new)
        upload(current)
    elif intent == 'EditComponent':
        current = json.loads(json.dumps(eval(str(download()))))
        comp = current['components']
        for i in comp:
            if i["id"].lower() == d['Item'] + "-" + d['Label']:
                desc, loc = ComponentDescMap[componentMap(d['Item'])](d['description'])
                i['description'] = desc if d['description'] != "" else i['description']
                i['content'] = d['content'] if d['content'] != "" else i['content']
                i['column'] = loc if d['description'] != "" else i['column']

        upload(current)
    return (d, intent)


# ## AWS Lambda Handler

# In[73]:


def lambda_handler(event, context):
    if event["request"]["type"] == "LaunchRequest":
        return eval('{"version": "1", "sessionAttributes": {"key": "hack"},"response": {"outputSpeech": {"type": "PlainText", "text": "Hello World"}},"reprompt": {"outputSpeech": {"type": "PlainText","text": "I didn\'t catch that, can you try again?"}},"directives": [], "shouldEndSession": False}' )
    elif event["request"]["type"] == "IntentRequest":
        request = dict()
        request['intent'] = event['request']['intent']['name']
        temp = event['request']['intent']['slots']
        request['body'] = dict()
        for slot in temp.keys():
            request['body'][slot] = "" 
            if 'value' in temp[slot]:
                request['body'][slot] = temp[slot]['value']
        r = processinfo(request)
        return toSpeech(r, False)
    else:
        return eval('{"version": "1", "sessionAttributes": {"key": "hack"},"response": {"outputSpeech": {"type": "PlainText", "text": "Hello World"}},"reprompt": {"outputSpeech": {"type": "PlainText","text": "I didn\'t catch that, can you try again?"}},"directives": [], "shouldEndSession": True}' )


# ## Unit Testing

# In[61]:


def test(event):
    processinfo({"intent" : "CreateSite", "body" : {"title" : "Test"}})
    return toSpeech(processinfo(event), False)


# ## Confirmation to Speech

# In[82]:


def toSpeech(r, end):
    body, intent = r
    fmt = '{"version": "1", "sessionAttributes": {"key": "hack"},"response": {"outputSpeech": {"type": "PlainText", "text": "%s"}},"reprompt": {"outputSpeech": {"type": "PlainText","text": "I didn\'t catch that, can you try again?"}},"shouldEndSession": %s}'
    text = ""
    if intent == "CreateSite":
        text = "Congrats, I made you a site!"
    elif intent == "AddComponent":
        text = "I made a %s for you. To edit this component, refer to it by %s" % (body["id"].split('-')[0], " ".join(body["id"].split('-')))
    elif intent == "EditComponent":
        text = "Updated to new description"
    return eval(fmt % (text,  end))


# In[101]:


download()


# In[89]:





# In[ ]:




