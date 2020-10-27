import * as React from 'react';

export default function ProfilePic(params) {
  const { m } = params;
  return (
    <div className="profileImgBox">
      <img className="profileImg" src={m.img} alt="img" />
    </div>
  );
}
