import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ScrollView } from 'react-native';

export default function MedicationScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      {/* Header Section */}
      <View style={styles.header}>
        <Text style={styles.headerText}>MEDICATION</Text>
        <Image source={require('../assets/images/medication.png')} style={styles.icon} />
      </View>

      {/* Description Section */}
      <View style={styles.descriptionSection}>
        <Text style={styles.descriptionText}>You're doing great! Keep taking your medications</Text>
        <TouchableOpacity style={styles.addButton} onPress={() => navigation.navigate('AddMedication')}>
          <Text style={styles.addButtonText}>Add Medication</Text>
        </TouchableOpacity>
      </View>

      {/* Medication List */}
      <ScrollView style={styles.medicationList}>
        <View style={styles.medicationCard}>
          <Text style={styles.medicationName}>Norvasc</Text>
          <Text style={styles.medicationTime}>10 AM</Text>
          <Text style={styles.medicationDescription}>Take empty stomach</Text>
          <Text style={styles.medicationDose}>Dose: 80 mg</Text>
          <TouchableOpacity style={styles.checkbox}>
            <Image source={require('../assets/icons/ticked-checkbox.png')} style={styles.checkboxIcon} />
          </TouchableOpacity>
        </View>

        <View style={styles.medicationCard}>
          <Text style={styles.medicationName}>Prinivil</Text>
          <Text style={styles.medicationTime}>2 PM, 7 PM</Text>
          <Text style={styles.medicationDescription}>After breakfast, dinner</Text>
          <Text style={styles.medicationDose}>Dose: 40 mg</Text>
          <TouchableOpacity style={styles.checkbox}>
            <Image source={require('../assets/icons/checkbox.png')} style={styles.checkboxIcon} />
          </TouchableOpacity>
        </View>

        <View style={styles.medicationCard}>
          <Text style={styles.medicationName}>Cozaar</Text>
          <Text style={styles.medicationTime}>9 PM</Text>
          <Text style={styles.medicationDescription}>Before sleeping</Text>
          <Text style={styles.medicationDose}>Dose: 100 mg</Text>
          <TouchableOpacity style={styles.checkbox}>
            <Image source={require('../assets/icons/checkbox.png')} style={styles.checkboxIcon} />
          </TouchableOpacity>
        </View>
      </ScrollView>

      {/* XP Section */}
      <View style={styles.xpSection}>
        <Text style={styles.xpText}>Track all to get 15 XP!</Text>
      </View>

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
  descriptionSection: {
    marginTop: 20,
    alignItems: 'center',
  },
  descriptionText: {
    fontSize: 18,
    color: '#000',
  },
  addButton: {
    marginTop: 20,
    backgroundColor: '#4CAF50',
    paddingVertical: 12,
    paddingHorizontal: 40,
    borderRadius: 30,
  },
  addButtonText: {
    color: '#fff',
    fontSize: 16,
  },
  medicationList: {
    marginTop: 30,
  },
  medicationCard: {
    backgroundColor: '#f9f9f9',
    padding: 15,
    marginBottom: 15,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  medicationName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
  },
  medicationTime: {
    fontSize: 16,
    color: '#888',
  },
  medicationDescription: {
    fontSize: 14,
    color: '#555',
  },
  medicationDose: {
    fontSize: 14,
    color: '#333',
  },
  checkbox: {
    marginTop: 10,
    width: 30,
    height: 30,
    backgroundColor: '#ddd',
    borderRadius: 5,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxIcon: {
    width: 20,
    height: 20,
  },
  xpSection: {
    marginTop: 0,
    alignItems: 'center',

  },
  xpText: {
    fontSize: 16,
    color: '#888',
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
