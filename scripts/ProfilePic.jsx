import * as React from 'react';

export function ProfilePic(params)
{
    var m = params['m'];
    return (<div className = "profileImgBox">
                <img className = "profileImg" src = {m['img']}></img>
            </div>
            )
}