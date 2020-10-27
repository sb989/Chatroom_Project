import * as React from 'react';
import MessageContents from './MessageContents';
import ProfilePic from './ProfilePic';

export default function MessageBox(params) {
  const { m } = params;
  const { index } = params;
  const { cBox } = params;
  const { email } = params;

  if (m.sameOrDiffSender === 'same_sender') {
    return (
      <div className={cBox} id={index} index={index}>
        <MessageContents
          m={m}
          index={index}
          cMessage={params.cMessage}
          cName={params.cName}
          cText={params.cText}
          name=""
          text={params.text}
        />
      </div>
    );
  }

  if (email === m.email) {
    return (
      <div className={cBox} id={index} index={index}>
        <MessageContents
          m={m}
          index={index}
          cMessage={params.cMessage}
          cName={params.cName}
          cText={params.cText}
          name={params.name}
          text={params.text}
        />
        <ProfilePic
          m={m}
        />
      </div>
    );
  }

  return (
    <div className={cBox} id={index} index={index}>
      <ProfilePic
        m={m}
      />
      <MessageContents
        m={m}
        index={index}
        cMessage={params.cMessage}
        cName={params.cName}
        cText={params.cText}
        name={params.name}
        text={params.text}
      />
    </div>
  );
}
