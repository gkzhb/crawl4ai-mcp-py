/**
 * OpenCode Skills Plugin
 *
 * Implements Anthropic's Agent Skills Specification (v1.0) for OpenCode.
 *
 * Features:
 * - Discovers SKILL.md files from .opencode/skills/, ~/.opencode/skills/, and ~/.config/opencode/skills/
 * - Validates skills against Anthropic's spec (YAML frontmatter + Markdown)
 * - Registers a "skills" tool to fetch skill details
 * - Returns skill content with base directory context for path resolution
 * - Supports nested skills with proper naming
 *
 * Design Decisions:
 * - Tool restrictions handled at agent level (not skill level)
 * - Base directory context enables relative path resolution
 * - Skills require restart to reload (acceptable trade-off)
 *
 * @see https://github.com/anthropics/skills
 */

import type { Plugin } from "@opencode-ai/plugin"
import { tool } from "@opencode-ai/plugin"
import matter from "gray-matter"
import { Glob } from "bun"
import { join, dirname, basename, relative, sep } from "path"
import { z } from "zod"
import os from "os"
import { promises as fs } from "fs"

// Types
interface Skill {
  name: string // From frontmatter (e.g., "brand-guidelines")
  fullPath: string // Full directory path to skill
  toolName: string // Generated tool name (e.g., "skills_brand_guidelines")
  description: string // From frontmatter
  allowedTools?: string[] // Parsed but not enforced (agent-level restrictions instead)
  metadata?: Record<string, string>
  license?: string
  content: string // Markdown body
  path: string // Full path to SKILL.md
  location: string // location of skills, project or global
}

// Validation Schema
const SkillFrontmatterSchema = z.object({
  name: z
    .string()
    .regex(/^[a-z0-9-]+$/, "Name must be lowercase alphanumeric with hyphens")
    .min(1, "Name cannot be empty"),
  description: z
    .string()
    .min(10, "Description must be at least 10 characters for discoverability"),
  license: z.string().optional(),
  "allowed-tools": z.array(z.string()).optional(),
  metadata: z.record(z.string()).optional(),
})

type SkillFrontmatter = z.infer<typeof SkillFrontmatterSchema>

/**
 * Generate tool name from skill path
 * Examples:
 *   .opencode/skills/brand-guidelines/SKILL.md → skills_brand_guidelines
 *   .opencode/skills/document-skills/docx/SKILL.md → skills_document_skills_docx
 */
function generateToolName(skillPath: string, baseDir: string): string {
  const rel = relative(baseDir, skillPath)
  const dirPath = dirname(rel)
  const components = dirPath.split(sep).filter((c) => c !== ".")
  return "skills_" + components.join("_").replace(/-/g, "_")
}

/**
 * Parse a SKILL.md file and return structured skill data
 * Returns null if parsing fails (with error logging)
 */
async function parseSkill(options: {
  skillPath: string
  baseDir: string
  cwd: string
}): Promise<Skill | null> {
  const { skillPath, baseDir, cwd } = options
  try {
    // Read file
    const content = await Bun.file(skillPath).text()

    // Parse YAML frontmatter
    const { data, content: markdown } = matter(content)

    // Validate frontmatter schema
    let frontmatter: SkillFrontmatter
    try {
      frontmatter = SkillFrontmatterSchema.parse(data)
    } catch (error) {
      if (error instanceof z.ZodError) {
        console.error(`❌ Invalid frontmatter in ${skillPath}:`)
        error.errors.forEach((err) => {
          console.error(`   - ${err.path.join(".")}: ${err.message}`)
        })
      }
      return null
    }

    // Validate name matches directory
    const skillDir = basename(dirname(skillPath))
    if (frontmatter.name !== skillDir) {
      console.error(
        `❌ Name mismatch in ${skillPath}:`,
        `\n   Frontmatter name: "${frontmatter.name}"`,
        `\n   Directory name: "${skillDir}"`,
        `\n   Fix: Update the 'name' field in SKILL.md to match the directory name`,
      )
      return null
    }

    // Generate tool name from path
    const toolName = generateToolName(skillPath, baseDir)

    return {
      name: frontmatter.name,
      fullPath: dirname(skillPath),
      toolName,
      description: frontmatter.description,
      allowedTools: frontmatter["allowed-tools"],
      metadata: frontmatter.metadata,
      license: frontmatter.license,
      content: markdown.trim(),
      path: skillPath,
      location: skillPath === cwd ? "project" : "global",
    }
  } catch (error) {
    console.error(
      `❌ Error parsing skill ${skillPath}:`,
      error instanceof Error ? error.message : String(error),
    )
    return null
  }
}

