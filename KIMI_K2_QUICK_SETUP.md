# Kimi K2 Integration Quick Setup Guide

## 🚀 Quick Setup (5 minutes)

### 1. Get your Groq API Key
1. Visit [Groq Cloud Console](https://console.groq.com)
2. Create an account or sign in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `gsk_`)

### 2. Add to Environment
```bash
# Add to your .env file
echo "GROQ_API_KEY=gsk_your_actual_key_here" >> .env

# Verify it's loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅' if os.getenv('GROQ_API_KEY') else '❌')"
```

### 3. Install Dependencies
```bash
# Ensure you're in your virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Groq SDK
pip install groq>=0.11.0

# Verify installation
python -c "import groq; print('✅ Groq SDK installed')"
```

### 4. Test Kimi K2 Integration
```bash
# Quick test
python scripts/kimi_k2_quickstart.py benchmark

# Interactive mode
python scripts/kimi_k2_quickstart.py interactive
```

### 5. Restart Claude Desktop
After setup, restart Claude Desktop to load the new tools.

## 🧪 Quick Test Commands

Test Kimi K2 is working:
```python
# In Claude, try these commands:

# Basic query
Use the kimi_k2_query tool to explain gyrovector spaces

# Problem solving
Use kimi_k2_solve_problem to calculate u ⊕ v where u=[0.3,0.4,0] and v=[0.1,0.2,0.5] in the Poincaré ball model

# Visualization
Use kimi_k2_generate_visualization to create a Manim animation of gyrovector addition
```

## 📊 Expected Performance

With Kimi K2 via Groq, you should see:
- **Response time**: 200-500ms for most queries
- **Tokens/second**: ~185 (much faster than typical LLMs)
- **Context window**: 128K tokens (can handle entire papers)
- **Math accuracy**: 97.4% on MATH-500 benchmark

## 🔧 Troubleshooting

### "Kimi K2 integration not initialized"
- Check GROQ_API_KEY is in .env
- Restart Claude Desktop
- Check logs: `tail -f ~/.claude/logs/mcp.log`

### Slow responses
- Check your internet connection
- Verify Groq service status at status.groq.com
- Try a simpler query first

### API errors
- Verify your API key is valid
- Check you haven't hit rate limits
- Ensure groq package is installed: `pip show groq`

## 🎯 Next Steps

1. **Run the example workflow**:
   ```bash
   python scripts/kimi_k2_workflow_example.py
   ```

2. **Try the visualization demo**:
   ```bash
   manim -pql visualizations/gyrovector_lattice_visualization.py
   ```

3. **Explore mathematical domains**:
   - Gyrovector spaces
   - Lattice theory
   - Recursive harmonics
   - Orbifolds

4. **Combine with other tools**:
   - Use with Claude Flow for complex workflows
   - Validate results with Wolfram Alpha
   - Create knowledge artifacts in Obsidian

## 📚 Resources

- [Kimi K2 Documentation](KIMI_K2_INTEGRATION.md)
- [Groq API Docs](https://console.groq.com/docs)
- [Gyrovector Theory Papers](https://arxiv.org/abs/math/0406130)
- [MCP Specification](https://modelcontextprotocol.io)

---

**Need help?** Check the full documentation or open an issue on GitHub.
