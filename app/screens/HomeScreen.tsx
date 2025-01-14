import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';

export default function HomeScreen({ navigation }: any) {

  return (
    <View style={styles.container}>
      {/* Header Section */}
      <View style={styles.header}>
        <Text style={styles.greeting}>Welcome to Senior Sage!</Text>
        <Image source={require('../assets/icons/owl.png')} style={styles.icon} />
      </View>

      {/* Blood Pressure Data */}
      <View style={styles.bloodPressure}>
        <Text style={styles.bloodPressureText}>Blood Pressure data</Text>
        <Image source={require('../assets/images/graph.png')} style={styles.graph} />
      </View>

      {/* Text-based Summary */}
      <View style={styles.summary}>
        <Text style={styles.summaryText}>Over the past month, you've had a mix of readings. 
          There were several higher readings, where your systolic pressure went above 130, especially on days like the 1st, 5th, 11th, and 23rd.
          It's important to pay attention to these instances as they indicate stages of high blood pressure. 
        </Text>
      </View>

      {/* Upcoming Appointment */}
      <View style={styles.appointment}>
        <Text style={styles.appointmentTitle}>Upcoming Appointment</Text>
        <View style={styles.appointmentDetails}>
          <Image source={require('../assets/icons/doctor.png')} style={styles.doctorIcon} />
          <View style={styles.appointmentInfo}>
            <Text style={styles.doctorName}>Dr. Anjana Reddy</Text>
            <Text style={styles.specialty}>Cardiologist</Text>
            <Text style={styles.appointmentDate}>12 Nov - 6 PM</Text>
          </View>
        </View>
        <View style={styles.appointmentActions}>
          <TouchableOpacity style={styles.videoButton}>
            {/*<Image source={require('../assets/icons/video-icon.png')} style={styles.videoIcon} />*/}
            <Text style={styles.videoText}>Video</Text>
          </TouchableOpacity>
        </View>
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
  greeting: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
  },
  icon: {
    width: 50,
    height: 50,
  },
  bloodPressure: {
    marginTop: 20,
    alignItems: 'center',
  },
  bloodPressureText: {
    fontSize: 18,
    color: '#000',
    marginBottom: 5,
  },
  graph: {
    width: '100%',
    height: 180,
    resizeMode: 'contain',
  },
  summary: {
    marginTop: 20,
    padding: 10,
  },
  summaryText: {
    fontSize: 16,
    color: '#000',
  },
  appointment: {
    marginTop: 30,
    backgroundColor: '#f8f8f8',
    padding: 20,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  appointmentTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#000',
  },
  appointmentDetails: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  doctorIcon: {
    width: 60,
    height: 60,
    borderRadius: 20,
    marginRight: 10,
  },
  appointmentInfo: {
    flex: 1,
  },
  doctorName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
  },
  specialty: {
    fontSize: 14,
    color: '#888',
  },
  appointmentDate: {
    fontSize: 14,
    color: '#555',
  },
  appointmentActions: {
    marginTop: 20,
    alignItems: 'flex-end',
  },
  videoButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#4CAF50',
    padding: 10,
    borderRadius: 30,
    width: 100,
    justifyContent: 'center',
  },
  videoText: {
    marginLeft: 5,
    color: '#fff',
    fontSize: 14,
  },
  videoIcon: {
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
    padding: 5,
  },
  navIcon: {
    width: 34,
    height: 34,
  },
});

