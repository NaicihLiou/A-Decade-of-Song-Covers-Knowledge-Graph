# save this as app.py
import json
from flask import Flask, request, render_template
from neo4j import GraphDatabase
# from py2neo import Graph
# import py2neo.client.json

app = Flask(__name__)
app.debug = True



def execute_query_neo4j(uri, user, password, query_cmd):
    result = None
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session(database="neo4j") as session:
        result = session.execute_write(query_neo4j, query_cmd)
        print(result); print('='*40)
    driver.close()
    return result

def query_neo4j(tx, query_cmd):
    result = tx.run(query_cmd)
    return [{'song':elem['song'], 'singer':elem['singer']} for elem in result]

    for elem in result:
        try:
            print(elem['n'].get('name'))
            # print(elem.data()['n']['name'])
            # print(json.dumps(elem.data()))
        except:
            print( 'nooooo')
    return result
    # return result.single()[0]

# def print_friends(tx, name):
#     query = ("MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
#              "RETURN friend.name ORDER BY friend.name")
#     for record in tx.run(query, name=name):
#         print(record["friend.name"])

@app.route("/")
def hello():
    print('='*40+'bf query')
    #     cmd = """MATCH (ee:Person)-[:KNOWS]-(friends)
    # WHERE ee.name = 'Emil' RETURN ee, friends"""
    # cmd = "MATCH (n) RETURN n LIMIT 10"
    # execute_query_neo4j("bolt://localhost:7687", "neo4j", "dsci558", cmd)
    return render_template('index.html')

@app.route("/songQuery", methods=['GET'])
def songQuery():
    song = request.args.get('songInput')
    singer = request.args.get('singerInput')
    year = request.args.get('yearInput')
    print(f'Query Input\tsong = {song}\tsinger = {singer}\tyear = {year}')

    where_cmds = []
    # query by song title
    if song:    
        where_cmds += [f'song.rdfs__title CONTAINS "{song}"']
        # ns0__original_song
        # cmd = f'MATCH (song:ns0__cover_song)-[:ns1__sung_by]->(singer:ns0__singer) WHERE song.rdfs__title CONTAINS "{song}" RETURN song, singer LIMIT 20;'

    # query by singer name
    if singer:
        where_cmds += [f'singer.rdfs__title	CONTAINS "{singer}"']
        # cmd=f'MATCH (n:ns0__singer) WHERE n.rdfs__title CONTAINS "Art" RETURN n.rdfs__title LIMIT 10;'
        # cmd = f'MATCH (song:ns0__cover_song)-[:ns1__sung_by]->(singer:ns0__singer) WHERE singer.rdfs__title	CONTAINS "{singer}" RETURN song, singer LIMIT 20;'
  
    # query by released year
    if year:
        where_cmds += [f'song.rdfs__release_date <= date("{year}-12-31") AND song.rdfs__release_date >= date("{year}-01-01")']
        # cmd = f'MATCH (n:ns0__cover_song) WHERE n.rdfs__release_date <= date("{year}-12-31") AND n.rdfs__release_date >= date("{year}-01-01") RETURN n LIMIT 10;'
        # cmd = f'MATCH (song:ns0__cover_song)-[:ns1__sung_by]->(singer:ns0__singer) WHERE song.rdfs__release_date <= date("2015-12-31") AND song.rdfs__release_date >= date("2015-01-01") RETURN song, singer LIMIT 20;'
    
    where_cmd = ' AND '.join(where_cmds)
    cmd = f'MATCH (song)-[:ns1__sung_by]->(singer:ns0__singer) WHERE {where_cmd} RETURN song, singer LIMIT 10;'
    print('='*40,f'cmd = {cmd}', '='*40)
    result_elems = execute_query_neo4j("bolt://localhost:7687", "neo4j", "dsci558", cmd)
   
    result = []
    for result_elem in result_elems:
        song_to_print = {}
        for target in ['singer', 'song']:
            elem = result_elem[target]
            for k, v in elem.items():
                if k == 'uri': continue
                
                k = k.replace('rdfs__', '')
                if k == 'title': k = target
                song_to_print[k] = v

        for k in ['song','singer','has_writers','release_date','award','tag','birth_date','facebook','instagram','twitter','webpage','award']:
            song_to_print[k] = song_to_print.get(k, '')
        
        # Extract first element in list format
        if song_to_print['has_writers']: 
            song_to_print['has_writers'] = song_to_print['has_writers'].split(',')[0]
        result.append(song_to_print)
    
    
    # print(result)
    return render_template('index.html', queryResult=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=50000, debug=True)
