import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  Image,
  StyleSheet,
  Alert,
} from 'react-native';
import { launchImageLibrary } from 'react-native-image-picker';

export default function ProfilePictureScreen({ navigation }: any) {
  const [profileImage, setProfileImage] = useState<string | null>(null);

  // Function to handle image selection
  const selectImage = () => {
    launchImageLibrary(
      {
        mediaType: 'photo',
        maxWidth: 300,
        maxHeight: 300,
        quality: 0.8,
      },
      (response) => {
        if (response.didCancel) {
          Alert.alert('Canceled', 'No image selected');
        } else if (response.errorCode) {
          Alert.alert('Error', response.errorMessage || 'Something went wrong');
        } else if (response.assets && response.assets.length > 0) {
          const selectedImage = response.assets[0].uri || null;
          setProfileImage(selectedImage);
        }
      }
    );
  };

  return (
    <View style={styles.container}>
      <Text style={styles.stepText}>Step 1/1</Text>
      <Text style={styles.title}>Select Profile Picture</Text>
      <Text style={styles.subtitle}>
        You can select a photo from one of the options below or add your own
      </Text>

      {/* Profile Picture Circle */}
      <TouchableOpacity onPress={selectImage} style={styles.profileCircle}>
        {profileImage ? (
          <Image source={{ uri: profileImage }} style={styles.profileImage} />
        ) : (
          <Text style={styles.addIcon}>+</Text>
        )}
      </TouchableOpacity>

      {/* Default Images */}
      <View style={styles.defaultImagesContainer}>
        {[1, 2, 3, 4].map((item) => (
          <View key={item} style={styles.defaultImageBox}>
            <Text style={styles.placeholderText}>Img {item}</Text>
          </View>
        ))}
      </View>

      {/* Continue Button */}
      <TouchableOpacity
        style={styles.continueButton}
        onPress={() => navigation.navigate('UserDetails')}
      >
        <Text style={styles.continueButtonText}>Continue</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
    justifyContent: 'space-between',
  },
  stepText: {
    textAlign: 'center',
    fontSize: 14,
    color: '#aaa',
  },
  title: {
    textAlign: 'center',
    fontSize: 20,
    fontWeight: 'bold',
  },
  subtitle: {
    textAlign: 'center',
    fontSize: 14,
    color: '#777',
    marginVertical: 10,
  },
  profileCircle: {
    alignSelf: 'center',
    backgroundColor: '#f0f0f0',
    width: 100,
    height: 100,
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center',
  },
  addIcon: {
    fontSize: 30,
    color: '#999',
  },
  profileImage: {
    width: 100,
    height: 100,
    borderRadius: 50,
  },
  defaultImagesContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginVertical: 20,
  },
  defaultImageBox: {
    backgroundColor: '#f0f0f0',
    width: 70,
    height: 70,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 10,
  },
  placeholderText: {
    color: '#777',
  },
  continueButton: {
    backgroundColor: '#007bff',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  continueButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
