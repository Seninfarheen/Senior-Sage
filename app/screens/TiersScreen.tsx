import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, ScrollView } from 'react-native';

export default function TiersScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      {/* Header Section */}
      <View style={styles.header}>
        <Text style={styles.headerText}>TIERS</Text>
        <View style={styles.icons}>
          <Image source={require('../assets/images/castle.png')} style={styles.icon} />
        </View>
      </View>

      {/* Tier Display Section */}
      <ScrollView style={styles.tiersList}>
        <View style={styles.tierContainer}>
          <Image source={require('../assets/images/castle.png')} style={styles.icon} />
          <Text style={styles.tierLabel}>Diamond</Text>
          <Text style={styles.tierPoints}>20000 points</Text>
          <Image source={require('../assets/images/diamond-tier.png')} style={styles.tierBadge} />
        </View>

        <View style={styles.tierContainer}>
          <Image source={require('../assets/images/ladder.png')} style={styles.ladderIcon} />
          <Text style={styles.tierLabel}>Emerald</Text>
          <Text style={styles.tierPoints}>10000 points</Text>
          <Image source={require('../assets/images/emerald-tier.png')} style={styles.tierBadge} />
        </View>

        <View style={styles.tierContainer}>
          <Image source={require('../assets/images/ladder.png')} style={styles.ladderIcon} />
          <Text style={styles.tierLabel}>Platinum</Text>
          <Text style={styles.tierPoints}>5000 points</Text>
          <Image source={require('../assets/images/platinum-tier.png')} style={styles.tierBadge} />
        </View>

        <View style={styles.tierContainer}>
          <Image source={require('../assets/images/ladder.png')} style={styles.ladderIcon} />
          <Text style={styles.tierLabel}>Gold</Text>
          <Text style={styles.tierPoints}>2000 points</Text>
          <Image source={require('../assets/images/gold-tier.png')} style={styles.tierBadge} />
        </View>

        <View style={styles.tierContainer}>
          <Image source={require('../assets/images/ladder.png')} style={styles.keyIcon} />
          <Text style={styles.tierLabel}>Silver</Text>
          <Text style={styles.tierPoints}>500 points</Text>
          <Image source={require('../assets/images/silver-tier.png')} style={styles.tierBadge} />
        </View>

        <View style={styles.tierContainer}>
          <Image source={require('../assets/images/ladder.png')} style={styles.ladderIcon} />
          <Text style={styles.tierLabel}>Bronze</Text>
          <Text style={styles.tierPoints}>Start</Text>
          <Image source={require('../assets/images/bronze-tier.png')} style={styles.tierBadge} />
        </View>
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
  icons: {
    flexDirection: 'row',
  },
  icon: {
    width: 30,
    height: 30,
    marginLeft: 10,
  },
  tiersList: {
    marginTop: 30,
  },
  tierContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
    paddingBottom: 10,
  },
  ladderIcon: {
    width: 30,
    height: 30,
    marginRight: 20,
  },
  tierLabel: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
    flex: 1,
  },
  tierPoints: {
    fontSize: 16,
    color: '#888',
  },
  tierBadge: {
    width: 40,
    height: 40,
  },
  keyIcon: {
    width: 30,
    height: 30,
    marginRight: 20,
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


