export type Difficulty = 'easy' | 'medium' | 'advanced';

/**
 * A single step within a tutorial.
 */
export interface Step {
  /** The position/order of the step in the tutorial (1-based or 0-based as used by the app). */
  order: number;
  /** Short title for the step. */
  title: string;
  /** Detailed description or instructions for this step. */
  description: string;
  /** Optional URL or path to an image illustrating the step. */
  image?: string;
}

/**
 * Tutorial metadata and content.
 */
export interface Tutorial {
  /** Unique identifier for the tutorial. */
  id: string;
  /** Title of the tutorial. */
  title: string;
  /** Difficulty level. */
  difficulty: Difficulty;
  /** Recommended age range as a string (e.g. "8-12", "Teen", "All ages"). */
  ageRange: string;
  /** Short description or summary of the tutorial. */
  description: string;
  /** Ordered list of steps that make up the tutorial. */
  steps: Step[];
  /** Path to the template used for rendering this tutorial (e.g. component/template identifier or file path). */
  templatePath: string;
  /** Path or URL to a placeholder image used when specific step images are unavailable. */
  placeholderImage: string;
}