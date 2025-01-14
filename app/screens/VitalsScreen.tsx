import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ScrollView } from 'react-native';

export default function VitalsScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      {/* Header Section */}
      <View style={styles.header}>
        <Text style={styles.headerText}>VITALS</Text>
        <Image source={require('../assets/icons/owl.png')} style={styles.icon} />
      </View>

      {/* Description Section */}
      <View style={styles.descriptionSection}>
        <Text style={styles.descriptionText}>Keep tracking your vitals regularly!</Text>
        <TouchableOpacity style={styles.addButton} onPress={() => navigation.navigate('AddReading')}>
          <Text style={styles.addButtonText}>Add Reading</Text>
        </TouchableOpacity>
      </View>

      {/* BP Readings Image */}
      <View style={styles.bpChartContainer}>
        <Text style={styles.chartTitle}>BP Readings &gt;</Text>
        <Image
          source={require('../assets/images/graph.png')} // Replace with your BP readings image
          style={styles.bpChartImage}
        />
      </View>

      {/* XP Section */}
      <View style={styles.xpSection}>
        <Text style={styles.xpText}>Measure your vitals to get 20 XP!</Text>
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
  bpChartContainer: {
    marginTop: 40,
    alignItems: 'center',
  },
  chartTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  bpChartImage: {
    width: '100%',
    height: 220,
    resizeMode: 'contain',
    marginTop: 10,
  },
  xpSection: {
    marginTop: 40,
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
    marginTop: 160,
  },
  navButton: {
    padding: 10,
  },
  navIcon: {
    width: 34,
    height: 34,
  },
});

