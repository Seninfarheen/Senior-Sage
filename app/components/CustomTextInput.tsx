// components/CustomTextInput.tsx
import React from 'react';
import { TextInput, StyleSheet, TextInputProps } from 'react-native';

export default function CustomTextInput(props: TextInputProps) {
  return (
    <TextInput
      {...props}
      style={[styles.input, props.style]} // Combine global styles with additional custom styles
      placeholderTextColor="#999" // Default placeholder color
    />
  );
}

const styles = StyleSheet.create({
  input: {
    width: '100%',
    height: 50,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
    paddingHorizontal: 10,
    marginBottom: 15,
    color: '#000', // Ensure text is visible
    backgroundColor: '#fff', // Ensure background is distinct
  },
});
