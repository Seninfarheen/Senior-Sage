import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ScrollView, Alert } from 'react-native';

export default function ClaimRewardsScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      {/* Header Section */}
      <View style={styles.header}>
        <Text style={styles.headerText}>Let's Reward Your Hardwork!</Text>
        <Image source={require('../assets/images/gift.png')} style={styles.icon} />
      </View>

      {/* Reward Points Display */}
      <View style={styles.rewardPointsSection}>
        <Text style={styles.rewardPointsText}>Your reward points (XP)</Text>
        <Text style={styles.rewardPoints}>500</Text>
        <View style={styles.rewardInfo}>
          <Text style={styles.rewardDescription}>Discount coupon 500 Reward Points = $5</Text>
          <TouchableOpacity style={styles.redeemButton} onPress={() => Alert.alert('Redeemed!')}>
            <Text style={styles.redeemButtonText}>Redeem</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Reward Options */}
      <ScrollView style={styles.rewardOptions}>
        <TouchableOpacity style={styles.rewardItem} onPress={() => navigation.navigate('Supplements')}>
          <Image source={require('../assets/icons/supplements.png')} style={styles.rewardIcon} />
          <Text style={styles.rewardItemText}>Supplements</Text>
          <Image source={require('../assets/icons/arrow.png')} style={styles.arrowIcon} />
        </TouchableOpacity>

        <TouchableOpacity style={styles.rewardItem} onPress={() => navigation.navigate('Pharmacies')}>
          <Image source={require('../assets/icons/pharmacy.png')} style={styles.rewardIcon} />
          <Text style={styles.rewardItemText}>Pharmacies</Text>
          <Image source={require('../assets/icons/arrow.png')} style={styles.arrowIcon} />
        </TouchableOpacity>

        <TouchableOpacity style={styles.rewardItem} onPress={() => navigation.navigate('Wellness')}>
          <Image source={require('../assets/icons/wellness.png')} style={styles.rewardIcon} />
          <Text style={styles.rewardItemText}>Wellness</Text>
          <Image source={require('../assets/icons/arrow.png')} style={styles.arrowIcon} />
        </TouchableOpacity>

        <TouchableOpacity style={styles.rewardItem} onPress={() => navigation.navigate('AllRewards')}>
          <Image source={require('../assets/images/gift.png')} style={styles.rewardIcon} />
          <Text style={styles.rewardItemText}>All rewards</Text>
          <Image source={require('../assets/icons/arrow.png')} style={styles.arrowIcon} />
        </TouchableOpacity>

        <TouchableOpacity style={styles.rewardItem} onPress={() => navigation.navigate('WaysToEarn')}>
          <Image source={require('../assets/icons/piggybank.png')} style={styles.rewardIcon} />
          <Text style={styles.rewardItemText}>Ways to earn</Text>
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
  rewardPointsSection: {
    marginTop: 30,
    backgroundColor: '#f0f8ff',
    padding: 20,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  rewardPointsText: {
    fontSize: 16,
    color: '#888',
  },
  rewardPoints: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#000',
    marginVertical: 10,
  },
  rewardInfo: {
    marginTop: 10,
  },
  rewardDescription: {
    fontSize: 14,
    color: '#888',
  },
  redeemButton: {
    backgroundColor: '#4CAF50',
    paddingVertical: 12,
    paddingHorizontal: 40,
    borderRadius: 30,
    marginTop: 10,
  },
  redeemButtonText: {
    color: '#fff',
    fontSize: 16,
  },
  rewardOptions: {
    marginTop: 30,
  },
  rewardItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f9f9f9',
    padding: 15,
    marginBottom: 10,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  rewardIcon: {
    width: 24,
    height: 24,
    marginRight: 20,
  },
  rewardItemText: {
    fontSize: 18,
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


