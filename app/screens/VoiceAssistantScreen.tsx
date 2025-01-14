import React, { useState } from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';

export default function VoiceAssistantScreen({ navigation }: any) {
  const [isListening, setIsListening] = useState(false);

  const toggleListening = () => {
    setIsListening(!isListening);
  };

  return (
    <View style={styles.container}>
      {/* Header Section */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={styles.headerText}>Voice Assistant</Text>
        </TouchableOpacity>
      </View>

      {/* Owl Icon */}
      <View style={styles.owlContainer}>
        <Image source={require('../assets/icons/owl.png')} style={styles.owlIcon} />
      </View>

      {/* Sound Wave */}
      <View style={styles.waveContainer}>
        <Image 
          source={require('../assets/images/sound-wave.png')} 
          style={[styles.soundWave, isListening && styles.activeWave]} 
        />
      </View>

      {/* Microphone Button */}
      <TouchableOpacity style={styles.microphoneButton} onPress={toggleListening}>
        <Image source={require('../assets/icons/mic.png')} style={styles.microphoneIcon} />
      </TouchableOpacity>

      {/* Close Button */}
      <TouchableOpacity style={styles.closeButton} onPress={() => navigation.goBack()}>
        <Image source={require('../assets/icons/close.png')} style={styles.closeIcon} />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  header: {
    position: 'absolute',
    top: 40,
    left: 20,
    zIndex: 1,
  },
  headerText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
  },
  owlContainer: {
    alignItems: 'center',
    marginBottom: 30,
  },
  owlIcon: {
    width: 100,
    height: 100,
  },
  waveContainer: {
    marginTop: 20,
    alignItems: 'center',
  },
  soundWave: {
    width: 200,
    height: 100,
    resizeMode: 'contain',
    opacity: 0.5, // Initially not active
  },
  activeWave: {
    opacity: 1, // Active state when listening
  },
  microphoneButton: {
    marginTop: 40,
    width: 80,
    height: 80,
    backgroundColor: '#4CAF50',
    borderRadius: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  microphoneIcon: {
    width: 40,
    height: 40,
    tintColor: '#fff',
  },
  closeButton: {
    position: 'absolute',
    top: 40,
    right: 20,
    zIndex: 1,
  },
  closeIcon: {
    width: 30,
    height: 30,
  },
});


