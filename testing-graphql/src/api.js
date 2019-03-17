export const query = (queryString) => {
  if (process.env.REACT_APP_MOCK_API || process.env.NODE_ENV === 'test') {
    return import('./mock-api').then(module => module.mockQuery(queryString));
  };
  throw new Error('api not implemented');
}
