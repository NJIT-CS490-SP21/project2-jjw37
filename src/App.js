import './App.css';
import './Board.css';
import { Board } from './Board.js';
import { useState, useRef, useEffect } from 'react'
import io from 'socket.io-client';

const socket = io();

function App() {
  const inputRef = useRef();
  const [isLogin, setLogin] = useState(false);
  const [users, setUsers] = useState([]);
  const [leaderBoard, setLeaderBoard] = useState([]);
  
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
    </div>
  );
}

export default App;