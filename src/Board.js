import React from 'react'
import { Box } from './Box.js'

function getSquare(i) {
    return <Box value={i}/>;
}

export function Board(props) {
    return <div className="board">
        {getSquare(0)}
        {getSquare(1)}
        {getSquare(2)}
        {getSquare(3)}
        {getSquare(4)}
        {getSquare(5)}
        {getSquare(6)}
        {getSquare(7)}
        {getSquare(8)}
    </div>;
}