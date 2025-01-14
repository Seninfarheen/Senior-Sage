import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ScrollView } from 'react-native';

export default function SettingsScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      {/* Header Section */}
      <View style={styles.header}>
        <Image source={require('../assets/icons/owl.png')} style={styles.icon} />
        <Text style={styles.headerText}>Settings</Text>
        <Image source={require('../assets/icons/gears.png')} style={styles.icon} />
      </View>

      {/* General Section */}
      <ScrollView style={styles.settingsList}>
        <Text style={styles.sectionTitle}>General</Text>

        <TouchableOpacity style={styles.settingItem} onPress={() => navigation.navigate('Account')}>
          <Image source={require('../assets/icons/user.png')} style={styles.settingIcon} />
          <Text style={styles.settingText}>Account</Text>
          <Image source={require('../assets/icons/arrow.png')} style={styles.arrowIcon} />
        </TouchableOpacity>

        <TouchableOpacity style={styles.settingItem} onPress={() => navigation.navigate('Notifications')}>
          <Image source={require('../assets/icons/bell.png')} style={styles.settingIcon} />
          <Text style={styles.settingText}>Notifications</Text>
          <Image source={require('../assets/icons/arrow.png')} style={styles.arrowIcon} />
        </TouchableOpacity>

        <TouchableOpacity style={styles.settingItem} onPress={() => navigation.navigate('DeleteLogs')}>
          <Image source={require('../assets/icons/trash.png')} style={styles.settingIcon} />
          <Text style={styles.settingText}>Delete logs</Text>
          <Image source={require('../assets/icons/arrow.png')} style={styles.arrowIcon} />
        </TouchableOpacity>

        <TouchableOpacity style={styles.settingItem} onPress={() => navigation.navigate('LogOut')}>
          <Image source={require('../assets/icons/logout.png')} style={styles.settingIcon} />
          <Text style={styles.settingText}>Log Out</Text>
          <Image source={require('../assets/icons/arrow.png')} style={styles.arrowIcon} />
        </TouchableOpacity>

        <Text style={styles.sectionTitle}>Feedback</Text>

        <TouchableOpacity style={styles.settingItem} onPress={() => navigation.navigate('ReportBug')}>
          <Image source={require('../assets/icons/report.png')} style={styles.settingIcon} />
          <Text style={styles.settingText}>Report a bug</Text>
          <Image source={require('../assets/icons/arrow.png')} style={styles.arrowIcon} />
        </TouchableOpacity>

        <TouchableOpacity style={styles.settingItem} onPress={() => navigation.navigate('SendFeedback')}>
          <Image source={require('../assets/icons/bell.png')} style={styles.settingIcon} />
          <Text style={styles.settingText}>Send feedback</Text>
          <Image source={require('../assets/icons/arrow.png')} style={styles.arrowIcon} />
        </TouchableOpacity>
      </ScrollView>

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
  icon: {
    width: 50,
    height: 50,
  },
  settingsList: {
    marginTop: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 20,
    color: '#333',
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f9f9f9',
    padding: 15,
    borderRadius: 8,
    marginTop: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  settingIcon: {
    width: 24,
    height: 24,
    marginRight: 15,
  },
  settingText: {
    fontSize: 16,
    color: '#333',
    flex: 1,
  },
  arrowIcon: {
    width: 20,
    height: 20,
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
    width: 34,
    height: 34,
  },
});
