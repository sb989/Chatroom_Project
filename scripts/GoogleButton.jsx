import * as React from 'react';
import GoogleLogin from 'react-google-login';
import Socket from './Socket';

export default function GoogleButton(params) {
  function success(response) {
    const { name } = response.profileObj;
    const { email } = response.profileObj;
    let img;
    if ('imageUrl' in response.profileObj) {
      img = response.profileObj.imageUrl;
    } else {
      img = 'static/profile_pic.png';
    }

    Socket.emit('login', {
      name,
      email,
      img,
    });

    params.setAuthenticated(true);
    params.setName(name);
    params.setImg(img);
    params.setEmail(email);
  }

  function failure() {
  }

  return (
    <GoogleLogin
      clientId="30624731772-clsbuhec4ag6bukbqpsuf1qppc3g3n5r.apps.googleusercontent.com"
      buttonText="Login"
      onSuccess={success}
      onFailure={failure}
      cookiePolicy="single_host_origin"
      redirectUri
    />
  );
}
