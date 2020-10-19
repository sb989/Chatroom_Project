import * as React from 'react';
import {Message} from './Message'
export function Messages(params)
{
    var messages = params['messages'];
    var copy = [...messages];
    
    function mess()
    {
        return copy.reverse().map((m,index)=>
            <Message
            m = {m}
            index = {index}
            email = {params['email']}
            key = {index}
            />
            );
    }
    
    return (<div className = "messages">
        {mess()}
    </div>)
}