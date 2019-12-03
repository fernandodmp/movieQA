from nltk.tokenize import word_tokenize
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
from queries import director, directed_by, synopsis, country, language, actors, starred_in, category
import string, time, sys

if len(sys.argv) > 1 and sys.argv[1] == "-i":
    nltk.download('averaged_perceptron_tagger')
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')


def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV }
    return tag_dict.get(tag, wordnet.NOUN)

lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')
table = str.maketrans('', '', string.punctuation)

if __name__ == "__main__":
    
    DEBUG = False
    if len(sys.argv) > 1 and sys.argv[1] == "-d":
        DEBUG = True

    while True:
        print("Make me a question!")
        question = input()
        if question.lower() == "exit":
            break
        print("Processing the question...")
        if DEBUG:
            initial_time = time.time()
            initial_processing_time = time.time()
        question_words = question.split()

        processed_question = [word.translate(table) for word in question_words]

        tagged_words = nltk.pos_tag(processed_question)

        processed_question = [word for word in tagged_words if word[0] not in stop_words]

        lemmatized_question = ([(lemmatizer.lemmatize(word[0],get_wordnet_pos(word[0])), word[1]) for word in processed_question])

        tagged_words = lemmatized_question
        
        if DEBUG:
            print(tagged_words)
            print("The processing took {0:.2f}s".format(time.time() - initial_processing_time ))

        
        initial_search_time = time.time()
        print('Searching...\n')
        possible_matches = [
            director.match,
            directed_by.match,
            synopsis.match,
            country.match,
            language.match,
            starred_in.match,
            actors.match,
            category.match
        ]
        
        answer_found = False
        for possible_match in possible_matches:
            if DEBUG:
                answer = possible_match(tagged_words)
                if answer:
                    print(answer)
                    answer_found = True
                    break
            
            else:
                try:
                    answer = possible_match(tagged_words)
                    if answer:
                        print(answer)
                        answer_found = True
                        break
                except:
                    pass
        if(not answer_found):
            print("We could not find what you're looking for\n")
        
        if DEBUG:
            print("The search took {0:.2f}s".format(time.time() - initial_search_time ))
            print("The overall question answering took {0:.2f}s".format(time.time() - initial_time))
    
