require('dotenv').config();
const express = require('express');
const cors = require('cors');
const twilio = require('twilio'); // <-- New Twilio Import

const app = express();

// Middleware
app.use(cors());
app.use(express.json()); // Tells the server to expect and parse JSON payloads

// Initialize the Twilio Client
const twilioClient = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);

// Health Check Route
app.get('/', (req, res) => {
  res.send('Shield Backend is online.');
});

// Phase 3: The Complete SOS Catching & Alerting Route
app.post('/api/v1/v-2/sos/trigger', async (req, res) => {
  const { latitude, longitude, timestamp } = req.body;

  // Failsafe: Ensure the payload actually contains coordinates
  if (!latitude || !longitude) {
    console.log('❌ Invalid SOS payload received.');
    return res.status(400).json({ error: 'Missing GPS coordinates.' });
  }

  console.log('\n🚨 URGENT: SOS PROTOCOL INITIATED 🚨');
  console.log(`📍 Location Lock: ${latitude}, ${longitude}`);
  console.log(`⏰ Timestamp: ${timestamp}`);
  
  // 1. Generate a universally clickable Google Maps link
  const mapsLink = `https://maps.google.com/?q=${latitude},${longitude}`;
  
  // 2. Format the emergency message
  const emergencyMessage = `🚨 SHIELD EMERGENCY: Arya has triggered an SOS protocol. Immediate assistance required. Live Location: ${mapsLink}`;

  try {
    // 3. Fire the SMS via Twilio
    console.log('📡 Pinging cellular towers for SMS broadcast...');
    
    /* // UNCOMMENT THIS BLOCK ONCE YOU HAVE YOUR TWILIO KEYS IN THE .ENV FILE
    const message = await twilioClient.messages.create({
      body: emergencyMessage,
      from: process.env.TWILIO_PHONE_NUMBER,
      to: process.env.EMERGENCY_CONTACT_NUMBER
    });
    console.log(`✅ SMS successfully delivered! Message SID: ${message.sid}`);
    */
    
    // Mock success log for local testing
    console.log(`✅ [MOCK] SMS Sent to ${process.env.EMERGENCY_CONTACT_NUMBER}: ${emergencyMessage}`);

    // Send a success response back to the Flutter app
    return res.status(200).json({ 
      message: 'SOS payload secured. Emergency contacts notified.',
      success: true
    });

  } catch (error) {
    console.error('❌ Twilio API Error:', error.message);
    return res.status(500).json({ error: 'Failed to dispatch SMS alerts.' });
  }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🛡️ Shield Backend actively listening on port ${PORT}`);
});