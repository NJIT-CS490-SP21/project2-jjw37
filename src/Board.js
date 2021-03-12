import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import Box from './Box';

const socket = io();

export default function Board() {
  const initialState = Array(9).fill(null);
  const [box, setBox] = useState(initialState);
  const [xNext, setXNext] = useState(true);
  const [counter, setCounter] = useState(0);
  const [isSpectator, setSpectator] = useState(false);
  const [isPlayer, setPlayer] = useState(false);
  const [isWinner, setWinner] = useState(false);

  function calculateWinner(boxes) {
    const lines = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6],
    ];
    for (const line of lines) {
      const [a, b, c] = line;
      if (boxes[a] && boxes[a] === boxes[b] && boxes[a] === boxes[c]) {
        return boxes[a];
      }
    }
    return null;
  }

  function handleClick(i) {
    const newBox = [...box];
    const winnerStat = Boolean(calculateWinner(newBox));
    const squareState = Boolean(newBox[i]);
    if (isSpectator === true && isPlayer === false) return;
    if (winnerStat || squareState) return;
    newBox[i] = xNext ? 'X' : 'O';
    setBox(newBox);
    setXNext(!xNext);
    setCounter((prevCount) => prevCount + 1);
    socket.emit('move', { i, xNext: !xNext });
    const stateAfter = Boolean(calculateWinner(newBox));
    if (stateAfter === true) {
      setWinner(true);
      socket.emit('winner', { xNext: !xNext });
    }
  }

  useEffect(() => {
    socket.on('move', (data) => {
      console.log(data.i);
      console.log(data.xNext);
      setCounter((prevCount) => prevCount + 1);
      setXNext(data.xNext);
      setBox((prevBox) => {
        const socketBox = [...prevBox];
        socketBox[data.i] = !data.xNext ? 'X' : 'O';
        return socketBox;
      });
    });
  }, []);

  useEffect(() => {
    socket.on('restart', (data) => {
      console.log(data);
      setXNext(true);
      setCounter(0);
      const freshState = Array(9).fill(null);
      setBox(freshState);
      setWinner(false);
    });
  }, []);

  useEffect(() => {
    socket.on('user_count', (data) => {
      if (data.counter > 2 && isPlayer === false) setSpectator(true);
      if (data.counter < 3) setPlayer(true);
    });
  }, [isPlayer]);

  function restartGame() {
    if (isSpectator === true && isPlayer === false) return;
    console.log(counter);
    const winnerStat = Boolean(calculateWinner(box));
    if (winnerStat === false && counter !== 9) {
      return;
    }
    setXNext(true);
    setCounter(0);
    setBox(initialState);
    setWinner(false);
    socket.emit('restart', { counter });
  }

  function renderBox(i) {
    return <Box value={box[i]} onClick={() => handleClick(i)} />;
  }

  let winnerPlayer = 'The game is in progress';
  const curPlayer = `Current Player is: ${xNext ? 'X' : 'O'}`;
  const winner = calculateWinner(box);
  if (winner) {
    winnerPlayer = `The winner is player ${winner}`;
  }
  if (counter === 9 && isWinner === false) {
    winnerPlayer = 'Game ends in draw';
  }

  return (
    <div>
      <div className="curPlayer">{curPlayer}</div>
      <div className="board">
        {renderBox(0)}
        {renderBox(1)}
        {renderBox(2)}
        {renderBox(3)}
        {renderBox(4)}
        {renderBox(5)}
        {renderBox(6)}
        {renderBox(7)}
        {renderBox(8)}
      </div>
      <div className="winnerStatus">{winnerPlayer}</div>
      <div align="center">
        <button type="submit" className="restart" onClick={() => restartGame()}>
          Restart Game
        </button>
      </div>
    </div>
  );
}
