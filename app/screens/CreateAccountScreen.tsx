import React from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
} from 'react-native';
import CustomTextInput from '../components/CustomTextInput';

export default function CreateAccountScreen({ navigation }: any) {
  const [firstName, setFirstName] = React.useState('');
  const [lastName, setLastName]  = React.useState('');
  const [email, setEmail]        = React.useState('');
  const [password, setPassword]  = React.useState('');

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Senior Sage</Text>
      </View>

      <Text style={styles.pageTitle}>Create Account</Text>

      {/* Input Fields */}
      <CustomTextInput
        placeholder="First Name"
        value={firstName}
        onChangeText={setFirstName}
      />
      <CustomTextInput
        placeholder="Last Name"
        value={lastName}
        onChangeText={setLastName}
      />
      <CustomTextInput
        placeholder="Email"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
      />
      <CustomTextInput
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />

      {/* Create Account Button */}
      <TouchableOpacity 
        style={styles.createAccountButton}
        onPress={() => navigation.navigate('ProfilePicture')} //Navigate to Profile Picture
      >
        <Text style={styles.createAccountButtonText}>Create Account</Text>
      </TouchableOpacity>

      {/* Sign In Link */}
      <TouchableOpacity onPress={() => navigation.navigate('Login')}>
        <Text style={styles.signInLink}>
          Already have an account? <Text style={styles.signInText}>Sign in</Text>
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#fff',
  },
  header: {
    alignItems: 'center',
    marginBottom: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  pageTitle: {
    fontSize: 28,
    fontWeight: '600',
    marginBottom: 20,
  },
  input: {
    width: '100%',
    height: 50,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
    paddingHorizontal: 10,
    marginBottom: 15,
  },
  createAccountButton: {
    width: '100%',
    backgroundColor: '#4CAF50',
    paddingVertical: 15,
    borderRadius: 5,
    alignItems: 'center',
    marginBottom: 20,
  },
  createAccountButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  signInLink: {
    color: '#007BFF',
    fontSize: 14,
    marginTop: 20,
  },
  signInText: {
    textDecorationLine: 'underline',
    fontWeight: 'bold',
  },
});
