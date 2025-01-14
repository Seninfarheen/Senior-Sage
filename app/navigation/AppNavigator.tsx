import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import LoginScreen from '../screens/LoginScreen';
import CreateAccountScreen from '../screens/CreateAccountScreen';
import ProfilePictureScreen from '../screens/ProfilePictureScreen';
import UserDetailsScreen from '../screens/UserDetailsScreen';
import VoiceSelectionScreen from '../screens/VoiceSelectionScreen';
import HomeScreen from '../screens/HomeScreen';
import VoiceAssistantScreen from '../screens/VoiceAssistantScreen';
import RemindersScreen from '../screens/RemindersScreen';
import SettingsScreen from '../screens/SettingsScreen';
import RewardsScreen from '../screens/RewardsScreen';
import VitalsScreen from '../screens/VitalsScreen';
import MedicationScreen from '../screens/MedicationScreen';
import ClaimRewardsScreen from '../screens/ClaimRewardsScreen';
import ExerciseScreen from '../screens/ExerciseScreen';
import AppointmentsScreen from '../screens/AppointmentsScreen';
import StreaksScreen from '../screens/StreaksScreen';
import TiersScreen from '../screens/TiersScreen';

const Stack = createStackNavigator();

export default function AppNavigator() {
  console.log('Initializing AppNavigator...'); // Debugging statement for navigator initialization

  return (
    <Stack.Navigator>
      <Stack.Screen
        name="Login"
        component={LoginScreen}
        options={{ title: 'Login' }}
        listeners={{
          focus: () => console.log('Navigated to Login Screen'), // Debug when entering Login
          blur: () => console.log('Left Login Screen'), // Debug when leaving Login
        }}
      />
      <Stack.Screen
        name="CreateAccount"
        component={CreateAccountScreen}
        options={{title: 'Create Account'}}
        listeners={{
          focus: () => console.log('Navigate to Create Account Screen'), //Debug when entering Create Account
          blur: () => console.log('Left Create Account Screen'), //Debug when leaving Create Account
        }}
      />
      <Stack.Screen
        name="ProfilePicture"
        component={ProfilePictureScreen}
        options={{title: 'Profile Picture'}}
        listeners={{
          focus: () => console.log('Navigate to Profile Picture Screen'), //Debug when entering Profile Picture Screen
          blur: () => console.log('Left the Profile Picture Screen'), // Debug when leaving Profile Picture Screen
        }}
      />
      <Stack.Screen
        name="UserDetails"
        component={UserDetailsScreen}
        options={{title: 'User Details'}}
        listeners={{
          focus: () => console.log('Navigate to User Details Screen'), //Debug when entering User Details Screen
          blur: () => console.log('Left the User Details Screen'), //Debug when leaving the User Details Screen
        }}
      />
      <Stack.Screen
        name="VoiceSelection"
        component={VoiceSelectionScreen}
        options={{title: 'Voice Selection'}}
        listeners={{
          focus: () => console.log('Navigate to Voice Selection Screen'), //Debug when entering Voice Selection Screen
          blur: () => console.log('Left the Voice Selection Screen'), //Debug when leaving the Voice Selection Screen
        }}
      />
      <Stack.Screen
        name="Home"
        component={HomeScreen}
        options={{title: 'Home'}}
        listeners={{
          focus: () => console.log('Navigate to Home Screen'), //Debug when entering Home Screen
          blur: () => console.log('Left the Home Screen '), //Debug when leaving the Home Screen
        }}
      />
      <Stack.Screen
        name="Voice Assistant"
        component={VoiceAssistantScreen}
        options={{title: 'Voice Assistant'}}
        listeners={{
          focus: () => console.log('Navigate to Voice Assistant Screen'), //Debug when entering Voice Assistant Screen
          blur: () => console.log('Left the Voice Assistant Screen'), //Debug when leaving Voice Assistant Screen
        }}
      />
      <Stack.Screen
        name="Reminders"
        component={RemindersScreen}
        options={{title: 'Reminders'}}
        listeners={{
          focus: () => console.log('Navigate to Reminders Screen'), //Debug when entering Reminders Screen
          blur: () => console.log('Left the Reminders Screen'), //Debug when leaving the Reminders Screen
        }}
      />
      <Stack.Screen
        name="Settings"
        component={SettingsScreen}
        options={{title: 'Settings'}}
        listeners={{
          focus: () => console.log('Navigate to Settings Screen'), //Debug when entering Settings Screen
          blur: () => console.log('Left the Settings Screen'), //Debug when leaving the Settings Screen
        }}
      />
      <Stack.Screen
        name="Rewards"
        component={RewardsScreen}
        options={{title: 'Rewards'}}
        listeners={{
          focus: () => console.log('Navigate to Rewards Screen'), //Debug when entering Rewards Screen
          blur: () => console.log('Left the Rewards Screen'), //Debug when leaving the Rewards Screen
        }}
      />
      <Stack.Screen
        name="Vitals"
        component={VitalsScreen}
        options={{title: 'Vitals'}}
        listeners={{
          focus: () => console.log('Navigate to Vitals Screen'), //Debug when entering Vitals Screen
          blur: () => console.log('Left the Vitals Screen'), //Debug when leaving the Vitals Screen
        }}
      />
      <Stack.Screen
        name="Medication"
        component={MedicationScreen}
        options={{title: 'Medication'}}
        listeners={{
          focus: () => console.log('Navigate to Medication Screen'), //Debug when entering Medication Screen
          blur: () => console.log('Left the Medication Screen'), //Debug when leaving the Medication Screen
        }}
      />
      <Stack.Screen
        name="Claim Rewards"
        component={ClaimRewardsScreen}
        options={{title: 'Claim Rewards'}}
        listeners={{
          focus: () => console.log('Navigate to Claim Rewards Screen'), //Debug when entering Claim Rewards Screen
          blur: () => console.log('Left the Claim Rewards Screen'), //Debug when leaving the Claim Rewards Screen
        }}
      />
      <Stack.Screen
        name="Exercise"
        component={ExerciseScreen}
        options={{title: 'Exercise'}}
        listeners={{
          focus: () => console.log('Navigate to the Exercise Screen'), //Debug when entering Exercise Screen
          blur: () => console.log('Left the Exercise Screen'), //Debug when leaving Exercise Screen
        }}
      />
      <Stack.Screen
        name="Appointments"
        component={AppointmentsScreen}
        options={{title: 'Appointments'}}
        listeners={{
          focus: () => console.log('Navigate to the Appointments Screen'), //Debug when entering Appointments Screen
          blur: () => console.log('Left the Appointments Screen'), //Debug when leaving Appointments Screen
        }}
      />
      <Stack.Screen
        name="Streaks"
        component={StreaksScreen}
        options={{title: 'Streaks'}}
        listeners={{
          focus: () => console.log('Navigate to the Streaks Screen'), //Debug when entering Streaks Screen
          blur: () => console.log('Left the Streaks Screen'), //Debug when leaving Streaks Screen
        }}
      />
      <Stack.Screen
        name="Tiers"
        component={TiersScreen}
        options={{title: 'Tiers'}}
        listeners={{
          focus: () => console.log('Navigate to the Tier Screen'), //Debug when entering Tiers Screen
          blur: () => console.log('Left the Tier Screen'), //Debug when leaving Tiers Screen
        }}
      />
    </Stack.Navigator>
  );
}

