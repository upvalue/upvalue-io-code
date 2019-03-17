import React from 'react';
import App from './App';
import { render, waitForElement } from 'react-testing-library';

it('renders without crashing', async () => {
  const { getByText } = render(<App />);
  await waitForElement(() => getByText("hello world!"));
});
