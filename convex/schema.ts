import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

// Define the schema for the NerdsCourt Canon Core database
export default defineSchema({
  // Personas table - stores character/agent data
  personas: defineTable({
    // Identity fields
    identity: v.object({
      designation: v.string(),
      alias: v.string(),
      universe: v.string(),
      spawned_from: v.string(),
    }),
    // Personality framework
    personality_framework: v.string(),
    // Soul data
    soul_data: v.object({
      core_traits: v.array(v.string()),
      purpose: v.string(),
      parable: v.string(),
    }),
    // Self-awareness description
    self_awareness: v.string(),
    // Calibration source
    calibrated_by: v.string(),
    // Model profile for AI routing
    model_profile: v.string(),
    // Session ID
    session_id: v.string(),
    // Timestamp
    generated_at: v.string(),
    // Creation timestamp in the database
    created_at: v.string(),
  }),

  // Trials table - stores trial records
  trials: defineTable({
    // Case ID
    case_id: v.string(),
    // Trial title
    title: v.string(),
    // Plaintiffs
    plaintiffs: v.array(v.string()),
    // Defendants
    defendants: v.array(v.string()),
    // Charges
    charges: v.array(v.string()),
    // Verdict
    verdict: v.string(),
    // Sentencing
    sentencing: v.array(v.string()),
    // Notable quotes
    notable_quotes: v.array(v.string()),
    // Trial tone
    trial_tone: v.string(),
    // Linked record
    linked_record: v.optional(v.string()),
    // Timestamp
    timestamp: v.string(),
    // Post-credit scene
    post_credit_scene: v.object({
      setting: v.string(),
      present: v.array(v.string()),
      quote: v.string(),
    }),
    // Creation timestamp in the database
    created_at: v.string(),
  }),
});
