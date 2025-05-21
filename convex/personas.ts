import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { Id } from "./_generated/dataModel";

// Use ConvexError from the values module
const ConvexError = v.Error;

// Schema for persona data
// This matches the structure from krakoa_engine/generate_krakoa_persona.py
export type Persona = {
  identity: {
    designation: string;
    alias: string;
    universe: string;
    spawned_from: string;
  };
  personality_framework: string;
  soul_data: {
    core_traits: string[];
    purpose: string;
    parable: string;
  };
  self_awareness: string;
  calibrated_by: string;
  model_profile: string;
  session_id: string;
  generated_at: string;
};

// Create a new persona
export const createPersona = mutation({
  args: {
    persona: v.any(),
  },
  handler: async (ctx, args) => {
    // Validate the persona data structure
    const persona = args.persona as Persona;

    if (!persona.identity || !persona.identity.designation) {
      throw new ConvexError("Invalid persona data: missing identity.designation");
    }

    // Store the persona in the database
    const personaId = await ctx.db.insert("personas", {
      ...persona,
      created_at: new Date().toISOString(),
    });

    return {
      id: personaId,
      ...persona,
    };
  },
});

// Get a persona by ID
export const getPersonaById = query({
  args: {
    personaId: v.id("personas"),
  },
  handler: async (ctx, args) => {
    const persona = await ctx.db.get(args.personaId);

    if (!persona) {
      throw new ConvexError("Persona not found");
    }

    return persona;
  },
});

// List all personas
export const listAllPersonas = query({
  args: {},
  handler: async (ctx) => {
    const personas = await ctx.db.query("personas").collect();
    return personas;
  },
});

// Get personas by universe
export const getPersonasByUniverse = query({
  args: {
    universe: v.string(),
  },
  handler: async (ctx, args) => {
    const personas = await ctx.db
      .query("personas")
      .filter((q) => q.eq(q.field("identity.universe"), args.universe))
      .collect();

    return personas;
  },
});

// Get personas by trait
export const getPersonasByTrait = query({
  args: {
    trait: v.string(),
  },
  handler: async (ctx, args) => {
    const personas = await ctx.db.query("personas").collect();

    // Filter personas that have the specified trait
    return personas.filter((persona) => {
      const traits = persona.soul_data?.core_traits || [];
      return traits.some((t: string) =>
        t.toLowerCase().includes(args.trait.toLowerCase())
      );
    });
  },
});
