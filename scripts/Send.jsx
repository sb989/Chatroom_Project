import * as React from 'react';
import { Socket } from './Socket';

export function Send()
{
    const [input,setInput]= React.useState('');
    
    function newInp(curr)
    {
        setInput(curr);
    }
    
    function submit()
    {
        Socket.emit('new message',{
            'message':input
        });
    }
    
    return (
        <div>
            <form onSubmit={submit}>
                <input onInput={newInp}/>
                <button>send</button>
            </form>
        </div>
        
        )
    
}