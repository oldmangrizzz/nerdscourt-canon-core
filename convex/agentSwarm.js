import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

/**
 * Save agent threads data to the database.
 * 
 * This function stores the conversation threads between agents in the Agency-Swarm
 * framework. Each conversation has a unique ID provided by the CustomGPT.
 */
export const saveAgentThreads = mutation({
  args: {
    conversationId: v.string(),
    threadsData: v.any()
  },
  handler: async (ctx, { conversationId, threadsData }) => {
    // Check if thread exists
    const existing = await ctx.db
      .query("agentThreads")
      .withIndex("by_conversation_id", (q) => 
        q.eq("conversationId", conversationId)
      )
      .first();
    
    if (existing) {
      // Update existing thread
      await ctx.db.patch(existing._id, { 
        threadsData,
        updatedAt: new Date().toISOString()
      });
      return { success: true, id: existing._id };
    } else {
      // Create new thread
      const id = await ctx.db.insert("agentThreads", { 
        conversationId, 
        threadsData,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      });
      return { success: true, id };
    }
  }
});

/**
 * Get agent threads data from the database.
 * 
 * This function retrieves the conversation threads between agents for a specific
 * conversation ID.
 */
export const getAgentThreads = query({
  args: {
    conversationId: v.string()
  },
  handler: async (ctx, { conversationId }) => {
    const thread = await ctx.db
      .query("agentThreads")
      .withIndex("by_conversation_id", (q) => 
        q.eq("conversationId", conversationId)
      )
      .first();
    
    return thread || { threadsData: {} };
  }
});

/**
 * Save agent state to the database.
 * 
 * This function stores the state of an individual agent within a conversation.
 * This allows agents to maintain context and memory across interactions.
 */
export const saveAgentState = mutation({
  args: {
    agentId: v.string(),
    conversationId: v.string(),
    stateData: v.any()
  },
  handler: async (ctx, { agentId, conversationId, stateData }) => {
    // Check if state exists
    const existing = await ctx.db
      .query("agentStates")
      .withIndex("by_agent_conversation", (q) => 
        q.eq("agentId", agentId).eq("conversationId", conversationId)
      )
      .first();
    
    if (existing) {
      // Update existing state
      await ctx.db.patch(existing._id, { 
        stateData,
        updatedAt: new Date().toISOString()
      });
      return { success: true, id: existing._id };
    } else {
      // Create new state
      const id = await ctx.db.insert("agentStates", { 
        agentId,
        conversationId, 
        stateData,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      });
      return { success: true, id };
    }
  }
});

/**
 * Get agent state from the database.
 * 
 * This function retrieves the state of an individual agent within a conversation.
 */
export const getAgentState = query({
  args: {
    agentId: v.string(),
    conversationId: v.string()
  },
  handler: async (ctx, { agentId, conversationId }) => {
    const state = await ctx.db
      .query("agentStates")
      .withIndex("by_agent_conversation", (q) => 
        q.eq("agentId", agentId).eq("conversationId", conversationId)
      )
      .first();
    
    return state || { stateData: {} };
  }
});

/**
 * Record a trial event in the database.
 * 
 * This function stores events that occur during a trial, such as
 * agent interactions, verdicts, and sentencing.
 */
export const recordTrialEvent = mutation({
  args: {
    trialId: v.string(),
    eventType: v.string(),
    eventData: v.any(),
    agentId: v.optional(v.string())
  },
  handler: async (ctx, { trialId, eventType, eventData, agentId }) => {
    const id = await ctx.db.insert("trialEvents", {
      trialId,
      eventType,
      eventData,
      agentId,
      timestamp: new Date().toISOString()
    });
    
    return { success: true, id };
  }
});

/**
 * Get trial events from the database.
 * 
 * This function retrieves events for a specific trial, optionally
 * filtered by event type.
 */
export const getTrialEvents = query({
  args: {
    trialId: v.string(),
    eventType: v.optional(v.string())
  },
  handler: async (ctx, { trialId, eventType }) => {
    let query = ctx.db
      .query("trialEvents")
      .withIndex("by_trial_id", (q) => q.eq("trialId", trialId));
    
    if (eventType) {
      query = query.filter((q) => q.eq(q.field("eventType"), eventType));
    }
    
    const events = await query.order("desc").collect();
    return events;
  }
});
