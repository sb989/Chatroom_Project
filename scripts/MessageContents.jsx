import * as React from 'react';


export function MessageContents(params)
{
    var cMessage = params['cMessage'];
    var cName = params['cName'];
    var cText = params['cText'];
    var index = params['index'];
    var name = params['name'];
    var text = params['text'];
    var m = params['m'];
    if(m['msg_type']==='img')
    {
        text = <img className = "msgImg" src = {m['text']}></img>
    }
    else if(m['msg_type']==='link')
    {
        var hr = m['text']
        if(!hr.startsWith('http'))
            hr = 'https://'+m['text']
        text = <a href = {hr}>{m['text']}</a>;
    }
    
    return(
        <div className={cMessage} key={index}>
                            <div className={cName}>
                                {name}
                            </div>
                            <div className={cText}>
                                {text}
                            </div>
        </div>
        )
}