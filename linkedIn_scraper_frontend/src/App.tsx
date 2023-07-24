//import logo from './logo.svg'
import './App.css'
import React, { useState } from 'react';
import axios from 'axios';

const App: React.FC = () => {
  const [data, setData] = useState<string | null>(null);
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const sendData = async () => {
    setLoading(true);
    const response = await axios.post('http://127.0.0.1:5000/link', { data: data }, {
      headers: {
        'Content-Type': 'application/json'
      },
    });

    const responseBody = response.data;
    setLoading(false);
    setResponse(responseBody);
    console.log(responseBody);
  };

  const getData = (val: any) => {
    setData(val.target.value);
    console.warn(val.target.value);
  };

  return (
    <div className="App">
      <div style={{ textAlign: 'center' }}>
        <h1>Input LinkedIn URL</h1>
        <input type="text" onChange={getData} />
        <button onClick={sendData}>Submit</button>
      </div>
      {loading ? <h1>Loading...</h1> :
        response?.error ? <h1>{response.error}</h1> :
          response &&
          <div style={{ textAlign: 'left', paddingLeft: '40px' }}>
            {["Name", "Title", "Location", "About", "Experiences", "Education", "Recommendation"].map(key => (
              <div key={key}>
                <h2>{key}</h2>
                {Array.isArray(response[key]) && Array.isArray(response[key][0]) ? response[key].map((group: any, index: number) => (
                  <div key={index} style={{ marginBottom: '45px' }}>
                    {group.map((item: string, i: number) => i === 0 ? <li key={i}>{item}</li> : <p key={i}>{item}</p>)}
                  </div>
                )) : <p>{JSON.stringify(response[key])}</p>}
              </div>
            ))}
          </div>
      }
    </div>
  );
};

export default App;
