import React from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { useRef } from 'react';

const RotatingBoxMesh = ({ color = '#667eea', size = 1 }) => {
  const meshRef = useRef(null);

  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.x += 0.01;
      meshRef.current.rotation.y += 0.01;
    }
  });

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[size, size, size]} />
      <meshStandardMaterial color={color} wireframe />
    </mesh>
  );
};

export const RotatingBox = ({ color = '#667eea', size = 1 }) => {
  return (
    <Canvas>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <RotatingBoxMesh color={color} size={size} />
    </Canvas>
  );
};