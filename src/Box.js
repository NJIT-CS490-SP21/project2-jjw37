import React, { useEffect, useState } from "react";


export function Box(props) {
    const [value, setValue] = useState(null);
    return <button className="box" onClick={() => setValue('X')}>
        {value}
    </button>;
}