import mongoose from 'mongoose';

const organDetailsSchema = new mongoose.Schema({
  kidney: { type: Boolean, default: false },
  liver: { type: Boolean, default: false },
  lung: { type: Boolean, default: false },
  pancreas: { type: Boolean, default: false },
  intestine: { type: Boolean, default: false },
  boneMarrow: { type: Boolean, default: false },
  blood: { type: Boolean, default: false },
  skin: { type: Boolean, default: false },
  amnioticMembrane: { type: Boolean, default: false },
}, { _id: false });

const donorSchema = new mongoose.Schema({
  // Basic Identification
  firstName: { type: String, required: true },
  middleName: { type: String },
  lastName: { type: String, required: true },

  // Vital & Verification Status
  isAlive: { type: Boolean, required: true },
  isVerified: { type: Boolean, default: false },

  // Organ/Tissue Donation Preferences
  organDonation: organDetailsSchema,

  // Blood Group
  bloodGroup: {
    type: String,
    enum: ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'],
    required: true,
  },

  // Location for AI matching
  location: {
    latitude: { type: Number, required: true },
    longitude: { type: Number, required: true },
  },

  // Contact Information
  contactEmail: { type: String, required: true },
  contactPhone: { type: String, required: true },

  // Images
  userImage: { type: String },
  idImage: { type: String },

  // Medical History
  pastMedicalHistory: { type: String },

  // Timestamps
  registeredAt: { type: Date, default: Date.now },

  // AI Matching Fields
  isEligible: { type: Boolean, default: true },
  isActive: { type: Boolean, default: true },
});

// Initialize the model
const Donor = mongoose.models.donors || mongoose.model('donors', donorSchema);

export default Donor;
