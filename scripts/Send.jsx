import * as React from 'react';
import { Socket } from './Socket';
// import { Content } from './Content';
import moment from 'moment';

export function Send(params)
{
    const [input,setInput]= React.useState('');
    function newInp(curr)
    {
        setInput(curr.target.value);
    }
    
    function submit(e)
    {
        var dt = moment().format('YYYY-MM-DD HH:mm:ss.SSSSSS');
        Socket.emit('new message',{
            'message':input,
            'sender':params['username'],
            'datetime':dt
        });
        e.preventDefault();
        var form = document.getElementById("form");
        form.reset();
        console.log(params['username']);
        params['addMessage'](input,dt,params['username']);
    }
    
    return (
        <div>
            <form id="form" onSubmit={submit}>
            
                <input type ='text'onInput={newInp}/>
                <button>send</button>
            </form>
        </div>
        
        )
    
}