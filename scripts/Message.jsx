import * as React from 'react';
import {MessageBox} from './MessageBox';
export function Message(params)
{
    var m = params['m'];
    var index = params['index'];
    var cBox = "receivedBox";
    var cMessage = "receivedMessage";
    var cName = "receivedMessageName";
    var cText = "receivedMessageText";
    var text = m['text'];
    var name = m['name'];
    var email = params['email'];
    
    if(m['email']===email)
    {
        cBox = "sentBox"
        cMessage = "sentMessage"
        cName = "sentMessageName"
        cText = "sentMessageText"
    }
    return (<div key = {index} 
    className = {m["same_or_diff_sender"]}
    index = {index}>
        <MessageBox
            m = {m}
            index = {index}
            cBox = {cBox}
            cMessage = {cMessage}
            cName = {cName}
            cText = {cText}
            text = {text}
            name = {name}
            email = {email}
            key = {index}
        />
        </div>)
    
}