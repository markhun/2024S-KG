// find genres and books
MATCH (b)-[:hasGENRE]->(n:Genre)
// split genre labels by comma
WITH b, n, split(n.genre,',') as genres
// turn list of labels in to rows of label
UNWIND genres as genre
// get-or-create an genre with that label
MERGE (a:Genre {genre:genre})
// if it's a new genre node, then the previous one was a a combined genre
WITH * WHERE n <> a
// get rid of the combined genre and it's relationships
DETACH DELETE n
// create a new relationship to the book
MERGE (b)-[:hasGENRE]->(a);