import { Box } from './Box.js';
import React, { useEffect, useState } from "react";
import io from 'socket.io-client';

const socket = io();

export function Board(props) {
    const initialState = Array(9).fill(null);
    const [box, setBox] = useState(initialState);
    
    
    
    function handleClick(i) {
        const newBox = [...box];
        newBox[i] = 'X';
        setBox(newBox);
        socket.emit('move', {i: i});
    }
    
    useEffect(() => {
    socket.on('move', (data) => {
        console.log(data);
        console.log(Box[data.i]);
        setBox(prevBox => [...prevBox, prevBox[data.i] = 'X']);
    });
  }, []);
    
    function renderBox(i) {
    return <Box value={box[i]} onClick= {() => handleClick(i)} />;
    }
    
    return <div className="board">
        {renderBox(0)}
        {renderBox(1)}
        {renderBox(2)}
        {renderBox(3)}
        {renderBox(4)}
        {renderBox(5)}
        {renderBox(6)}
        {renderBox(7)}
        {renderBox(8)}
    </div>;
}