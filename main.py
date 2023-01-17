from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha


#Speech Engine Initialization
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) #0 = male, 1 = female
activationWord = "computer" #AI wake word


#Choose a browser
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

#Wolfram Alpha Client
appID = 'LL8RRA-UV642G53GK'
wolframClient = wolframalpha.Client(appID)

def speak(text, rate = 120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait() #starts running the engine and does not stop until process completes

def parseCommand():
    listener = sr.Recognizer() #speech-to-text
    print('Good morning master') #aknowledging wake word

    with sr.Microphone() as source:
        listener.pause_threshold = 1 #gap before ending listening
        input_speech = listener.listen(source)

    try:
        print('Trying to figure out what in the world you just said to me...')
        query = listener.recognize_google(input_speech, language='en_gb') #Running speech against database
        print(f'Pretty sure you said something along the lines of "{query}"')
    except Exception as exception:
        print('dawg say it wit ya chest')
        speak('speak up nerd')
        print(exception)
        return 'None'

    return query


def search_wikipedia(query):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('Nothing found on the subject')
        speak("That doesn't exist LOL")
        return 'No result recieved'
    try:
        wikiPage = wikipedia.page(searchResults[0])          #Grab the first result
    except wikipedia.DisambiguationError as error:                   #Unless there's a disambiguation error
        wikiPage = wikipedia.page(error.options[0])                  #If so, grab the first result of the error
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']

def search_wolframAlpha(query = ''):
    response = wolframClient.query(query)         # "@success" = query was resolvable, "@numpods" = number of results returned, "pod" = list of results possible containing subpods
    if response ['@success'] == 'false':
        return 'Could not compute'
    
    #Query resolved
    else:
        result = ''
       
        #Question
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]
        #May contain the answer, has the highest confidence value
        #if it's primary or has title of result or definition, then it's the official result
        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            #Get the result
            result = listOrDict(pod1['subpod'])
            #remove bracketed sections from result
            return result.split('(')[0]
        else:
            question = listOrDict(pod0['subpod'])
            #remove bracketed sections from result
            return question.split('(')[0]
            #search wikipedia instead
            speak('Computation failed. Checking that one website teachers hate.')
            return search_wikipedia(question)








#Main Loop


if __name__ == '__main__':
    speak('Hold on dude let me wake up a little bit')

    while True:
        #Parse as a list
        query = parseCommand().lower().split()
        
        if query[0] == activationWord:
            query.pop(0)
            
            
            #List Commands


            if query[0] == 'say':                   #keyword here is "say"
                if 'hello' in query:
                    speak('no.')
                else:
                    query.pop(0) #remove say
                    speech = ' '.join(query)
                    speak(speech)
            

            #Navigation
            if query[0] == 'look' and query[1] == 'up':
                speak("fine. I'll open your browser for you you lazy sack of potatos")
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)

            
            #Wikipedia
            if query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                speak("Checking that one website teachers hate.")
                speak(search_wikipedia(query))


            #Wolfram Alpha
            if query[0] == 'compute' or query[0] == 'computer' or query[0] == 'computes':
                query = ' '.join(query[1:])
                speak("I can't believe you would make me think. How dare you.")
                try:
                    result = search_wolframAlpha(query)
                    speak(result)
                except:
                    speak('nah im too dumb for that.')
            

            #Note Taking
            if query[0] == 'log':
                speak('fine but im deleting your games to make room')
                newNote = parseCommand().lower()
                now = datetime.now().strftime('%Y-%m-$d-%H-%M-%S')

                with open('note_%s.txt' % now, 'w') as newFile:
                    newFile.write(newNote)
                speak('I wrote it down for you princess.')
            
            #Exit Protocol
            if query[0] == 'exit':
                speak('yeah yeah whatever')
                break


