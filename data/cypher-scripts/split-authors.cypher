// find authors and books
MATCH (n:Author)-[:WROTE]->(b)
// split author name by comma
WITH b, n, split(n.author,', ') as names
// turn list of names in to rows of name
UNWIND names as name
// get-or-create an author with that name
MERGE (a:Author {name:name})
// if it's a new author node, then the previous one was a a combined author
WITH * WHERE n <> a
// get rid of the combined author and it's relationships
DETACH DELETE n
// create a new relationship to the book
MERGE (a)-[:WROTE]->(b);