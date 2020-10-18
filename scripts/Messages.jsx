import * as React from 'react';
import {Message} from './Message'
export function Messages(params)
{
    var messages = params['messages'];
    var copy = [...messages];
    
    function mess()
    {
        console.log("messages function");
        return copy.reverse().map((m,index)=>
            <Message
            m = {m}
            index = {index}
            />
            );
    }
    
    return <div className = "messages">
        {mess()}
    </div>
}