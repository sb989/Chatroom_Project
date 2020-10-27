import * as React from 'react';
import moment from 'moment';
import Socket from './Socket';

export default function Send(params) {
  const [input, setInput] = React.useState('');
  let runAgain;
  let event;
  function newInp(curr) {
    setInput(curr.target.value);
  }

  function submit(e) {
    e.preventDefault();
    if (params.name === null) {
      runAgain = true;
      event = e;
      return;
    }
    const dt = moment().format('YYYY-MM-DD HH:mm:ss.SSSSSS');

    Socket.emit('new message', {
      msg: input,
      email: params.email,
      name: params.name,
      dt,
      msg_type: 'text',
      img: params.img,
      index: params.messages.length,
    });

    const form = document.getElementById('form');
    form.reset();
    params.addMessage(input, dt, params.name, 'text', params.email, params.img, '');
    runAgain = false;
  }

  if (runAgain) submit(event);

  return (
    <div className="send">
      <form id="form" className="form" onSubmit={submit}>

        <textarea className="sendInput" type="text" onInput={newInp} />
        <button className="sendButton" type="submit">Send</button>
      </form>
    </div>

  );
}
