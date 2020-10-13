import * as React from 'react';
import { Socket } from './Socket';
// import { Content } from './Content';
import moment from 'moment';

export function Send(params)
{
    const [input,setInput]= React.useState('');
    var runAgain;
    var event;
    function newInp(curr)
    {
        setInput(curr.target.value);
    }
    
    function submit(e)
    {
        e.preventDefault();
        if(params['username']===null)
        {
            runAgain=true;
            event = e;
            return;      
        }
        var dt = moment().format('YYYY-MM-DD HH:mm:ss.SSSSSS');
        if(params['username']===null)
            return;
        Socket.emit('new message',{
            'message':input,
            'sender':params['username'],
            'datetime':dt
        });
        
        var form = document.getElementById("form");
        form.reset();
        console.log(params['username']);
        params['addMessage'](input,dt,params['username']);
        runAgain = false;
    }
    
    if(runAgain)
        submit(event);

    
    return (
        <div className = "send">
            <form id="form" className="form" onSubmit={submit}>
            
                <input className = "sendInput" type ='text'onInput={newInp}/>
                <button className = "sendButton">Send</button>
            </form>
        </div>
        
        )
    
}