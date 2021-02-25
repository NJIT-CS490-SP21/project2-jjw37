import { Box } from './Box.js';
import React, { useEffect, useState } from "react";
import io from 'socket.io-client';

const socket = io();

export function Board(props) {
    const initialState = Array(9).fill(null);
    const [box, setBox] = useState(initialState);
    const [xNext, setXNext] = useState(true);
    
    
    
    function handleClick(i) {
        const newBox = [...box];
        newBox[i] = xNext ? 'X' : 'O';
        setBox(newBox);
        setXNext(!xNext);
         socket.emit('move', {i: i, xNext: !xNext});
    }
    
    useEffect(() => {
    socket.on('move', (data) => {
        console.log(data);
        console.log(Box[data.i]);
        setXNext(prevVal => data.xNext);
        setBox(prevBox => [...prevBox, prevBox[data.i] = !data.xNext ? 'X' : 'O']);
    });
  }, []);
    
    function renderBox(i) {
    return <Box value={box[i]} onClick= {() => handleClick(i)} />;
    }
    
    const curPlayer = `Current Player is: ${xNext ? "X" : "O"}`;
    
    return (
        <div>
        <div className = "curPlayer"> 
            {curPlayer}
        </div>
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
        </div>
    );
};