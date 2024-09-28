import string

collbaorative_filtering = string.Template(
    """
MATCH (u:User {user_id:$user_id})
MATCH (u)-[r:RATED]->(book)
WHERE r.rating >= 4
WITH u, r, book
ORDER BY r.rating DESC LIMIT 150

MATCH (book)<-[r2:RATED]-(peer)
WHERE NOT u=peer
AND r.rating = r2.rating
WITH DISTINCT u, peer LIMIT 1500

MATCH (u)-[r:RATED]->(book)
WITH peer, collect(distinct book) as alreadyRead

MATCH (peer)-[r3:RATED]->(reco)
WHERE r3.rating >= 4
AND NOT reco in alreadyRead

// count how frequently the recommend book shows up
WITH reco, count(reco) as freq
RETURN reco.book_id AS id, reco.image_url AS image_url, reco.original_title AS Title, reco.average_rating AS average_rating, freq, (freq*reco.average_rating) AS score
ORDER BY score DESC LIMIT 100
"""
)

graphSAGE_similar_books = string.Template(
    """
MATCH (u:User {user_id:$user_id})
MATCH (u)-[r:RATED]->(b)
WITH u, collect(distinct b) as alreadyRead

MATCH (u)-[r:RATED]->(book)
WHERE r.rating >= 4
WITH u, r, book, alreadyRead
ORDER BY r.rating DESC LIMIT 150

MATCH (book)-[s:SIMILAR_GRAPHSAGE_EMBEDDING]->(reco)
WHERE NOT reco in alreadyRead
WITH reco, count(reco) as freq

RETURN reco.book_id as id, reco.image_url AS image_url, reco.original_title AS Title, reco.average_rating AS average_rating, freq, (freq*reco.average_rating) AS score
ORDER BY score DESC LIMIT 20    
"""
)

graphSAGE_similar_users = string.Template(
    """
MATCH (u:User {user_id:$user_id})
MATCH (u)-[r:RATED]->(b)
WITH u, collect(distinct b) as alreadyRead

MATCH (u)-[s:SIMILAR_GRAPHSAGE_EMBEDDING]->(peer:User)
WITH u, s, peer, alreadyRead
ORDER BY s.score DESC LIMIT 150

MATCH (peer)-[r:RATED]->(reco)
WHERE r.rating >= 4
AND NOT reco in alreadyRead

// count how frequently the recommend book shows up
WITH reco, count(reco) as freq

RETURN reco.book_id AS id, reco.image_url AS image_url, reco.original_title AS Title, reco.average_rating AS average_rating, freq, (freq*reco.average_rating) AS score
ORDER BY score DESC LIMIT 20
"""
)

fastRP_similar_books = string.Template(
    """
MATCH (u:User {user_id:$user_id})
MATCH (u)-[r:RATED]->(b)
WITH u, collect(distinct b) as alreadyRead

MATCH (u)-[r:RATED]->(book)
WHERE r.rating >= 4
WITH u, r, book, alreadyRead
ORDER BY r.rating DESC LIMIT 150

MATCH (book)-[s:SIMILAR_FASTRP_EMBEDDING]->(reco)
WHERE NOT reco in alreadyRead
WITH reco, count(reco) as freq

RETURN reco.book_id as id, reco.image_url AS image_url, reco.original_title AS Title, reco.average_rating AS average_rating, freq, (freq*reco.average_rating) AS score
ORDER BY score DESC LIMIT 20
"""
)


liked_books = string.Template(
    """
MATCH (u:User {user_id:$user_id})
MATCH (u)-[r:RATED]->(book:Book)
WITH r, book LIMIT 80

MATCH (book)<-[:WROTE]-(author:Author)
WITH r, book, collect(author.name) as authors

OPTIONAL MATCH (book)-[:hasGENRE]->(genre)
WITH r, book, authors, collect(genre.genre) as genres

RETURN book.book_id, book.image_url, book.isbn, book.original_title, book.title, authors as WROTE, genres AS hasGENRE, r.rating as RATED, book.average_rating, book.dbpedia_resource
ORDER BY r.rating DESC, book.average_rating DESC LIMIT 80
"""
)
