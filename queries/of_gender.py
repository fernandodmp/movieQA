from SPARQLWrapper import JSON, SPARQLWrapper

def sparql(movie_genre):
    wrapper = SPARQLWrapper("http://dbpedia.org/sparql")
    wrapper.setReturnFormat(JSON)
    wrapper.setQuery(
        '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX dbo: <http://dbpedia.org/ontology/>

        SELECT DISTINCT ?movie_name ?genre_name
        WHERE {{
        ?film a dbo:Film ; rdfs:label ?movie_name ; dct:subject ?genre  .
        ?genre rdfs:label ?genre_name .
        ?genre_name bif:contains "'{}'" .

        FILTER(LANG (?movie_name) = 'en')
        FILTER(LANG (?genre_name) = 'en')
        }}
        '''.format(movie_genre)
    )

    results = wrapper.query().convert()
    if len(results) > 0:
        answer = "Here are some movies of " + movie_genre + "\n"
        for result in results["results"]["bindings"][:20]:
            answer += "* " + result["movie_name"]["value"] + "\n"
        return answer
    else:
        return ""


print(sparql("Action"))