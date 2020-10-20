import * as React from 'react';
import { Socket } from './Socket';
import ReactDOM from 'react-dom';
import GoogleLogin from 'react-google-login';




export function GoogleButton(params) {
    
    function success(response) {
        let name = response["profileObj"]["name"];
        let email = response["profileObj"]["email"];
        let img;
        if("imageUrl" in response["profileObj"])
        {
            img = response["profileObj"]["imageUrl"];
        }
        else
        {
            img = "static/profile_pic.png";
        }
        console.log(name);
        console.log(email);
        console.log(response);
        Socket.emit('login', {
            'name': name,
            'email':email,
            'img':img
        });
        
        console.log('Sent the name ' + name + ' to server!');
        params["setAuthenticated"](true);
        params["setName"](name);
        params["setImg"](img);
        params["setEmail"](email);
    }
    
    function failure(response){
        console.log(response);
    }
    
    
    
    return <GoogleLogin
        clientId="30624731772-clsbuhec4ag6bukbqpsuf1qppc3g3n5r.apps.googleusercontent.com"
        buttonText="Login"
        onSuccess={success}
        onFailure={failure}
        cookiePolicy={'single_host_origin'}
        redirectUri
        />
    
}
