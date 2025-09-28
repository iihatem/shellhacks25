# Plastes: Internal Design & Process

This document outlines the internal process of "Plastes," the generator agent responsible for converting natural language requests into `AgentConfig` YAML files.

## 1. Core Objective

Plastes' primary function is to act as a highly intelligent parser and generator. It must bridge the gap between a user's high-level, natural language request and the structured, detailed `AgentConfig` schema.

## 2. Internal Process Flow

When Plastes receives a request, it executes the following internal sequence:

### Step 1: Deconstruction and Analysis

Plastes uses a powerful LLM (e.g., Gemini 1.5 Pro) with a specialized meta-prompt to deconstruct the user's request. The goal of this step is to break down the request into its fundamental components.

*   **Meta-Prompt:** The prompt sent to the LLM would be something like:
    > "You are an expert in AI agent architecture. Analyze the following user request and extract the specified components into a JSON object. The components to extract are: `agent_name`, `agent_description`, `step_by_step_logic`, `required_tools`, and `required_sub_agents`."

*   **Input:** The user's natural language request.
*   **Output:** A structured JSON object containing the initial analysis.

**Example:**

For the request: `Create a 'Support-Ticket-Router' agent...`

The LLM would produce a JSON object like:
```json
{
  "agent_name": "Support-Ticket-Router",
  "agent_description": "An agent that routes support tickets based on their subject line.",
  "step_by_step_logic": [
    "Trigger: When a new support ticket is received via email.",
    "Step 1: Read the ticket's subject line.",
    "Step 2: If the subject contains 'Billing', delegate to 'Billing' department.",
    "Step 3: Otherwise, delegate to 'General Support' department."
  ],
  "required_tools": ["read_email_subject"],
  "required_sub_agents": ["Billing-Agent", "General-Support-Agent"]
}
```

### Step 2: Refinement and Structuring

Plastes takes the JSON object from Step 1 and refines it into the final `AgentConfig` YAML structure.

*   **Instruction Formatting:** The `step_by_step_logic` is formatted into the `instruction` field of the YAML.
*   **Tool Verification:** Plastes checks the `required_tools` against the `tool_library.yaml`. 
    *   If a tool exists, its definition is used.
    *   If a tool does not exist, Plastes generates a new, basic tool definition and adds it to the library. It might also flag this new tool for human review.
*   **Sub-Agent Structuring:** For each sub-agent in `required_sub_agents`, Plastes creates the sub-agent block in the parent's YAML, including generating a concise `description` and a detailed `expected_behavior` based on the initial request.

### Step 3: YAML Generation and Validation

*   **Generation:** Plastes assembles the final `AgentConfig` YAML file.
*   **Validation:** It then validates the generated YAML against our defined schema to ensure it is well-formed.
*   **Sub-Agent Stub Generation:** For any *new* sub-agents identified, Plastes also generates their initial `AgentConfig` files (e.g., `billing_agent.yaml`), including the `metadata.created_by` field.

## 3. Self-Correction and Ambiguity Resolution

If the user's request is ambiguous, Plastes is designed to handle it gracefully. In Step 1, if the LLM cannot confidently extract the required components, Plastes' process dictates that it should not proceed. Instead, it should return a question to the user, asking for clarification on the ambiguous part of the request. This ensures that the generated agents are based on clear and precise instructions.