from SPARQLWrapper import JSON, SPARQLWrapper

question_identifiers = ['what', 'which']
identifiers = ['country', 'nationality']
possible_tags = ['WP', 'WDT', 'JJ']

def match(tagged_words):
    question = ''.join([(word[0] + ' ') for word in tagged_words])
    question = question.lower()
    if (tagged_words[0][1] in possible_tags and tagged_words[0][0].lower() in question_identifiers):
        for identifier in identifiers:
            if identifier in question:
                question, name = question.split(identifier, 1)
                return sparql(name)
    return None


def sparql(movie_name):
    wrapper = SPARQLWrapper("http://dbpedia.org/sparql")
    wrapper.setReturnFormat(JSON)
    wrapper.setQuery(
        '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX dbo: <http://dbpedia.org/ontology/>

        SELECT DISTINCT ?movie_name ?country
        WHERE {{
        ?film a dbo:Film ; rdfs:label ?movie_name ; dbp:country ?country .
        ?movie_name bif:contains "'{}'" .

        FILTER(LANG (?movie_name) = 'en')
        }}
        '''.format(movie_name)
    )
    
    results = wrapper.query().convert()
    if len(results["results"]["bindings"]) > 0:
        answer = "The following results were found:\n\n"
        answer_dict = {}
        for result in results["results"]["bindings"]:
            if result["movie_name"]["value"] not in answer_dict.keys():
                answer_dict[result["movie_name"]["value"]] = [result["country"]["value"]]
            else:
                answer_dict[result["movie_name"]["value"]].append(result["country"]["value"])
            #answer += "The country of " + result["movie_name"]["value"] + " is " + result["country"]["value"] + "\n"
        
        for movie in answer_dict.keys():
            answer += "The countries in " + movie +  " are:\n"
            for country in answer_dict[movie]:
                answer += "* " + country +"\n"
            answer+="\n"
        return answer
    else:
        return None

    results = wrapper.query().convert()
    if len(results) > 0:
        answer = ""
        for result in results["results"]["bindings"]:
            answer += "The country of " + result["movie_name"]["value"] + " is " + result["country"]["value"] + "\n"
        return answer
    else:
        return None