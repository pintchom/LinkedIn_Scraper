import logo from './logo.svg'
import './App.css'
import React, {useState} from 'react'


function App() {

  const [data, setData] = useState(null); //user data
  const [response, setResponse] = useState(null); //request response from scraper
  const [loading, setLoading] = useState(false); //loading screen toggle var

  async function sendData() {
    setLoading(true); // "Loading..." displayed after link submitted and before response arrives from backend
    const response = await fetch('http://127.0.0.1:5000/link', { // calling POST req via fetch to flask - local port 5000
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({data: data}) // posting link submitted to backend
    });

    const responseBody = await response.json(); // when response comes in from scraper...
    setLoading(false); // loading finishes ...
    setResponse(responseBody); //response set to post req response ...
    console.log(responseBody); //logged
  }

  function getData(val) { // just saving user linkedin input
    setData(val.target.value)
    console.warn(val.target.value)
  }

  return (
    <div className="App">
      <div style={{textAlign: 'center'}}>
        <h1>Input LinkedIn URL</h1>
        <input type="text" onChange={getData} />
        <button onClick={sendData}>Submit</button>
      </div>
      {loading ? <h1>Loading...</h1> : response && 
        <div style={{textAlign: 'left', paddingLeft: '40px'}}>
          {["Name", "Title", "Location", "About", "Experiences", "Education", "Recommendation"].map(key => (
            <div key={key}>
              <h2>{key}</h2>
              {Array.isArray(response[key]) && Array.isArray(response[key][0]) ? response[key].map((group, index) => (
                <div key={index}>
                  {group.map((item, i) => i === 0 ? <li key={i}>{item}</li> : <p key={i}>{item}</p>)}
                </div>
              )) : <p>{JSON.stringify(response[key])}</p>}
            </div>
          ))}
        </div>
      }
    </div>
  );
}

export default App;