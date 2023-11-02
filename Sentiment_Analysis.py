from flask import Flask, render_template, request
from textblob import TextBlob

def spell_check(text):
    from spellchecker import SpellChecker
    spell = SpellChecker()

    # split the sentence into words
    words = text.split()
    words_updated = []

    # find misspelled words and replace them
    for i, word in enumerate(words):
        if spell.correction(word) != word:
            if spell.correction(word) is None : 
                words_updated.append(words[i]) 
            else:    
                words_updated.append(spell.correction(word))
        else : 
            words_updated.append(words[i]) 

    # join the corrected words back into a sentence
    corrected_text = " ".join(words_updated)
    
    return corrected_text

def text_blob(text):
    from textblob import TextBlob

    # Create a TextBlob object
    blob = TextBlob(text)

    #Create an empty dictionary
    dic = { 'performance' : [0,0],
           'steering' : [0,0],
           'stability' : [0,0],
           'adas' : [0,0],
           'comfort' : [0,0],
           'fun' : [0,0]
          }

    for sentence in blob.sentences:
        sentence2 = spell_check(sentence)  #Perform spell check 
        blob2 = TextBlob(sentence2)
        for aspect in dic.keys() :
            if aspect in blob2.sentences[0].lower():
                dic[aspect][0] += 1
                dic[aspect][1] += blob2.sentences[0].sentiment.polarity


    # Calculate the average polarity for each aspect
    polarities = {}
    for aspect in dic.keys() :
        if dic[aspect][0] > 0 :

            if ((dic[aspect][1]/dic[aspect][0]) >= -1) & ((dic[aspect][1]/dic[aspect][0]) <=0) : sentiment = "Negative"
            elif ((dic[aspect][1]/dic[aspect][0]) > 0) & ((dic[aspect][1]/dic[aspect][0]) <=0.3): sentiment = "Neutral"
            else : sentiment = "Positive"

            polarities.update({aspect+"_polarity": [round(dic[aspect][1]/dic[aspect][0],2),sentiment]})

        else : 
            polarities.update({aspect+"_polarity": [dic[aspect][0], "NA"]})    
            
    return polarities 


#Replace the path with your respective path
app = Flask(__name__, template_folder='/Users/harsha/Desktop/Capstone')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    message = request.form['message']
    
    polarities = text_blob(message)
    
    return render_template('result.html', sentiment=polarities)

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    