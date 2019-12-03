from SPARQLWrapper import JSON, SPARQLWrapper

question_identifiers = ['which', 'what']
identifiers = ['movie', 'directed', 'direct']
possible_tags = ['WP', 'WDT', 'JJ']

def match(tagged_words):
    question = ''.join([word[0] for word in tagged_words])
    question = question.lower()
    if (tagged_words[0][1] in possible_tags and tagged_words[0][0].lower() in question_identifiers):
        if identifiers[0] in question and (identifiers[1] in question or identifiers[2] in question):
            name = ""
            first = True
            for word in tagged_words:
                if (word[1] == 'NNP'):
                    if(first):
                        name += word[0]
                        first = False                                                       
                    else:
                        name += ' ' + word[0]
            return sparql(name)
    return None

def sparql(director_name):
    wrapper = SPARQLWrapper("http://dbpedia.org/sparql")
    wrapper.setReturnFormat(JSON)
    wrapper.setQuery(
        '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX dbo: <http://dbpedia.org/ontology/>

        SELECT DISTINCT ?movie_name ?director_name
        WHERE {{
        ?film a dbo:Film ; rdfs:label ?movie_name ; dbo:director ?director .
        ?director rdfs:label ?director_name .
        ?director_name bif:contains "'{}'"

        FILTER(LANG (?movie_name) = 'en')
        FILTER(LANG (?director_name) = 'en')
        }}
        '''.format(director_name)
    )

    results = wrapper.query().convert()
    if len(results["results"]["bindings"]) > 0:
        answer = "The following results were found:\n"
        answer_dict = {}
        for result in results["results"]["bindings"]:
            if result["director_name"]["value"] not in answer_dict.keys():
                answer_dict[result["director_name"]["value"]] = [result["movie_name"]["value"]]
            else:
                answer_dict[result["director_name"]["value"]].append(result["movie_name"]["value"])
            #answer += result["director_name"]["value"] + " is the director of " + result["movie_name"]["value"] + "\n"
        
        for director in answer_dict.keys():
            answer += "Movies directed by " + director +  ":\n"
            for movie in answer_dict[director]:
                answer += "* " + movie +"\n"
            answer+="\n"
        return answer
    else:
        return None