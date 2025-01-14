import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ScrollView } from 'react-native';

export default function StreaksScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      {/* Header Section */}
      <View style={styles.header}>
        <Text style={styles.headerText}>STREAKS</Text>
        <View style={styles.icons}>
          <Image source={require('../assets/images/fire.png')} style={styles.icon} />
          <Image source={require('../assets/icons/calendar.png')} style={styles.icon} />
        </View>
      </View>

      {/* Streak Counter Section */}
      <View style={styles.streakSection}>
        <Image source={require('../assets/images/streakfire.png')} style={styles.streakIcon} />
        <Text style={styles.streakText}>3 Day Streak!</Text>
        <Text style={styles.streakMessage}>Track your activities daily to build your streak</Text>
      </View>

      {/* Week Calendar Section */}
      <ScrollView horizontal style={styles.calendarSection}>
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day, index) => (
          <View key={index} style={styles.dayContainer}>
            <Text style={styles.dayText}>{day}</Text>
            <View style={[styles.dayCircle, index < 3 && styles.activeDay]} />
          </View>
        ))}
      </ScrollView>

      {/* Continue Button */}
      <TouchableOpacity style={styles.continueButton} onPress={() => navigation.navigate('Home')}>
        <Text style={styles.continueButtonText}>Continue</Text>
      </TouchableOpacity>

      {/* Bottom Navigation */}
      <View style={styles.navbar}>
        <TouchableOpacity style={styles.navButton} onPress={() => navigation.navigate('Home')}>
          <Image source={require('../assets/icons/home.png')} style={styles.navIcon} />
        </TouchableOpacity>
        <TouchableOpacity style={styles.navButton} onPress={() => navigation.navigate('Rewards')}>
          <Image source={require('../assets/icons/rewards.png')} style={styles.navIcon} />
        </TouchableOpacity>
        <TouchableOpacity style={styles.navButton} onPress={() => navigation.navigate('Voice Assistant')}>
          <Image source={require('../assets/icons/mic.png')} style={styles.navIcon} />
        </TouchableOpacity>
        <TouchableOpacity style={styles.navButton} onPress={() => navigation.navigate('Reminders')}>
          <Image source={require('../assets/icons/bell.png')} style={styles.navIcon} />
        </TouchableOpacity>
        <TouchableOpacity style={styles.navButton} onPress={() => navigation.navigate('Settings')}>
          <Image source={require('../assets/icons/settings.png')} style={styles.navIcon} />
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    paddingHorizontal: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 30,
  },
  headerText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
  },
  icons: {
    flexDirection: 'row',
  },
  icon: {
    width: 30,
    height: 30,
    marginLeft: 10,
  },
  streakSection: {
    alignItems: 'center',
    marginTop: 40,
  },
  streakIcon: {
    width: 50,
    height: 50,
  },
  streakText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
    marginVertical: 10,
  },
  streakMessage: {
    fontSize: 16,
    color: '#888',
  },
  calendarSection: {
    marginTop: 30,
    flexDirection: 'row',
  },
  dayContainer: {
    alignItems: 'center',
    marginHorizontal: 10,
  },
  dayText: {
    fontSize: 16,
    color: '#333',
  },
  dayCircle: {
    width: 25,
    height: 25,
    borderRadius: 12.5,
    marginTop: 5,
    backgroundColor: '#ddd',
  },
  activeDay: {
    backgroundColor: '#FF6F61',
  },
  continueButton: {
    backgroundColor: '#4CAF50',
    paddingVertical: 12,
    paddingHorizontal: 40,
    borderRadius: 30,
    marginTop: 30,
    alignSelf: 'center',
  },
  continueButtonText: {
    color: '#fff',
    fontSize: 16,
  },
  navbar: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 10,
    borderTopWidth: 1,
    borderTopColor: '#ddd',
    backgroundColor: '#f8f8f8',
  },
  navButton: {
    padding: 10,
  },
  navIcon: {
    width: 24,
    height: 24,
  },
});


