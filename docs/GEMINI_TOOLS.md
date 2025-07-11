# Gemini AI Integration Tools

## Overview
The Gemini integration provides 6 powerful tools that leverage Google's Gemini AI model for enhanced analysis, brainstorming, and research capabilities. These tools complement Claude's capabilities by providing alternative perspectives and leveraging Gemini's 1M token context window.

## Available Tools

### 1. `gemini_query`
**Purpose**: General-purpose AI queries for analysis and insights
**Parameters**:
- `prompt` (required): The question or prompt for Gemini
- `context` (optional): Additional background information
- `temperature` (optional): Creativity level (0.0-1.0, default 0.7)

**Example**:
```json
{
  "prompt": "What are the implications of gyrovector spaces for modern physics?",
  "context": "Focus on applications in special relativity and quantum mechanics",
  "temperature": 0.5
}
```

### 2. `gemini_analyze_code`
**Purpose**: Analyze code for security, performance, or quality issues
**Parameters**:
- `code` (required): The code to analyze
- `analysis_type` (optional): "security", "performance", "quality", or "general" (default)
- `language` (optional): Programming language (auto-detected if not specified)

**Example**:
```json
{
  "code": "def process_data(input): return eval(input)",
  "analysis_type": "security",
  "language": "python"
}
```

### 3. `gemini_brainstorm`
**Purpose**: Generate creative ideas and solutions
**Parameters**:
- `topic` (required): The topic or problem to brainstorm
- `constraints` (optional): Any requirements or limitations
- `num_ideas` (optional): Number of ideas to generate (default 5)

**Example**:
```json
{
  "topic": "Ways to visualize 4D hyperbolic geometry",
  "constraints": "Must be implementable in Manim",
  "num_ideas": 7
}
```

### 4. `gemini_summarize`
**Purpose**: Summarize large texts using Gemini's 1M token window
**Parameters**:
- `text` (required): The text to summarize
- `summary_type` (optional): "brief", "detailed", "bullet_points", or "key_insights" (default "brief")
- `max_length` (optional): Maximum length in words

**Example**:
```json
{
  "text": "[Long research paper content...]",
  "summary_type": "key_insights",
  "max_length": 200
}
```

### 5. `gemini_math_analysis`
**Purpose**: Analyze mathematical concepts and theorems
**Parameters**:
- `concept` (required): Mathematical concept to analyze
- `approach` (optional): "proof", "visualization", "applications", or "connections" (default)
- `context` (optional): Specific mathematical context

**Example**:
```json
{
  "concept": "Möbius transformations in gyrovector spaces",
  "approach": "connections",
  "context": "Relate to conformal geometry and special relativity"
}
```

### 6. `gemini_research_review`
**Purpose**: Review and critique research content
**Parameters**:
- `content` (required): Research content to review
- `focus_areas` (optional): Array of specific areas to focus on
- `academic_level` (optional): "undergraduate", "graduate", "research", or "publication" (default "research")

**Example**:
```json
{
  "content": "[Research abstract or paper section...]",
  "focus_areas": ["methodology", "novelty", "mathematical rigor"],
  "academic_level": "publication"
}
```

## Use Cases

### 1. Collaborative Analysis
Ask Gemini for a second opinion on complex mathematical proofs or research directions:
```
"Use gemini_math_analysis to verify this proof of the gyrotriangle inequality"
```

### 2. Large Document Processing
Leverage Gemini's 1M token context for analyzing entire research papers:
```
"Use gemini_summarize to extract key insights from this 100-page thesis"
```

### 3. Security Auditing
Get thorough code security analysis:
```
"Use gemini_analyze_code with analysis_type='security' on our authentication system"
```

### 4. Research Enhancement
Generate new research directions and connections:
```
"Use gemini_brainstorm to explore applications of gyrovector spaces in machine learning"
```

## Best Practices

1. **Temperature Settings**:
   - Use lower temperatures (0.1-0.3) for factual analysis
   - Use medium temperatures (0.4-0.6) for balanced responses
   - Use higher temperatures (0.7-0.9) for creative brainstorming

2. **Context Windows**:
   - Gemini can handle up to 1M tokens
   - Ideal for analyzing entire codebases or research collections
   - Break very large inputs into logical sections for better results

3. **Combining with Other Tools**:
   - Use Perplexity for recent research discovery
   - Use Gemini for deep analysis of discovered papers
   - Use Wolfram for mathematical validation
   - Use Manim for visualizing Gemini's suggestions

## Rate Limits

Free tier includes:
- 1,000 requests per day
- 60 requests per minute
- 1M token context window
- Access to Gemini 2.0 Flash

## Error Handling

Common errors and solutions:
- **API Key Issues**: Ensure GEMINI_API_KEY is set in .env
- **Rate Limits**: Implement delays between requests if needed
- **Context Too Large**: Split into smaller chunks (rare with 1M limit)

## Integration Examples

### Research Workflow
```python
# 1. Discover papers with Perplexity
papers = await discover_research("gyrovector spaces applications")

# 2. Analyze with Gemini
analysis = await gemini_research_review(
    content=papers[0]["abstract"],
    focus_areas=["novelty", "mathematical rigor"]
)

# 3. Brainstorm extensions
ideas = await gemini_brainstorm(
    topic="Extending this research to quantum computing",
    num_ideas=10
)

# 4. Create visualization
animation = await create_manim_animation(
    concept=ideas["best_visualization_idea"],
    animation_type="3d_transformation"
)
```

### Code Review Pipeline
```python
# 1. Read code from Dropbox
code = await read_dropbox_file("src/core_algorithm.py")

# 2. Security analysis
security = await gemini_analyze_code(
    code=code["content"],
    analysis_type="security"
)

# 3. Performance analysis
performance = await gemini_analyze_code(
    code=code["content"],
    analysis_type="performance"
)

# 4. Save report to Obsidian
await ingest_to_obsidian(
    content=f"# Code Review\n\n## Security\n{security}\n\n## Performance\n{performance}",
    title="Core Algorithm Review",
    folder="reviews"
)
```