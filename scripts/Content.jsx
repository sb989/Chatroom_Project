import * as React from 'react';
import { Socket } from './Socket';
import { Send } from './Send';
import {MessageBox} from './MessageBox';
import {GoogleButton} from './GoogleButton';
export function Content() {
    
    const[messages,setMessages] = React.useState([]);
    const[name,setName] = React.useState(null);
    const[email,setEmail] = React.useState('');
    const[roomCount,setRoomCount] = React.useState(0);
    const[authenticated,setAuthenticated] = React.useState(false);
    const[loginMessage,setLoginMessage] = React.useState('');
    const[pic,setPic] = React.useState('');
    var element = document.getElementById(0);
    if(element)
        element.scrollIntoView(false);
        
    function receiveCount()
    {
        React.useEffect(()=>{
            Socket.on('room_count',(data)=>{
                setRoomCount(data['count']);
            })
            return ()=>{Socket.removeEventListener('room_count');}
        });
    }
    
    function disconnect()
    {
        
        React.useEffect(()=>{
            Socket.on('disconnect',()=>{
                alert("You are not connected to the server. Messages might send when you reconnect.");    
            })
            return ()=>{Socket.removeEventListener('disconnect');}
        });
    }
    
    
    
    receiveCount();
    disconnect();
    
    if(authenticated)
    {
        return(
        <div>
            <h2 className="roomCount">Room Count: {roomCount}</h2>
            <MessageBox 
            name = {name} setName = {setName} 
            messages = {messages} pic = {pic}
            setMessages = {setMessages}
            email = {email}
            />
        </div>
        
        );
    }
        
    else
    {
        return(
        <div>
            <h1>Login</h1>
            {loginMessage}<br/>
            <GoogleButton 
            setAuthenticated = {setAuthenticated} 
            setLoginMessage = {setLoginMessage}
            setName = {setName}
            setPic = {setPic}
            setEmail = {setEmail}
            />
        </div>
            )
    }
    
}
