import {registerRoot, Composition, AbsoluteFill, useCurrentFrame, interpolate} from 'remotion';
import React from 'react';
const Title: React.FC = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{background:'#111',justifyContent:'center',alignItems:'center'}}>
    <h1 style={{color:'#f5d742',fontSize:90,opacity:interpolate(f,[0,20],[0,1])}}>Remotion OK</h1>
  </AbsoluteFill>;
};
registerRoot(() => <Composition id="Test" component={Title} durationInFrames={45} fps={30} width={1080} height={1920}/>);
