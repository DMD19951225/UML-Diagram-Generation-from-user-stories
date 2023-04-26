import logo from './logo.svg';
import React,{Component, useState} from 'react';
import axios from 'axios';
import './App.css'


function App() {
  const [text, setText] = useState("")
  const [url, setUrl] = useState("")
  const sendText = async () => {
    console.log(text)
    const sentence = {
      "sentence" : text
    }
    await axios.post("http://localhost:8000/createUml/", sentence)
      .then(res => {
        console.log(res.data.url);
        const testUrl = res.data.url

        setUrl(res.data.url)
      })
  }
  return (
    <div className="App">
      <div className='upload'>

        <label>Input senteces</label>
        <input onChange={(e) => setText(e.target.value)}></input>
        <button onClick={() => sendText()}>Send</button>
      </div>
      <img src={"http://localhost:8000"+url}/>
    </div>
  );
}

export default App;
