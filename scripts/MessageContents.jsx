import * as React from 'react';

export default function MessageContents(params) {
  const { cMessage } = params;
  const { cName } = params;
  const { cText } = params;
  const { index } = params;
  const { name } = params;
  let { text } = params;
  const { m } = params;
  if (m.msgType === 'img') {
    text = <img className="msgImg" src={m.text} alt="img" />;
  } else if (m.msgType === 'link') {
    let hr = m.text;
    if (!hr.startsWith('http')) hr = `https://${m.text}`;
    text = <a href={hr}>{m.text}</a>;
  }

  return (
    <div className={cMessage} key={index}>
      <div className={cName}>
        {name}
      </div>
      <div className={cText}>
        {text}
      </div>
    </div>
  );
}
