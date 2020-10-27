import * as React from 'react';
import { Socket } from './Socket';
import ChatBox from './ChatBox';
import { GoogleButton } from './GoogleButton';

export default function Content() {
  const [messages, setMessages] = React.useState([]);
  const [name, setName] = React.useState(null);
  const [email, setEmail] = React.useState('');
  const [roomCount, setRoomCount] = React.useState(0);
  const [authenticated, setAuthenticated] = React.useState(false);
  const [loginMessage, setLoginMessage] = React.useState('');
  const [img, setImg] = React.useState('');

  function receiveCount() {
    React.useEffect(() => {
      Socket.on('room_count', (data) => {
        setRoomCount(data.count);
      });
      return () => { Socket.removeEventListener('room_count'); };
    });
  }

  function disconnect() {
    React.useEffect(() => {
      Socket.on('disconnect', () => {
        alert('You are not connected to the server. Messages might send when you reconnect.');
      });
      return () => { Socket.removeEventListener('disconnect'); };
    });
  }

  receiveCount();
  disconnect();

  if (authenticated) {
    return (
      <div>
        <div className="top">
          <h1 className="Chat">CHAT</h1>
          <h2 className="roomCount">
            Room Count:
            {roomCount}
          </h2>
        </div>
        <ChatBox
          name={name}
          setName={setName}
          messages={messages}
          img={img}
          setMessages={setMessages}
          email={email}
        />
      </div>

    );
  }

  if (!authenticated) {
    return (
      <div className="loginBox">
        <h1 className="loginHeader">Login</h1>
        {loginMessage}
        <br />
        <GoogleButton
          className="googleButton"
          setAuthenticated={setAuthenticated}
          setLoginMessage={setLoginMessage}
          setName={setName}
          setImg={setImg}
          setEmail={setEmail}
        />
      </div>
    );
  }
}
