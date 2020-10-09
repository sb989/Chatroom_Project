import * as React from 'react';
import { Socket } from './Socket';
import { Send } from './Send';

export function Content() {
    const[messages,setMessages] = React.useState([]);
    const[username,setUsername]= React.useState('');
   
    function firstConnect(){
        React.useEffect(()=>{
            Socket.on('connected',(data)=>{
                console.log("connected");
                setUsername(data['username']);
                data['msgs'].forEach((msg)=>{
                    setMessages(msg);
                });
                
                console.log(data['username']);
            });
        });
    }
    
    function sendMessage(){
        React.useEffect()
    }
    
    function messageFormat(){
        return messages.map(m=>{
            <li>{m}</li>
        });
    }
    
    
    firstConnect();
    
    return (
        <div>
            <h1>CHAT</h1>
                <ol>
                    {messageFormat()}
                </ol>
                <Send username={username}/>
        </div>
    );
}
