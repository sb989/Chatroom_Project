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
                    text = messages[i]['m'];
                    sender = messages[i]['sender'];
                    dt = messages[i]['dt'];
                    message = dt +"\n "+sender+": "+text;
                    setMessages(m=>m.concat(message));
                    
                }
                console.log(data['username']);
            });
        });
    }
    
    function sendMessage(){
        React.useEffect()
    }
    
    function messageFormat(){
        console.log(messages);
        return messages.map((m,index)=><li key={index}>{m}</li>);
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
