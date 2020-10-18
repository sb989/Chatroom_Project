import * as React from 'react';
import {MessageContents} from './MessageContents';
import {ProfilePic} from './ProfilePic';
export function MessageBox(params)
{
    var m = params['m']
    var index = params['index']
    var cBox = params['cBox']
    var email = params['email']
    
    if(m["same_or_diff_sender"] === "same_sender")
    {
        return(<div className ={cBox} id={index} index={index}>
            <MessageContents
                m = {m}
                index = {index}
                cMessage = {params['cMessage']}
                cName = {params['cName']}
                cText = {params['cText']}
                name = ''
                text = {params['text']}
            
            />
            </div>)
    }
    
    else if(email === m['email'])
    {
        return (<div className ={cBox} id={index} index={index}>
                    <MessageContents
                        m = {m}
                        index = {index}
                        cMessage = {params['cMessage']}
                        cName = {params['cName']}
                        cText = {params['cText']}
                        name = {params['name']}
                        text = {params['text']}
                    />
                    <ProfilePic
                        m = {m}
                    />
                </div>
                )
    }
    
    else
    {
        return (<div className ={cBox} id={index} index={index}>
                    <ProfilePic
                        m = {m}
                    />
                    <MessageContents
                        m = {m}
                        index = {index}
                        cMessage = {params['cMessage']}
                        cName = {params['cName']}
                        cText = {params['cText']}
                        name = {params['name']}
                        text = {params['text']}
                    />
                </div>
                )
    }
}

    