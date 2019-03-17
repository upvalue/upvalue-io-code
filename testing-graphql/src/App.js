import React, { useState, useEffect } from 'react';
import './App.css';

import { query } from './api';

const App = () => {
  const [hello, setHello] = useState('loading');

  useEffect(() => {
    setHello('hello world!');
    // query(`{ echo(str: "hello world!") }`).then(result => setHello(result.data.echo));
  }, []);

  return (<p>{hello}</p>);
}

export default App;
