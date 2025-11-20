import React from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { useRef } from 'react';
import { Line } from '@react-three/drei';

const Molecule = ({ color = '#667eea' }) => {
  const groupRef = useRef(null);

  useFrame(() => {
    if (groupRef.current) {
      groupRef.current.rotation.x += 0.003;
      groupRef.current.rotation.y += 0.005;
    }
  });

  const atoms = [
    { position: [0, 0, 0], size: 0.4 },
    { position: [2, 0, 0], size: 0.3 },
    { position: [-2, 0, 0], size: 0.3 },
    { position: [0, 2, 0], size: 0.3 },
    { position: [0, -2, 0], size: 0.3 }
  ];

  return (
    <group ref={groupRef}>
      {atoms.map((atom, idx) => (
        <mesh key={idx} position={atom.position}>
          <sphereGeometry args={[atom.size, 32, 32]} />
          <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.3} />
        </mesh>
      ))}
    </group>
  );
};

export const MoleculeAnimation = ({ color = '#667eea' }) => {
  return (
    <Canvas>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <Molecule color={color} />
    </Canvas>
  );
};