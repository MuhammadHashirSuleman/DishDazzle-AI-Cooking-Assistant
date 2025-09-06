# 🔧 DishDazzle API Setup Guide

## 🚀 Overview

DishDazzle uses the **OpenRouter API** to provide access to multiple powerful AI models. This gives you flexibility to choose the best model for your cooking assistance needs while maintaining consistent performance and reliability.

### 🤖 Supported AI Models

1. **DeepSeek v3.1** (`deepseek/deepseek-chat`)
   - ⚡ Fast response times
   - 💡 Excellent for recipe suggestions
   - 🎯 Good at following cooking instructions

2. **Llama 3.1 70B Instruct** (`meta-llama/llama-3.1-70b-instruct`)
   - 🧠 Advanced reasoning capabilities
   - 📚 Comprehensive cooking knowledge
   - 🗣️ Natural conversation flow

## 🔑 Getting Your API Key

### Step 1: Create OpenRouter Account

1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Click **Sign Up** to create a new account
3. Verify your email address
4. Complete your profile setup

### Step 2: Generate API Key

1. Navigate to your **Dashboard**
2. Go to the **Keys** section
3. Click **Create New Key**
4. Give your key a descriptive name (e.g., "DishDazzle App")
5. Copy the generated API key (starts with `sk-or-...`)

⚠️ **Important**: Store your API key securely - you won't be able to see it again!

## ⚙️ Configuring DishDazzle

### Method 1: Using the Settings Dialog (Recommended)

1. **Launch DishDazzle** application
2. Click the **◆ Settings** button in the sidebar
3. In the Preferences dialog:
   - Find the **API Settings** section
   - Enter your OpenRouter API key
   - Select your preferred AI model from the dropdown
   - Click **OK** to save

### Method 2: Manual Configuration

Edit the configuration file at `config/config.json`:

```json
{
  "api": {
    "openrouter": {
      "deepseek": {
        "api_key": "sk-or-your-api-key-here",
        "model": "deepseek/deepseek-chat"
      },
      "llama": {
        "api_key": "sk-or-your-api-key-here",
        "model": "meta-llama/llama-3.1-70b-instruct"
      }
    }
  },
  "theme": "light",
  "auto_save": true,
  "cache": {
    "enabled": true
  }
}
```

## 💰 Understanding Costs

### Pricing Model
- OpenRouter charges per **token** (input + output)
- **DeepSeek**: ~$0.14 per 1M input tokens, ~$0.28 per 1M output tokens
- **Llama 3.1 70B**: ~$0.52 per 1M input tokens, ~$0.75 per 1M output tokens

### Typical Usage
- **Recipe suggestion**: ~500-1500 tokens (~$0.001-$0.003)
- **Chat response**: ~200-800 tokens (~$0.0003-$0.001)
- **Cooking help**: ~300-1000 tokens (~$0.0005-$0.002)

### Cost Optimization Tips
- ⚡ Use **DeepSeek** for general cooking questions (faster + cheaper)
- 🧠 Use **Llama** for complex recipe development
- 💾 Enable **response caching** to reduce repeated API calls
- 📄 Keep conversations concise for better cost efficiency

## 🔄 Switching Between Models

You can change AI models anytime:

1. **In-App Switching**:
   - Use the model dropdown in the sidebar
   - Changes apply immediately to new conversations

2. **Per-Feature Optimization**:
   - **Recipe Suggestions**: DeepSeek (fast, cost-effective)
   - **Complex Cooking Help**: Llama (detailed, nuanced responses)
   - **Quick Questions**: DeepSeek (immediate answers)

## 🐛 Troubleshooting

### ❌ Common Issues

**"API Key Invalid" Error**
- ✅ Verify key starts with `sk-or-`
- ✅ Check for extra spaces or characters
- ✅ Regenerate key if needed

**"Rate Limited" Error**
- ✅ Wait a few minutes before retrying
- ✅ Check your OpenRouter usage limits
- ✅ Consider upgrading your account tier

**"Insufficient Credits" Error**
- ✅ Add funds to your OpenRouter account
- ✅ Check your current balance in the dashboard
- ✅ Set up auto-recharge if available

**Slow Response Times**
- ✅ Try switching to DeepSeek (faster model)
- ✅ Check your internet connection
- ✅ OpenRouter may be experiencing high traffic

**Connection Timeout**
- ✅ Restart the application
- ✅ Check firewall settings
- ✅ Verify internet connectivity

### 📊 Monitoring Usage

1. **OpenRouter Dashboard**:
   - View real-time usage statistics
   - Track spending by model
   - Set usage alerts

2. **DishDazzle Logs**:
   - Check `logs/` directory for API calls
   - Monitor response times and errors
   - Review caching effectiveness

## 🔒 Security Best Practices

### 🔐 API Key Security
- ❌ **Never share** your API key
- ❌ **Don't commit** keys to version control
- ✅ **Regenerate keys** if compromised
- ✅ **Monitor usage** for suspicious activity

### 🛡️ Application Security
- ✅ Keys are stored **locally** in encrypted config
- ✅ **No data** is sent to third parties except OpenRouter
- ✅ **Conversations** are not stored on external servers
- ✅ **Cache** is stored locally for privacy

## 🎆 Advanced Features

### 💾 Response Caching
DishDazzle automatically caches similar requests:
```json
"cache": {
  "enabled": true,
  "ttl_hours": 24,
  "max_size_mb": 50
}
```

### ⚛️ Thread Safety
- API calls run in background threads
- UI remains responsive during requests
- Multiple requests can be processed simultaneously

### 🔄 Automatic Retries
- Failed requests are automatically retried
- Exponential backoff for rate limiting
- Graceful error handling and user feedback

## 🌐 Alternative Providers

While DishDazzle is optimized for OpenRouter, you can modify the code to work with:

- **OpenAI Direct** (requires code changes)
- **Anthropic Claude** (via OpenRouter)
- **Google Gemini** (via OpenRouter)
- **Other providers** supported by OpenRouter

## 🔗 Useful Links

- 🌐 [OpenRouter Dashboard](https://openrouter.ai/dashboard)
- 📊 [OpenRouter Pricing](https://openrouter.ai/pricing)
- 📖 [OpenRouter Documentation](https://openrouter.ai/docs)
- 💬 [OpenRouter Discord](https://discord.gg/openrouter)
- 🐛 [Report Issues](https://github.com/yourusername/DishDazzle/issues)

## 🎁 Pro Tips

1. 🔄 **Start with DeepSeek** - it's faster and cheaper for most tasks
2. 🧠 **Use Llama for complex recipes** - better at understanding nuanced cooking techniques  
3. 💾 **Enable caching** - saves money on repeated questions
4. 📊 **Monitor your usage** - set alerts to avoid surprise bills
5. ⚡ **Keep prompts focused** - shorter questions = lower costs
6. 🔄 **Switch models based on task** - optimize for speed vs. quality

---

🎆 **Happy Cooking with AI!** 🎆

For additional help, check our [User Manual](user_manual.md) or [open an issue](https://github.com/yourusername/DishDazzle/issues).
