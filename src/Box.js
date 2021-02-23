import React, { useEffect, useState } from "react";


export function Box(props) {
    return <button className="box" onClick={props.onClick}>
        {props.value}
    </button>;
}