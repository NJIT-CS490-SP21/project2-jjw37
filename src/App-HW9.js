import logo from './logo.svg';
import './App.css';
import { ListItem } from './ListItem.js';
import { useState, useRef } from 'react'

function App() {
  const [myList, changeList] = useState([]);
  const inputRef = useRef(null);
  
  function onClickButton() {
    const userText = inputRef.current.value;
    changeList(prevList => [... prevList, userText]);
  }
  
  
  return (
    <div>
      <h1>Hello</h1>
      <input type = "text" />
      <button onClick={onClickButton}> Add stuff </button>
      <ul> 
        {myList.map(item => <ListItem name={item} />)}
      </ul>
    </div>
  );
}

export default App;

