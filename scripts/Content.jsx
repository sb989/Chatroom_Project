import * as React from 'react';
import { Socket } from './Socket';
import { Send } from './Send';
import {MessageBox} from './MessageBox'
export function Content() {
    const[messages,setMessages] = React.useState([]);
    const[username,setUsername]= React.useState(null);
    const[roomCount,setRoomCount]=React.useState(0);
    
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
    receiveCount();
    
    return (
    <div>
        <h2 className="roomCount">Room Count: {roomCount}</h2>
        <MessageBox username={username} setUsername={setUsername} messages={messages} setMessages={setMessages}/>
    </div>
    
    );
    
    
}
