import { ConvexError, v } from "convex/values";
import { action, mutation, query } from "./_generated/server";
import { api } from "./_generated/api";
import { Id } from "./_generated/dataModel";

// API router for the NerdsCourt Canon Core
// This file handles routing requests to the appropriate handlers

// Persona-related routes
export const spawnPersona = mutation({
  args: {
    persona: v.any(),
  },
  handler: async (ctx, args) => {
    // Route to the personas module
    return await ctx.runMutation(api.personas.createPersona, {
      persona: args.persona,
    });
  },
});

export const getPersona = query({
  args: {
    personaId: v.id("personas"),
  },
  handler: async (ctx, args) => {
    // Route to the personas module
    return await ctx.runQuery(api.personas.getPersonaById, {
      personaId: args.personaId,
    });
  },
});

export const listPersonas = query({
  args: {},
  handler: async (ctx) => {
    // Route to the personas module
    return await ctx.runQuery(api.personas.listAllPersonas, {});
  },
});

// Trial-related routes
export const generateTrial = mutation({
  args: {
    trial: v.any(),
  },
  handler: async (ctx, args) => {
    // Route to the trials module
    return await ctx.runMutation(api.trials.createTrial, {
      trial: args.trial,
    });
  },
});

export const getTrial = query({
  args: {
    trialId: v.id("trials"),
  },
  handler: async (ctx, args) => {
    // Route to the trials module
    return await ctx.runQuery(api.trials.getTrialById, {
      trialId: args.trialId,
    });
  },
});

export const listTrials = query({
  args: {},
  handler: async (ctx) => {
    // Route to the trials module
    return await ctx.runQuery(api.trials.listAllTrials, {});
  },
});

// Model routing
export const getModelForPersona = query({
  args: {
    personaId: v.id("personas"),
  },
  handler: async (ctx, args) => {
    const persona = await ctx.runQuery(api.personas.getPersonaById, {
      personaId: args.personaId,
    });
    
    if (!persona) {
      throw new ConvexError("Persona not found");
    }
    
    return persona.model_profile || "openrouter:gemini-pro-vision"; // Default fallback
  },
});
