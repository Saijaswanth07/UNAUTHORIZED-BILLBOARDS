import React from 'react';
import { View, Text, ScrollView, StyleSheet, Linking } from 'react-native';
import { Button } from 'react-native-paper';

const PrivacyPolicy = ({ onAccept }) => {
  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Privacy Policy & Data Usage</Text>
      
      <Text style={styles.sectionTitle}>Data Collection</Text>
      <Text style={styles.text}>
        We collect the following information to process and investigate billboard compliance reports:
      </Text>
      <Text style={styles.listItem}>• Photos/videos of potential violations</Text>
      <Text style={styles.listItem}>• Geolocation data</Text>
      <Text style={styles.listItem}>• Device information (make, model, OS version)</Text>
      <Text style={styles.listItem}>• Timestamp of report submission</Text>
      <Text style={styles.listItem}>• Optional contact information</Text>

      <Text style={styles.sectionTitle}>How We Use Your Data</Text>
      <Text style={styles.listItem}>• Investigate potential billboard violations</Text>
      <Text style={styles.listItem}>• Improve our detection algorithms</Text>
      <Text style={styles.listItem}>• Generate compliance reports for authorities</Text>
      <Text style={styles.listItem}>• Contact you for additional information if needed</Text>

      <Text style={styles.sectionTitle}>Data Protection</Text>
      <Text style={styles.text}>
        We implement industry-standard security measures to protect your data:
      </Text>
      <Text style={styles.listItem}>• End-to-end encryption for all data in transit</Text>
      <Text style={styles.listItem}>• Secure storage with access controls</Text>
      <Text style={styles.listItem}>• Regular security audits</Text>
      <Text style={styles.listItem}>• Data minimization principles</Text>

      <Text style={styles.sectionTitle}>AI & Privacy</Text>
      <Text style={styles.text}>
        Our AI systems are designed with privacy in mind:
      </Text>
      <Text style={styles.listItem}>• No facial recognition or personal identification</Text>
      <Text style={styles.listItem}>• Focused solely on billboard structures and content</Text>
      <Text style={styles.listItem}>• No persistent tracking of individuals</Text>

      <Text style={styles.sectionTitle}>Your Rights</Text>
      <Text style={styles.listItem}>• Request access to your data</Text>
      <Text style={styles.listItem}>• Request data deletion</Text>
      <Text style={styles.listItem}>• Withdraw consent</Text>
      <Text style={styles.listItem}>• File a complaint</Text>

      <Text style={styles.note}>
        By using this app, you agree to our full 
        <Text 
          style={styles.link}
          onPress={() => Linking.openURL('https://yourapp.com/terms')}
        >
          {' '}Terms of Service
        </Text> and 
        <Text 
          style={styles.link}
          onPress={() => Linking.openURL('https://yourapp.com/privacy')}
        >
          {' '}Privacy Policy
        </Text>.
      </Text>

      <Button 
        mode="contained" 
        onPress={onAccept}
        style={styles.button}
      >
        I Understand and Agree
      </Button>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
    color: '#333',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 15,
    marginBottom: 10,
    color: '#444',
  },
  text: {
    fontSize: 16,
    marginBottom: 10,
    lineHeight: 22,
    color: '#555',
  },
  listItem: {
    fontSize: 15,
    marginLeft: 15,
    marginBottom: 8,
    lineHeight: 22,
    color: '#555',
  },
  note: {
    fontSize: 14,
    marginTop: 20,
    marginBottom: 20,
    fontStyle: 'italic',
    color: '#666',
  },
  link: {
    color: '#1e88e5',
    textDecorationLine: 'underline',
  },
  button: {
    marginTop: 20,
    marginBottom: 40,
    paddingVertical: 8,
  },
});

export default PrivacyPolicy;
