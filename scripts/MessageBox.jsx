import * as React from 'react';
import { Socket } from './Socket';
import { Send } from './Send';

export function MessageBox(params){
    var username = params['username'];
    var setUsername = params['setUsername'];
    var messages = params['messages'];
    var setMessages = params['setMessages'];
    
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
        
        return messages.map((m,index)=>divClass(m,index));
    }
    
    function divClass(m,index)
    {
        var dClass = <div className="receivedBox" id={index} key={index}><div className="receivedMessage" key={index}> <div className="receivedMessageName">{m['sender']}</div><div className="receivedMessageText">{m['text']}</div></div></div>;
        if(m['sender']===username)
            dClass = <div className="sentBox" id={index} key={index}><div className="sentMessage" key={index}><div className="sentMessageName">{m['sender']}</div><div className="sentMessageText">{m['text']}</div></div></div>;
       return dClass;
       
    }
    
    function receiveMessage(){
        React.useEffect(()=>{
            Socket.on('new message',(data)=>{
                if(username===null)    
                    return;
                if(data['sender'] === username)
                    return;
                addMessage(data['message'],data['dt'],data['sender']);
                
            });
            return ()=>{
                Socket.removeEventListener('new message');
            }
        });
    }
    
  
    
    firstConnect();
    receiveMessage();
   
    return(
        <div id ="messageBox">
            <h1 className="Chat">CHAT</h1>
            <div className ="messages">
                {messageFormat()}
            </div>
            <Send username={params['username']} addMessage={addMessage}/>
        </div>
        )
}