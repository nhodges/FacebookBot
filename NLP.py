from datetime import datetime, timedelta
import time
import string
import random

def removePunctuation(str):
    return str.translate(None, string.punctuation)

# input: g.user, i.e. mongodb user object
def sayHiTimeZone(user):
    user_now = getUserTime(user)
    if recentChat(user):
        return "Hi again"
    if user_now.hour < 12:
        return "Good morning"
    elif user_now.hour < 19:
        return "Good afternoon"
    else:
        return "Good evening"

# input: g.user
def sayByeTimeZone(user):
    user_now = getUserTime(user)
    goodnights = ["Good night", "Have a good night", "Bye now", "See you later"]
    byes = ["Goodbye", "Bye then", "See you later", "Bye, have a good day"]
    
    if user_now.hour > 20:
        return "%s :)"%goodnights[random.randint(0,len(goodnights))]
    else:
        return "%s :)"%byes[random.randint(0,len(byes))]

# input: g.user
def recentChat(user):
    last_seen = user['last_seen'] 
    timestamp = datetime.strptime(last_seen,"%Y-%m-%d %H:%M:%S")
    time_since_chat = datetime.now() - timestamp
    recent30min = timedelta(minutes=60)
    if time_since_chat < recent30min:
        return True
    else:
        return False

# input: g.user
def getUserTime(user):
    user_tz = user['timezone']
    offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    server_tz = offset / 60 / 60 * -1
    time_diff = user_tz - server_tz
    server_now = datetime.now()
    return server_now + timedelta(hours=time_diff)

def isGreetings(inp_str):
    string = removePunctuation(inp_str).lower()
    greetings = ['hi','hey','hello', 'greetings', 'good morning', 'good afternoon', 'good evening']
    for word in greetings:
        if word in string:
            return True
    return False

def isGoodbye(inp_str):
    string = removePunctuation(inp_str).lower()
    byes = ['bye', 'see you']
    for word in byes:
        if word in string:
            return True
    return False

def findVerb(sentence):
    result = []
    for chunk in sentence.chunks:
        if chunk.type in ['VP']:
            strings = [w.string for w in chunk.words if w.type in ['VB','VBP']]
            result.extend(strings)
        # print chunk.type, [(w.string, w.type) for w in chunk.words ]
    return result


def findNounPhrase(sentence):
    res = ""
    for chunk in sentence.chunks:
        if chunk.type == 'NP':
            res += " ".join([w.string for w in chunk.words if w.type not in ['PRP', 'DT']])
            res += " "
    return res

def findProperNoun(sentence):
    for chunk in sentence.chunks:
        if chunk.type == 'NP':
            for w in chunk.words:
                if w.type == 'NNP':
                    return w.string
    return None

def yelp(verbList):
    print verbList
    yelpVerbs = ['eat', 'drink', 'find']
    for verb in verbList:
        if verb.lower() in yelpVerbs:
            return True
    return False


def nearBy(sentence):
    res = ""
    for chunk in sentence.chunks:
        if chunk.type in ['PP', 'ADVP']:
            res += " ".join([w.string for w in chunk.words if w.type in ['RB', 'PRP', 'IN']])
            res += " "
    res = res.strip()
    if res in ['near', 'around here', 'around', 'here', 'near here', 'nearby', 'near by', 'close by', 'close']:
        return True
    return False
