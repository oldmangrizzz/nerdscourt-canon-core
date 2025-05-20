import { ConvexError, v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { Id } from "./_generated/dataModel";

// Schema for trial data
// This matches the structure from trial_logic/trial_forge.py
export type Trial = {
  case_id: string;
  title: string;
  plaintiffs: string[];
  defendants: string[];
  charges: string[];
  verdict: string;
  sentencing: string[];
  notable_quotes: string[];
  trial_tone: string;
  linked_record: string | null;
  timestamp: string;
  post_credit_scene: {
    setting: string;
    present: string[];
    quote: string;
  };
};

// Create a new trial
export const createTrial = mutation({
  args: {
    trial: v.any(),
  },
  handler: async (ctx, args) => {
    // Validate the trial data structure
    const trial = args.trial as Trial;
    
    if (!trial.title || !trial.case_id) {
      throw new ConvexError("Invalid trial data: missing title or case_id");
    }
    
    // Store the trial in the database
    const trialId = await ctx.db.insert("trials", {
      ...trial,
      created_at: new Date().toISOString(),
    });
    
    return {
      id: trialId,
      ...trial,
    };
  },
});

// Get a trial by ID
export const getTrialById = query({
  args: {
    trialId: v.id("trials"),
  },
  handler: async (ctx, args) => {
    const trial = await ctx.db.get(args.trialId);
    
    if (!trial) {
      throw new ConvexError("Trial not found");
    }
    
    return trial;
  },
});

// List all trials
export const listAllTrials = query({
  args: {},
  handler: async (ctx) => {
    const trials = await ctx.db.query("trials").collect();
    return trials;
  },
});

// Get trials by plaintiff
export const getTrialsByPlaintiff = query({
  args: {
    plaintiff: v.string(),
  },
  handler: async (ctx, args) => {
    const trials = await ctx.db.query("trials").collect();
    
    // Filter trials that have the specified plaintiff
    return trials.filter((trial) => {
      const plaintiffs = trial.plaintiffs || [];
      return plaintiffs.some((p: string) => 
        p.toLowerCase().includes(args.plaintiff.toLowerCase())
      );
    });
  },
});

// Get trials by defendant
export const getTrialsByDefendant = query({
  args: {
    defendant: v.string(),
  },
  handler: async (ctx, args) => {
    const trials = await ctx.db.query("trials").collect();
    
    // Filter trials that have the specified defendant
    return trials.filter((trial) => {
      const defendants = trial.defendants || [];
      return defendants.some((d: string) => 
        d.toLowerCase().includes(args.defendant.toLowerCase())
      );
    });
  },
});

// Update trial verdict
export const updateVerdict = mutation({
  args: {
    trialId: v.id("trials"),
    verdict: v.string(),
    sentencing: v.array(v.string()),
  },
  handler: async (ctx, args) => {
    const trial = await ctx.db.get(args.trialId);
    
    if (!trial) {
      throw new ConvexError("Trial not found");
    }
    
    await ctx.db.patch(args.trialId, {
      verdict: args.verdict,
      sentencing: args.sentencing,
    });
    
    return await ctx.db.get(args.trialId);
  },
});
