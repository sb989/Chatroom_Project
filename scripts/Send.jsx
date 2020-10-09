import * as React from 'react';
import { Socket } from './Socket';
import { Content } from './Content';
import { username } from './Content';
import moment from 'moment';

export function Send(username)
{
    const [input,setInput]= React.useState('');
    
    function newInp(curr)
    {
        setInput(curr.target.value);
    }
    
    function submit(e)
    {
        Socket.emit('new message',{
            'message':input,
            'sender':username['username'],
            'datetime':moment().format('YYYY-MM-DD HH:mm:ss.SSSSSS')
        });
        e.preventDefault();
    }
    
    return (
        <div>
            <form onSubmit={submit}>
            
                <input type ='text'onInput={newInp}/>
                <button>send</button>
            </form>
        </div>
        
        )
    
}