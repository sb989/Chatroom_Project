import * as React from 'react';
import { Socket } from './Socket';
import { Send } from './Send';
import {Messages} from './Messages';
export function ChatBox(params)
{
    var name = params['name'];
    var messages = params['messages'];
    var setMessages = params['setMessages'];
    var email = params['email'];
    
    function firstConnect()
    {
        React.useEffect(()=>
        {
            Socket.on('connected',(data)=>
            {
                console.log("connected");
                var messages = data['messages'];
                var size = messages.length;
                var i;
                var message,text,sender_name,dt,msg_type;
                var sender_email,img,same_or_diff_sender;
                setMessages([]);
                var mess = [];
                for(i=0;i<size;i++)
                {
                    message = messages[i];
                    msg_type = message['msg_type']
                    text = message['msg'];
                    sender_name = message['name'];
                    sender_email = message['email'];
                    dt = message['dt'];
                    img = message['img'];
                    same_or_diff_sender = message["same_or_diff_sender"];
                    mess[i] = createMessage(text,dt,sender_name,msg_type,sender_email,img,same_or_diff_sender);
                }
                setMessages(m=>m.concat(mess));
            });
            var element = document.getElementById(0);
            if(element)
                element.scrollIntoView(false);
            
            
        },[]);
    }
    
    function createMessage(text,dt,s_name,msg_type,s_email,img,same_or_diff_sender)
    {
        if(same_or_diff_sender === '' && messages.length > 0 && messages[messages.length-1]['email'] === s_email)
        {
            same_or_diff_sender = "same_sender";
        }
        else if (same_or_diff_sender === '')
        {
            same_or_diff_sender = "diff_sender";
        }
        var message ={'dt':dt,'name':s_name,
            'text':text,'msg_type':msg_type,
            'email':s_email,'img':img,
            "same_or_diff_sender":same_or_diff_sender};
        return message
    }
    function addMessage(text,dt,s_name,msg_type,s_email,img,same_or_diff_sender)
    {
        var message = createMessage(text,dt,s_name,msg_type,s_email,img,same_or_diff_sender);
        setMessages(m=>m.concat(message));
    }
    
   
    
    function receiveMessage()
    {
        React.useEffect(()=>
        {
            Socket.on('new message',(data)=>
            {
                if(name===null)    
                    return;
                    
                if(data['email'] === email)
                {
                    if(data['index'] !=-1)
                    {
                        var copy = [...messages]
                        copy[data['index']]['msg_type'] = data['msg_type'];
                        setMessages(m=>copy); 
                    }
                        
                    return;
                }
                addMessage(data['msg'],data['dt'],data['name'],data['msg_type'],data['email'],data['img'],'');
                
            });
            return ()=>
            {
                Socket.removeEventListener('new message');
            }
        });
    }
    
    function receiveBotMessage()
    {
        React.useEffect(()=>
        {
            Socket.on('Bot',(data)=>
            {
                addMessage(data['msg'],data['dt'],data['name'],data['msg_type'],data['email'],data['img'],'');
            });
        
            return ()=>
            {
                Socket.removeEventListener('Bot');
            }
        });
    }
  
    
    firstConnect();
    receiveMessage();
   receiveBotMessage();
    return(
        <div className = "chatBox" id ="chatBox">
           
            <Messages
                messages = {params['messages']}
                email = {email}
            />
            
            <Send name={params['name']} 
            messages={params['messages']}
            addMessage={addMessage}
            email={email}
            img = {params['img']}    
            />
        </div>
        )
}