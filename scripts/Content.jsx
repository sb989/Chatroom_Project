import * as React from 'react';
import { Socket } from './Socket';
import { Send } from './Send';
import {MessageBox} from './MessageBox'
export function Content() {
    const[messages,setMessages] = React.useState([]);
    const[username,setUsername]= React.useState(null);
   
    
    return (<MessageBox username={username} setUsername={setUsername} 
    messages={messages} setMessages={setMessages}/>);
}
