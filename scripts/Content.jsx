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
                var messages = data['msgs']['messages'];
                var size = messages.length;
                var i;
                var message,text,sender,dt;
                setMessages([]);
                for(i=0;i<size;i++)
                {
                    message = messages[i];
                    text = message['m'];
                    sender = message['sender'];
                    dt = message['dt'];
                    addMessage(text,dt,sender);
                }
                console.log(data['username']);
            });
        },[]);
    }
    
    function addMessage(text,dt,sender)
    {
        var message ={'dt':dt,'sender':sender,'text':text};
        setMessages(m=>m.concat(message));
    }
    
    function messageFormat(){
        return messages.map((m,index)=><li key={index}>{m['dt']}<br/>{m['sender']+": "+m['text']}</li>);
    }
    
    function receiveMessage(){
        React.useEffect(()=>{
            Socket.on('new message',(data)=>{
                if(data['sender'] == username)
                    return;
                addMessage(data['message'],data['dt'],data['sender']);
            });
        });
    }
    
    firstConnect();
    
    return (
        <div>
            <h1>CHAT</h1>
                <ol>
                    {messageFormat()}
                </ol>
                <Send username={username} addMessage={addMessage}/>
        </div>
    );
}
