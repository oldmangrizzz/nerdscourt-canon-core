import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  // Agent threads for Agency-Swarm
  agentThreads: defineTable({
    conversationId: v.string(),
    threadsData: v.any(),
    createdAt: v.string(),
    updatedAt: v.string()
  }).index("by_conversation_id", ["conversationId"]),
  
  // Agent states for individual agents
  agentStates: defineTable({
    agentId: v.string(),
    conversationId: v.string(),
    stateData: v.any(),
    createdAt: v.string(),
    updatedAt: v.string()
  }).index("by_agent_conversation", ["agentId", "conversationId"]),
  
  // Trial events for recording trial activities
  trialEvents: defineTable({
    trialId: v.string(),
    eventType: v.string(),
    eventData: v.any(),
    agentId: v.optional(v.string()),
    timestamp: v.string()
  }).index("by_trial_id", ["trialId"]),
  
  // Trials for storing trial records
  trials: defineTable({
    trialId: v.string(),
    title: v.string(),
    plaintiffs: v.array(v.string()),
    defendants: v.array(v.string()),
    charges: v.array(v.string()),
    verdict: v.optional(v.string()),
    sentencing: v.optional(v.array(v.string())),
    trialTone: v.optional(v.string()),
    linkedRecord: v.optional(v.string()),
    timestamp: v.string(),
    status: v.string(), // "pending", "in_progress", "completed"
    createdAt: v.string(),
    updatedAt: v.string()
  }).index("by_trial_id", ["trialId"]),
  
  // Agent profiles for storing agent information
  agentProfiles: defineTable({
    agentId: v.string(),
    name: v.string(),
    role: v.string(),
    description: v.string(),
    emotionalSignature: v.optional(v.object({
      tone: v.optional(v.string()),
      baseline: v.optional(v.string())
    })),
    coreTraits: v.array(v.string()),
    purpose: v.string(),
    createdAt: v.string(),
    updatedAt: v.string()
  }).index("by_agent_id", ["agentId"]),
  
  // NerdBible entries for storing canonical lore
  nerdBibleEntries: defineTable({
    entryId: v.string(),
    title: v.string(),
    content: v.string(),
    category: v.string(),
    tags: v.array(v.string()),
    relatedEntries: v.array(v.string()),
    createdAt: v.string(),
    updatedAt: v.string()
  }).index("by_entry_id", ["entryId"])
    .index("by_category", ["category"])
    .index("by_tags", ["tags"]),
  
  // CustomGPT sessions for tracking user interactions
  customGptSessions: defineTable({
    sessionId: v.string(),
    userId: v.optional(v.string()),
    startTime: v.string(),
    lastActivity: v.string(),
    metadata: v.optional(v.any())
  }).index("by_session_id", ["sessionId"])
    .index("by_user_id", ["userId"])
});
