import React from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { useRef } from 'react';

const HeartShape = ({ color = '#ff4444' }) => {
  const meshRef = useRef(null);
  const scaleRef = useRef(1);
  const scalingDirection = useRef(1);

  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.z += 0.01;

      // Heartbeat animation
      scaleRef.current += 0.02 * scalingDirection.current;
      if (scaleRef.current >= 1.2 || scaleRef.current <= 1) {
        scalingDirection.current *= -1;
      }
      meshRef.current.scale.set(scaleRef.current, scaleRef.current, scaleRef.current);
    }
  });

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[1, 32, 32]} />
      <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.5} />
    </mesh>
  );
};

export const HeartBeat = ({ color = '#ff4444' }) => {
  return (
    <Canvas>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <HeartShape color={color} />
    </Canvas>
  );
};