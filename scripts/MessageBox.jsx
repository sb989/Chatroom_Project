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
                var message,text,sender,dt,msg_type;
                setMessages([]);
                for(i=0;i<size;i++)
                {
                    message = messages[i];
                    msg_type = message['msg_type']
                    text = message['m'];
                    sender = message['sender'];
                    dt = message['dt'];
                    addMessage(text,dt,sender,msg_type);
                }
                console.log(data['username']);
            });
        },[]);
    }
    
    function addMessage(text,dt,sender,msg_type)
    {
        var message ={'dt':dt,'sender':sender,'text':text,'msg_type':msg_type};
        setMessages(m=>m.concat(message));
       
    }
    
    function messageFormat(){
        var copy = [...messages];
        return copy.reverse().map((m,index)=>divClass(m,index));
    }
    
    function divClass(m,index)
    {
        var cBox = "receivedBox"
        var cMessage = "receivedMessage"
        var cName = "receivedMessageName"
        var cText = "receivedMessageText"
        var dClass;
        if(m['sender']===username)
        {
            cBox = "sentBox"
            cMessage = "sentMessage"
            cName = "sentMessageName"
            cText = "sentMessageText"
        }
        if(m['msg_type']==='text')
        {
            dClass = <div className={cBox} id={index} key={index}><div className={cMessage} key={index}> <div className={cName}>{m['sender']}</div><div className={cText}>{m['text']}</div></div></div>;
        }
        else if(m['msg_type']==='img')
        {
            dClass = <div className={cBox} id={index} key={index}><div className={cMessage} key={index}> <div className={cName}>{m['sender']}</div><div className={cText}><img src={m['text']}></img></div></div></div>;
        }
            
       return dClass;
       
    }
    
    function receiveMessage(){
        React.useEffect(()=>{
            Socket.on('new message',(data)=>{
                if(username===null)    
                    return;
                if(data['sender'] === username)
                    return;
                addMessage(data['message'],data['dt'],data['sender'],data['msg_type']);
                
            });
            return ()=>{
                Socket.removeEventListener('new message');
            }
        });
    }
    
    function receiveBotMessage()
    {
        React.useEffect(()=>{
            Socket.on('Bot',(data)=>{
                console.log(data);
                addMessage(data['message'],data['dt'],data['sender'],data['msg_type']);
            });
        
            return ()=>{
                Socket.removeEventListener('Bot');
            }
        });
    }
  
    
    firstConnect();
    receiveMessage();
   receiveBotMessage();
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