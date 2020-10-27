import * as React from 'react';
import { Socket } from './Socket';
import { Send } from './Send';
import Messages from './Messages';

export default function ChatBox(params) {
  const { name } = params;
  const { messages } = params;
  const { setMessages } = params;
  const { email } = params;

  function createMessage(text, dt, s_name, msg_type, s_email, img, same_or_diff_sender) {
    if (same_or_diff_sender === '' && messages.length > 0 && messages[messages.length - 1].email === s_email) {
      same_or_diff_sender = 'same_sender';
    } else if (same_or_diff_sender === '') {
      same_or_diff_sender = 'diff_sender';
    }
    const message = {
      dt,
      name: s_name,
      text,
      msg_type,
      email: s_email,
      img,
      same_or_diff_sender,
    };
    return message;
  }

  function addMessage(text, dt, sName, msgType, sEmail, img, sameOrDiffSender) {
    const message = createMessage(text, dt, sName, msgType, sEmail, img, sameOrDiffSender);
    setMessages((m) => m.concat(message));
  }

  function firstConnect() {
    React.useEffect(() => {
      Socket.on('connected', (data) => {
        const mssgs = data.messages;
        const size = mssgs.length;
        let i;
        let message; let text; let senderName; let dt; let msgType;
        let senderEmail; let img; let sameOrDiffSender;
        setMessages([]);
        const mess = [];
        for (i = 0; i < size; i += 1) {
          message = mssgs[i];
          msgType = message.msg_type;
          text = message.msg;
          senderName = message.name;
          senderEmail = message.email;
          dt = message.dt;
          img = message.img;
          sameOrDiffSender = message.same_or_diff_sender;
          mess[i] = createMessage(
            text,
            dt,
            senderName,
            msgType,
            senderEmail,
            img,
            sameOrDiffSender,
          );
        }
        setMessages((m) => m.concat(mess));
      });
      const element = document.getElementById(0);
      if (element) element.scrollIntoView(false);
    }, []);
  }

  function receiveMessage() {
    React.useEffect(() => {
      Socket.on('new message', (data) => {
        if (name === null) return;

        if (data.email === email) {
          if (data.index !== -1) {
            const copy = [...messages];
            copy[data.index].msg_type = data.msg_type;
            setMessages(() => copy);
          }

          return;
        }
        addMessage(data.msg, data.dt, data.name, data.msg_type, data.email, data.img, '');
      });
      return () => {
        Socket.removeEventListener('new message');
      };
    });
  }

  function receiveBotMessage() {
    React.useEffect(() => {
      Socket.on('Bot', (data) => {
        addMessage(data.msg, data.dt, data.name, data.msg_type, data.email, data.img, '');
      });

      return () => {
        Socket.removeEventListener('Bot');
      };
    });
  }

  firstConnect();
  receiveMessage();
  receiveBotMessage();
  return (
    <div className="chatBox" id="chatBox">

      <Messages
        messages={params.messages}
        email={email}
      />

      <Send
        name={params.name}
        messages={params.messages}
        addMessage={addMessage}
        email={email}
        img={params.img}
      />
    </div>
  );
}