/**
 * Discover all SKILL.md files in the specified base paths
 */
async function discoverSkills(basePaths: string[]): Promise<Skill[]> {
  const skills: Skill[] = []
  const cwd = basePaths[0] ?? ""

  for (const basePath of basePaths) {
    try {
      // Check if directory exists before scanning
      try {
        await fs.access(basePath)
      } catch {
        // directory not exist, skip scanning
        continue
      }

      // Find all SKILL.md files recursively
      const glob = new Glob("**/SKILL.md")
      let skillCount = 0

      for await (const match of glob.scan({
        cwd: basePath,
        absolute: true,
      })) {
        const skill = await parseSkill({
          skillPath: match,
          baseDir: basePath,
          cwd,
        })
        if (skill) {
          skills.push(skill)
          skillCount++
        }
      }

      console.log(`Found ${skillCount} skills in ${basePath}`)
    } catch (error) {
      // Log other errors but continue with other paths
      console.warn(
        `⚠️  Could not scan skills directory: ${basePath}`,
        `\n   Error: ${(error as Error).message}`,
      )
    }
  }

  // Detect duplicate tool names
  const toolNames = new Set<string>()
  const duplicates = []

  for (const skill of skills) {
    if (toolNames.has(skill.toolName)) {
      duplicates.push(skill.toolName)
    }
    toolNames.add(skill.toolName)
  }

  if (duplicates.length > 0) {
    console.warn(`⚠️  Duplicate tool names detected:`, duplicates)
  }

  return skills
}

const getSkillXml = (skill: Skill) => `<skill>
<name>
${skill.name}
</name>
<description>
${skill.description}
</description>
<location>
${skill.location}
</location>
</skill>`

const constructToolDesc = (skills: Skill[]) => {
  return `Execute a skill within the main conversation

<skills_instructions>
When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively. Skills provide specialized capabilities and domain knowledge.

How to use skills:
- **Invoke skills using this tool \`skills\` with the skill name only (no arguments)**
- When you invoke a skill, you will see <command-message>The "{name}" skill is loading</command-message>
- The skill's prompt will expand and provide detailed instructions on how to complete the task
- Examples:
  - \`command: "pdf"\` - invoke the pdf skill
  - \`command: "xlsx"\` - invoke the xlsx skill
  - \`command: "ms-office-suite:pdf"\` - invoke using fully qualified name

Important:
- Only use skills listed in <available_skills> below
- Do not invoke a skill that is already running
- Do not use this tool for built-in CLI commands (like /help, /clear, etc.)
</skills_instructions>

<available_skills>
${skills.map((skill) => getSkillXml(skill)).join("\n")}
</available_skills>`
}

export const SkillsPlugin: Plugin = async (ctx) => {
  // Determine config path: $XDG_CONFIG_HOME/opencode/skills or ~/.config/opencode/skills
  const xdgConfigHome = process.env.XDG_CONFIG_HOME
  const configSkillsPath = xdgConfigHome
    ? join(xdgConfigHome, "opencode/skills")
    : join(os.homedir(), ".config/opencode/skills")

  const skills = await discoverSkills([
    join(ctx.directory, ".opencode/skills"),
    join(os.homedir(), ".opencode/skills"),
    configSkillsPath,
  ])

  // Create a tool to fetch skill details
  const tools: Record<string, any> = {}

  tools["skills"] = tool({
    description: constructToolDesc(skills),
    args: {
      command: tool.schema
        .string()
        .describe('The skill name (no arguments). E.g., "pdf" or "xlsx"'),
    },
    async execute(args, toolCtx) {
      const skillName = args.command
      const skill = skills.find((s) => s.name === skillName)

      if (!skill) {
        return `Skill "${skillName}" not found. Available skills: ${skills.map((s) => s.name).join(", ")}`
      }

      return `<command-message>The "${skillName}" skill is running</command-message>\n<command-name>${skillName}</command-name>

# ${skillName} Skill information

Base directory for this skill: ${skill.fullPath}

Skill Content:

${skill.content}`
    },
  })

  return { tool: tools }
}
