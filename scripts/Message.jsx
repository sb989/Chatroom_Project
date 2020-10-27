import * as React from 'react';
import { MessageBox } from './MessageBox';

export default function Message(params) {
  const { m } = params;
  const { index } = params;
  let cBox = 'receivedBox';
  let cMessage = 'receivedMessage';
  let cName = 'receivedMessageName';
  let cText = 'receivedMessageText';
  const { text } = m;
  const { name } = m;
  const { email } = params;

  if (m.email === email) {
    cBox = 'sentBox';
    cMessage = 'sentMessage';
    cName = 'sentMessageName';
    cText = 'sentMessageText';
  }
  return (
    <div
      key={index}
      className={m.same_or_diff_sender}
      index={index}
    >
      <MessageBox
        m={m}
        index={index}
        cBox={cBox}
        cMessage={cMessage}
        cName={cName}
        cText={cText}
        text={text}
        name={name}
        email={email}
        key={index}
      />
    </div>
  );
}
