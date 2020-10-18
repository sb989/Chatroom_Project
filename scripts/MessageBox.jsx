import * as React from 'react';
import { Socket } from './Socket';
import { Send } from './Send';

export function MessageBox(params)
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
                console.log(data);
                var messages = data['messages'];
                var size = messages.length;
                var i;
                var message,text,sender,dt,msg_type;
                var sender_email,img,same_or_diff_sender;
                setMessages([]);
                for(i=0;i<size;i++)
                {
                    message = messages[i];
                    msg_type = message['msg_type']
                    text = message['msg'];
                    sender = message['name'];
                    sender_email = message['email'];
                    dt = message['dt'];
                    img = message['img'];
                    same_or_diff_sender = message["same_or_diff_sender"];
                    addMessage(text,dt,sender,msg_type,sender_email,img,same_or_diff_sender);
                }
            });
            var element = document.getElementById(0);
            if(element)
                element.scrollIntoView(false);
            
            
        },[]);
    }
    
    function addMessage(text,dt,sender,msg_type,email,img,same_or_diff_sender)
    {
        
        if(same_or_diff_sender === '' && messages.length > 0 && messages[messages.length-1]['email'] === email)
        {
            same_or_diff_sender = "same_sender";
        }
        else if (same_or_diff_sender === '')
        {
            same_or_diff_sender = "diff_sender";
        }
        var message ={'dt':dt,'sender':sender,
            'text':text,'msg_type':msg_type,
            'email':email,'img':img,
            "same_or_diff_sender":same_or_diff_sender};
        setMessages(m=>m.concat(message));
    }
    
    function messageFormat()
    {
        var copy = [...messages];
        return copy.reverse().map((m,index)=>divClass(m,index));
    }
    
    function divClass(m,index)
    {
        var dClass;
        var cBox = "receivedBox";
        var cMessage = "receivedMessage";
        var cName = "receivedMessageName";
        var cText = "receivedMessageText";
        var contents = m['text'];
        var sender = m['sender'];
        var img = <div className = "profileImgBox">
                    <img className = "profileImg" src = {m['img']}></img>
                </div>;
        if(m['email']===email)
        {
            cBox = "sentBox"
            cMessage = "sentMessage"
            cName = "sentMessageName"
            cText = "sentMessageText"
            // img = '';
        }
        if(m['msg_type']==='img')
        {
            contents = <img className = "msgImg" src = {m['text']}></img>
        }
        else if(m['msg_type']==='link')
        {
            var hr = m['text']
            if(!hr.startsWith('http'))
                hr = 'https://'+m['text']
            contents = <a href = {hr}>{m['text']}</a>;
        }
        if(m['same_or_diff_sender'] === 'same_sender')
        {
            sender = '';
            img = '';
        }
        
        var htmlMessage = <div className={cMessage} key={index}>
                            <div className={cName}>
                                {sender}
                            </div>
                            <div className={cText}>
                                {contents}
                            </div>
                        </div>
        
        var htmlBox = <div className={cBox} id={index} key={index}>
                        {img}
                        {htmlMessage}
                    </div>
                    
        if(m['email']===email)
        {
            htmlBox = <div className={cBox} id={index} key={index}>
                        {htmlMessage}
                        {img}
                    </div>
        }
        
        dClass = <div key={index} className={m["same_or_diff_sender"]}>
            {htmlBox}
        </div>;
        
        
            
       return dClass;
       
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
        <div id ="messageBox">
            <div className ="messages">
                {messageFormat()}
            </div>
            <Send name={params['name']} 
            messages={params['messages']}
            addMessage={addMessage}
            email={params['email']}
            img = {params['img']}    
            />
        </div>
        )
}