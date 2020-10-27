import * as React from 'react';
import { v4 as uuidv4 } from 'uuid';
import Message from './Message';

export default function Messages(params) {
  const { messages } = params;
  const copy = [...messages];

  function mess() {
    return copy.reverse().map((m, index) => (
      <Message
        m={m}
        index={index}
        email={params.email}
        key={uuidv4()}
      />
    ));
  }

  return (
    <div className="messages">
      {mess()}
    </div>
  );
}
