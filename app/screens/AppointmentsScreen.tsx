import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ScrollView } from 'react-native';

export default function AppointmentsScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      {/* Header Section */}
      <View style={styles.header}>
        <Text style={styles.headerText}>APPOINTMENTS</Text>
        <Image source={require('../assets/images/appointments.png')} style={styles.icon} />
      </View>

      {/* Description Section */}
      <View style={styles.descriptionSection}>
        <Text style={styles.descriptionText}>Don't forget your appointment today!</Text>
        <TouchableOpacity style={styles.addButton} onPress={() => navigation.navigate('AddAppointment')}>
          <Text style={styles.addButtonText}>Add Appointment</Text>
        </TouchableOpacity>
      </View>

      {/* Appointment List */}
      <ScrollView style={styles.appointmentList}>
        <View style={styles.appointmentCard}>
          <Image source={require('../assets/images/male-doc.png')} style={styles.appointmentIcon} />
          <View style={styles.appointmentDetails}>
            <Text style={styles.appointmentTitle}>Dr. Roger Lim</Text>
            <Text style={styles.appointmentType}>Cardiologist</Text>
            <Text style={styles.appointmentDate}>8 Dec - 2 PM</Text>
          </View>
        </View>

        <View style={styles.appointmentCard}>
          <Image source={require('../assets/images/female-doc.png')} style={styles.appointmentIcon} />
          <View style={styles.appointmentDetails}>
            <Text style={styles.appointmentTitle}>Dr. Annie Yu</Text>
            <Text style={styles.appointmentType}>Orthopedic</Text>
            <Text style={styles.appointmentDate}>4 Dec - 3 PM</Text>
          </View>
        </View>
      </ScrollView>

      {/* XP Section */}
      <View style={styles.xpSection}>
        <Text style={styles.xpText}>Mark your appointments to get 30 XP!</Text>
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
  appointmentList: {
    marginTop: 30,
  },
  appointmentCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f9f9f9',
    padding: 15,
    marginBottom: 15,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  appointmentIcon: {
    width: 50,
    height: 50,
    marginRight: 20,
  },
  appointmentDetails: {
    flex: 1,
  },
  appointmentTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
  },
  appointmentType: {
    fontSize: 14,
    color: '#888',
  },
  appointmentDate: {
    fontSize: 16,
    color: '#333',
  },
  xpSection: {
    marginTop: 40,
    alignItems: 'center',
  },
  xpText: {
    fontSize: 16,
    color: '#888',
    marginBottom: 10,
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


