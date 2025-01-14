import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ProgressBarAndroid } from 'react-native';

export default function RewardsScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      {/* Header Section */}
      <View style={styles.header}>
        <TouchableOpacity style={styles.header} onPress={() => navigation.navigate('Tiers')}>
          <Image source={require('../assets/images/bronze-tier.png')} style={styles.coinIcon} />
          <View style={styles.headerTextContainer}>
            <Text style={styles.totalPoints}>Total points: 300/500 (Next tier)</Text>
            <Text style={styles.tier}>Bronze Tier</Text>
          </View>
          <Image source={require('../assets/icons/owl.png')} style={styles.icon} />
        </TouchableOpacity>
      </View>

      {/* Daily Goal Section */}
      <View style={styles.dailyGoal}>
        <Text style={styles.dailyGoalText}>Daily Goal</Text>
        <Text style={styles.dailyPoints}>15/50 points</Text>
        <View style={styles.progressBarContainer}>
          <View style={[styles.progressBar, { width: '30%' }]} />
        </View>
      </View>

      {/* Streak Section */}
      <View style={styles.streakContainer}>
        <TouchableOpacity style={styles.activityIcon} onPress={() => navigation.navigate('Streaks')}>
          <Image source={require('../assets/images/fire.png')} style={styles.streakIcon} />
          <Text style={styles.streakText}>You're on a 3-day streak!</Text>
        </TouchableOpacity>
      </View>

      {/* Activity Log Section */}
      <View style={styles.activityLog}>
        <TouchableOpacity style={styles.activityIcon} onPress={() => navigation.navigate('Vitals')}>
          <Image source={require('../assets/images/vitals.png')} style={styles.activityIconImage} />
          <Text style={styles.activityLabel}>Vitals</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.activityIcon} onPress={() => navigation.navigate('Medication')}>
          <Image source={require('../assets/images/medication.png')} style={styles.activityIconImage} />
          <Text style={styles.activityLabel}>Medication</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.activityIcon} onPress={() => navigation.navigate('Exercise')}>
          <Image source={require('../assets/images/exercise.png')} style={styles.activityIconImage} />
          <Text style={styles.activityLabel}>Exercise</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.activityIcon} onPress={() => navigation.navigate('Appointments')}>
          <Image source={require('../assets/images/appointments.png')} style={styles.activityIconImage} />
          <Text style={styles.activityLabel}>Appointments</Text>
        </TouchableOpacity>
      </View>

      {/* Claim Rewards Button */}
      <TouchableOpacity style={styles.claimButton} onPress={() => navigation.navigate('Claim Rewards')}>
        <Text style={styles.claimButtonText}>Claim your rewards!</Text>
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
  coinIcon: {
    width: 50,
    height: 50,
  },
  headerTextContainer: {
    flex: 1,
    marginLeft: 10,
  },
  totalPoints: {
    fontSize: 16,
    color: '#333',
  },
  tier: {
    fontSize: 14,
    color: '#888',
  },
  icon: {
    width: 50,
    height: 50,
  },
  dailyGoal: {
    marginTop: 40,
  },
  dailyGoalText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#000',
  },
  dailyPoints: {
    fontSize: 18,
    color: '#333',
  },
  progressBarContainer: {
    backgroundColor: '#ddd',
    height: 10,
    borderRadius: 5,
    marginTop: 10,
  },
  progressBar: {
    backgroundColor: '#4CAF50',
    height: '100%',
    borderRadius: 5,
  },
  streakContainer: {
    marginTop: 20,
    flexDirection: 'row',
    alignItems: 'center',
  },
  streakIcon: {
    width: 30,
    height: 30,
    marginRight: 10,
  },
  streakText: {
    fontSize: 16,
    color: '#333',
  },
  activityLog: {
    marginTop: 30,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  activityIcon: {
    alignItems: 'center',
  },
  activityIconImage: {
    width: 50,
    height: 50,
    marginBottom: 5,
  },
  activityLabel: {
    fontSize: 14,
    color: '#333',
  },
  claimButton: {
    backgroundColor: '#FF6F61',
    paddingVertical: 12,
    paddingHorizontal: 40,
    borderRadius: 30,
    marginTop: 30,
    alignSelf: 'center',
  },
  claimButtonText: {
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
    marginTop: 230,
  },
  navButton: {
    padding: 10,
  },
  navIcon: {
    width: 34,
    height: 34,
  },
});


