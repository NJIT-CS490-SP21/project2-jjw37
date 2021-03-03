import './App.css';
<<<<<<< HEAD
import { ListItem } from './ListItem.js';
import { useState, useRef, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io(); // Connects to socket connection

function App() {
  const [messages, setMessages] = useState([]); // State variable, list of messages
  const inputRef = useRef(null); // Reference to <input> element

  function onClickButton() {
    if (inputRef != null) {
      const message = inputRef.current.value;
      // If your own client sends a message, we add it to the list of messages to 
      // render it on the UI.
      setMessages(prevMessages => [...prevMessages, message]);
      socket.emit('chat', { message: message });
    }
  }

  // The function inside useEffect is only run whenever any variable in the array
  // (passed as the second arg to useEffect) changes. Since this array is empty
  // here, then the function will only run once at the very beginning of mounting.
  useEffect(() => {
    // Listening for a chat event emitted by the server. If received, we
    // run the code in the function that is passed in as the second arg
    socket.on('chat', (data) => {
      console.log('Chat event received!');
      console.log(data);
      // If the server sends a message (on behalf of another client), then we
      // add it to the list of messages to render it on the UI.
      setMessages(prevMessages => [...prevMessages, data.message]);
    });
  }, []);

  return (
    <div>
      <h1>Chat Messages</h1>
      Enter message here: <input ref={inputRef} type="text" />
      <button onClick={onClickButton}>Send</button>
      <ul>
        {messages.map((item, index) => <ListItem key={index} name={item} />)}
      </ul>
=======
import './Board.css';
import { Board } from './Board.js';
import { useState, useRef, useEffect } from 'react'
import io from 'socket.io-client';

const socket = io();

function App() {
  const inputRef = useRef();
  const [isLogin, setLogin] = useState(false);
  const [users, setUsers] = useState([]);
  
  useEffect(() => {
    socket.on('login', (data) => {
      console.log(data)
      setUsers(data.users);
    });
  }, []);
  
  function loginButton() {
    const userName = inputRef.current.value;
    socket.emit('login', {userName: userName});
    setLogin(true);
  }
  
  return (
    <div>
      {isLogin === true ? (
        <div  className = 'grid'>
          <div className = 'column1'>
            <Board />
          </div>
          <div  className = 'column2'>
            <h2>User list</h2>
              {users.map((user) => <li>{user}</li>)}
          </div>
        </div>
      ) : (
      <div align ="center">
      <h1>enter username</h1>
      <input ref={inputRef} type="text" />
      <button onClick={loginButton}>Login</button>
      </div>
      )}
>>>>>>> milestone_1
    </div>
  );
}

export default App;