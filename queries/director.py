from SPARQLWrapper import JSON, SPARQLWrapper

identifiers = ["directs", "director", "direct"]

def match(tagged_words):
    question = ''.join([(word[0] + ' ') for word in tagged_words])
    question = question.lower()
    if (tagged_words[0][1] == 'WP' and tagged_words[0][0].lower() == "who"):
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

        SELECT DISTINCT ?movie_name ?director_name
        WHERE {{
        ?film a dbo:Film ; rdfs:label ?movie_name ; dbo:director ?director .
        ?movie_name bif:contains "'{}'" .
        ?director rdfs:label ?director_name .

        FILTER(LANG (?movie_name) = 'en')
        FILTER(LANG (?director_name) = 'en')
        }}
        '''.format(movie_name)
    )

    results = wrapper.query().convert()
    if len(results["results"]["bindings"]) > 0:
        answer = "The following results were found:\n"
        answer_dict = {}
        for result in results["results"]["bindings"]:
            if result["movie_name"]["value"] not in answer_dict.keys():
                answer_dict[result["movie_name"]["value"]] = [result["director_name"]["value"]]
            else:
                answer_dict[result["movie_name"]["value"]].append(result["director_name"]["value"])
            #answer += "The director of " + result["movie_name"]["value"] + " is " + result["director_name"]["value"] + "\n"
        
        for movie in answer_dict.keys():
            answer += "The directors in " + movie +  " are:\n"
            for director in answer_dict[movie]:
                answer += "* " + director +"\n"
            answer+="\n"
        return answer
    else:
        return None