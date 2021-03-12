import './App.css';
import React, { useState, useRef, useEffect } from 'react';
import io from 'socket.io-client';
import Board from './Board';
import './Board.css';

const socket = io();

function App() {
  const inputRef = useRef();
  const [isLogin, setLogin] = useState(false);
  const [users, setUsers] = useState([]);
  const [showLBoard, setShowLBoard] = useState(false);
  const [lBoardName, setLBoardName] = useState([]);
  const [lBoardScore, setLBoardScore] = useState([]);
  const [playerName, setPlayerName] = useState(null);

  useEffect(() => {
    socket.on('login', (data) => {
      console.log(data);
      setUsers(data.users);
      setLBoardName(data.leaderBoardName);
      setLBoardScore(data.leaderBoardScore);
    });
    socket.on('updateBoard', (data) => {
      console.log(data);
      setLBoardName(data.boardName);
      setLBoardScore(data.boardScore);
    });
  }, []);

  function loginButton() {
    const userName = inputRef.current.value;
    setPlayerName(userName);

    socket.emit('login', { userName });
    setLogin(true);
  }

  function leaderBoardButton() {
    setShowLBoard(!showLBoard);
  }

  return (
    <div>
      {isLogin === true ? (
        <div className="grid">
          <div className="column1">
            <Board />
          </div>
          <div className="column2">
            <h2>User list</h2>
            {users.map((user) => (
              <li>{user}</li>
            ))}
            <div>
              <h3>LeaderBoard</h3>
              <button type="submit" onClick={leaderBoardButton}>
                Show/Hide leaderBoard
              </button>
              {showLBoard === true ? (
                <div>
                  <table>
                    <tbody>
                      <tr>
                        <th>username</th>
                        <th>score</th>
                      </tr>
                      {lBoardName.map((name, idx) => (
                        <tr
                          style={
                            playerName === name
                              ? { backgroundColor: '#0000ff80' }
                              : { backgroundColor: '#ff000080' }
                          }
                        >
                          <td>{name}</td>
                          <td>{lBoardScore[idx]}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div>
                  <p>Press button to see scores</p>
                </div>
              )}
            </div>
          </div>
        </div>
      ) : (
        <div align="center">
          <h1>enter username</h1>
          <input ref={inputRef} type="text" />
          <button type="submit" onClick={loginButton}>
            Login
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
