from SPARQLWrapper import JSON, SPARQLWrapper

question_identifiers = ['what']
identifiers = ['synopsis', 'abstract', 'resume']
possible_tags = ['WP']

def match(tagged_words):
    question = ''.join([(word[0] + ' ') for word in tagged_words])
    question = question.lower()
    if (tagged_words[0][1] == "WP" and tagged_words[0][0].lower() == "what"):
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

        SELECT DISTINCT ?movie_name ?abstract
        WHERE {{
        ?film a dbo:Film ; rdfs:label ?movie_name ; dbo:abstract ?abstract .
        ?movie_name bif:contains "'{}'" .

        FILTER(LANG (?movie_name) = 'en')
        FILTER(LANG (?abstract) = 'en')
        }}
        '''.format(movie_name)
    )

    results = wrapper.query().convert()
    if len(results["results"]["bindings"]) > 0:
        answer = "The following results were found:\n\n"
        answer_dict = {}
        for result in results["results"]["bindings"]:
            if result["movie_name"]["value"] not in answer_dict.keys():
                answer_dict[result["movie_name"]["value"]] = [result["abstract"]["value"]]
            else:
                answer_dict[result["movie_name"]["value"]].append(result["abstract"]["value"])
            #answer += "The synopsis of " + result["movie_name"]["value"] + " is:\n " + result["abstract"]["value"] + "\n\n"
        
        for movie in answer_dict.keys():
            answer += "The synopsis of " + movie +  " is:\n"
            for abstract in answer_dict[movie]:
                answer += "* " + abstract +"\n"
            answer+="\n"
        return answer
    else:
        return None