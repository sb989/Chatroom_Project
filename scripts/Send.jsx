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
        if(params['name']===null)
        {
            runAgain=true;
            event = e;
            return;      
        }
        var dt = moment().format('YYYY-MM-DD HH:mm:ss.SSSSSS');
        if(params['name']===null)
            return;
        Socket.emit('new message',{
            'message':input,
            'email':params['email'],
            'name':params['name'],
            'datetime':dt,
            'msg_type':'text',
            'img':params['img'],
            'index':params['messages'].length
            });
        
        var form = document.getElementById("form");
        form.reset();
        console.log(params['name']);
        params['addMessage'](input,dt,params['name'],'text',params['email'],params['img'],'');
        runAgain = false;
    }
    
    if(runAgain)
        submit(event);

    
    return (
        <div className = "send">
            <form id="form" className="form" onSubmit={submit}>
            
                <textarea className = "sendInput" type ='text'onInput={newInp} ></textarea>
                <button className = "sendButton">Send</button>
            </form>
        </div>
        
        )
    
}