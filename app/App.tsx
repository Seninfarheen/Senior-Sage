import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import AppNavigator from './navigation/AppNavigator'; // Import your navigation setup

export default function App() {
  console.log('Rendering App...'); // Debugging statement for App entry point

  return (
    <NavigationContainer
      onReady={() => console.log('NavigationContainer is ready.')} // Debugging navigation initialization
      onStateChange={(state) => console.log('Navigation state changed:', state)} // Debugging state changes
    >
      <AppNavigator />
    </NavigationContainer>
  );
}
