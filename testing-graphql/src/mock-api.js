import { graphql } from 'graphql';
import { makeExecutableSchema } from 'graphql-tools';

/**
 * You'll notice I've defined the entire schema in this file.
 * In practice, you'd simply get the schema by introspection
 * or sharing code between your backend and frontend.
 */
const typeDefs = `
type Query {
  echo(str: String!): String!
}
`;

/**
 * I've defined resolvers here rather than use addMockFunctionsToSchema.
 * Not only do I think this will lead to more realistic tests, but my
 * goal is to use this mock frontend during development, so I want the
 * resolvers to return relatively realistic results.
 */
const resolvers = {
  Query: {
    echo: (param, { str }) => str
  }
}

const schema = makeExecutableSchema({ typeDefs, resolvers });

export const mockQuery = (queryString) => {
  return graphql(schema, queryString);
}