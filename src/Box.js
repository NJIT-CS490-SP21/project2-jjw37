import React from 'react';

export default function Box(props) {
  return (
    <button type="submit" className="box" onClick={props.onClick}>
      {props.value}
    </button>
  );
}
