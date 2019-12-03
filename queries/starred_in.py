from SPARQLWrapper import JSON, SPARQLWrapper

question_identifiers = ['which', 'what']
identifiers = ['movie', 'starred', 'star']
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

def sparql(actor_name):
    wrapper = SPARQLWrapper("http://dbpedia.org/sparql")
    wrapper.setReturnFormat(JSON)
    wrapper.setQuery(
        '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX dbo: <http://dbpedia.org/ontology/>

        SELECT DISTINCT ?movie_name ?actor_name
        WHERE {{
        ?film a dbo:Film ; rdfs:label ?movie_name ; dbo:starring ?actor .
        ?actor rdfs:label ?actor_name .
        ?actor_name bif:contains "'{}'"

        FILTER(LANG (?movie_name) = 'en')
        FILTER(LANG (?actor_name) = 'en')
        }}
        '''.format(actor_name)
    )

    results = wrapper.query().convert()
    if len(results["results"]["bindings"]) > 0:
        answer = "The following results were found:\n\n"
        answer_dict = {}
        for result in results["results"]["bindings"]:
            if result["actor_name"]["value"] not in answer_dict.keys():
                answer_dict[result["actor_name"]["value"]] = [result["movie_name"]["value"]]
            else:
                answer_dict[result["actor_name"]["value"]].append(result["movie_name"]["value"])
            #answer += result["actor_name"]["value"] + " starred in " + result["movie_name"]["value"] + "\n"
        
        for actor in answer_dict.keys():
            answer += "Movies starred by " + actor +  ":\n"
            for movie in answer_dict[actor]:
                answer += "* " + movie +"\n"
            answer+="\n"
        return answer
    else:
        return None