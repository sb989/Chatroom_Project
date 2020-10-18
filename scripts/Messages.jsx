import * as React from 'react';
import {Message} from './Message'
export function Messages(params)
{
    var messages = params['messages'];
    var copy = [...messages];
    
    function mess()
    {
        console.log("messages function");
        console.log("email"+params['email']);
        return copy.reverse().map((m,index)=>
            <Message
            m = {m}
            index = {index}
            email = {params['email']}
            />
            );
    }
    
    return (<div className = "messages">
        {mess()}
    </div>)
}