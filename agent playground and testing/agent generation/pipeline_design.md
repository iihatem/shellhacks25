# Agent Generation Pipeline Architecture

## 1. Introduction

This document outlines the architecture for a "no-code" pipeline that transforms natural language requests into structured, executable agent configurations. The pipeline is designed to produce configurations that are compliant with a defined schema, such as the `AgentConfig` YAML schema used by Google's ADK.

## 2. Core Philosophy

The pipeline is built on the principle of **configuration over code**. We do not generate new Python files for each agent. Instead, we generate YAML configuration files that are consumed by a generic, reusable `BaseAgent` engine. This approach promotes consistency, security, and ease of maintenance.

## 3. Pipeline Stages

The pipeline consists of three main stages:

**Stage 1: Request Intake**

*   **Input:** A natural language request from a user, provided in a text file. The request should be concise, clear, direct, and precise.
*   **Example:** `Create a 'Support-Ticket-Router' agent. When a new support ticket is received via email, the agent should read the ticket's subject line. If the subject line contains the word 'Billing', assign the ticket to the 'Billing' department. Otherwise, assign it to 'General Support'.`

**Stage 2: Analysis & Generation (The "Plastes" Process)**

*   **Process:** A central "Generator Agent" (referred to as "Plastes") analyzes the natural language request.
*   **Analysis:** Using a powerful Large Language Model, "Plastes" performs the following analysis:
    1.  **Identifies the Agent's Core Identity:** Extracts the agent's name and description.
    2.  **Determines the Agent's Logic:** Parses the conditional logic (e.g., if/then/else statements) and the sequence of operations.
    3.  **Identifies Necessary Tools:** Determines the tools required for the agent to perform its functions (e.g., `read_email_subject`).
    4.  **Identifies Potential Sub-Agents:** Recognizes when the request involves delegating tasks to other specialized agents (e.g., a 'Billing' department agent).
*   **Generation:** Based on the analysis, "Plastes" generates an `AgentConfig` YAML file.

**Stage 3: Output & Integration**

*   **Output:** A structured `AgentConfig` YAML file that represents the requested agent.
*   **Schema:** The YAML file adheres to a predefined schema (e.g., Google ADK's `AgentConfig` schema).
*   **Tool Library:** If new tools are identified, they are defined and added to a central `tool_library.yaml`.
*   **Sub-Agent Stubs:** If new sub-agents are identified, basic `AgentConfig` files for them are created, which can be further defined later.

## 4. Key Architectural Components & Schemas

### AgentConfig YAML Schema

This schema defines the structure of a single agent.

**Parent Agent Schema:**
```yaml
name: string
model: string
description: string
instruction: string
tools: list[object]
sub_agents: list[object]
  - name: string
    description: string
    expected_behavior: string # Detailed expectation of the sub-agent's role
```

**Sub-Agent Schema:**
```yaml
metadata:
  created_by: string # Name of the parent agent that created the need for this sub-agent
name: string
model: string
description: string
instruction: string
tools: list[object]
sub_agents: list[object]
```

**Example (`support_ticket_router.yaml`):**

```yaml
name: Support-Ticket-Router
model: gemini-1.5-pro-latest
description: Routes support tickets to the correct department based on the subject line.
instruction: |
  When a new support ticket is received, you must perform the following steps:
  1. Use the `read_email_subject` tool to get the subject line of the ticket.
  2. Analyze the subject line. 
  3. If the subject line contains the word 'Billing', delegate the ticket to the 'Billing-Agent' sub-agent.
  4. Otherwise, delegate the ticket to the 'General-Support-Agent' sub-agent.
tools:
  - name: read_email_subject
    description: Reads the subject line of a new support ticket.
sub_agents:
  - name: Billing-Agent
    description: Handles billing-related support tickets.
  - name: General-Support-Agent
    description: Handles general support tickets.
```

### Tool Library Schema

This schema defines the available tools in a central library.

```yaml
tools: list[object]
  - tool_id: string # Unique identifier for the tool
    name: string
    description: string
    category: string # e.g., 'email', 'billing', 'database'
    version: string # e.g., 1.0, 1.1
    author: string # Team or individual who created the tool
    schema: object # OpenAPI schema for the tool's parameters and output
      input: object
      output: object
```

**Example (`tool_library.yaml`):**

```yaml
tools:
  - name: read_email_subject
    description: Reads the subject line of a new support ticket.
    schema:
      type: object
      properties:
        ticket_id:
          type: string
          description: The ID of the support ticket.
      required:
        - ticket_id
```

## 5. Conceptual Objects

*   **Agent Object:** The conceptual representation of an agent, fully described by its `AgentConfig` YAML file.
*   **Sub-Agent:** An agent that is referenced in another agent's `sub_agents` list. It is also defined by its own `AgentConfig` YAML file.
*   **Tool:** A specific capability that an agent can use, defined in the `tool_library.yaml`.
