import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ScrollView } from 'react-native';


export default function RemindersScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      {/* Header Section */}
      <View style={styles.header}>
        <Image source={require('../assets/icons/owl.png')} style={styles.icon} />
        <Text style={styles.headerText}>Reminders</Text>
        <TouchableOpacity style={styles.notificationButton}>
          <Image source={require('../assets/icons/notification.png')} style={styles.notificationIcon} />
        </TouchableOpacity>
      </View>

      {/* Date Navigation */}
      <View style={styles.dateNavigation}>
        <Text style={styles.dateText}>4 Sat</Text>
        <Text style={[styles.dateText, styles.activeDate]}>5 Sun</Text>
        <Text style={styles.dateText}>6 Mon</Text>
        <Text style={styles.dateText}>7 Tues</Text>
      </View>

      {/* Reminder List */}
      <ScrollView style={styles.reminderList}>
        <View style={styles.reminderCard}>
          <Image source={require('../assets/icons/capsule.png')} style={styles.cardIcon} />
          <View style={styles.cardContent}>
            <Text style={styles.reminderTitle}>Paracetamol</Text>
            <Text style={styles.reminderDescription}>After breakfast, dinner</Text>
            <Text style={styles.reminderTime}>8:00 PM</Text>
          </View>
        </View>

        <View style={styles.reminderCard}>
          <Image source={require('../assets/icons/water-glass.png')} style={styles.cardIcon} />
          <View style={styles.cardContent}>
            <Text style={styles.reminderTitle}>Drink Water</Text>
            <Text style={styles.reminderDescription}>Drink 8 glasses per day</Text>
            <Text style={styles.reminderTime}>8:30 PM</Text>
          </View>
        </View>

        <View style={styles.reminderCard}>
          <Image source={require('../assets/icons/walking.png')} style={styles.cardIcon} />
          <View style={styles.cardContent}>
            <Text style={styles.reminderTitle}>Go for a walk</Text>
            <Text style={styles.reminderDescription}>Walk 30 mins, twice a day</Text>
            <Text style={styles.reminderTime}>9:00 PM</Text>
          </View>
        </View>
      </ScrollView>

      {/* Add New Reminder Button */}
      <TouchableOpacity style={styles.addButton} onPress={() => navigation.navigate('AddReminder')}>
        <Text style={styles.addButtonText}>+</Text>
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
  icon: {
    width: 50,
    height: 50,
  },
  notificationButton: {
    padding: 10,
  },
  notificationIcon: {
    width: 50,
    height: 50,
  },
  dateNavigation: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginVertical: 20,
  },
  dateText: {
    fontSize: 18,
    color: '#888',
    marginHorizontal: 10,
  },
  activeDate: {
    color: '#FF6F61', // Active date color
    fontWeight: 'bold',
  },
  reminderList: {
    marginBottom: 80, // Add space for the bottom button
  },
  reminderCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f0f8ff',
    marginBottom: 15,
    padding: 15,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  cardIcon: {
    width: 40,
    height: 40,
    marginRight: 20,
  },
  cardContent: {
    flex: 1,
  },
  reminderTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
  },
  reminderDescription: {
    fontSize: 14,
    color: '#888',
  },
  reminderTime: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  addButton: {
    position: 'absolute',
    bottom: 100,
    right: 20,
    backgroundColor: '#4CAF50',
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
  },
  addButtonText: {
    fontSize: 30,
    color: '#fff',
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
