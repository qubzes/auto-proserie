# Getting Your Google Gemini API Key

## Quick Steps

1. **Visit Google AI Studio**
   - Go to: https://makersuite.google.com/app/apikey
   - Or: https://aistudio.google.com/app/apikey

2. **Sign in with Google Account**
   - Use any Google account (Gmail, Workspace, etc.)

3. **Create API Key**
   - Click "Create API Key" button
   - Select "Create API key in new project" (or use existing project)
   - Copy the generated key (starts with `AIza...`)

4. **Add to .env file**
   ```bash
   GOOGLE_API_KEY=AIzaSyC...your-key-here
   ```

## Why Gemini 2.0 Flash?

✅ **Extremely Cost-Effective**
- ~$0.01 per W2 form (vs $0.05-0.10 for GPT-4/Claude)
- 1000 W2s = ~$10 (vs $50-100)

✅ **Fast Response Times**
- Optimized for speed
- Low latency

✅ **High Quality**
- Excellent at understanding structured data
- Strong JSON output formatting
- Great for form mapping tasks

✅ **Generous Free Tier**
- 1,500 requests per day (free)
- Perfect for testing and development

## API Limits

### Free Tier
- 15 RPM (requests per minute)
- 1 million TPM (tokens per minute)
- 1,500 RPD (requests per day)

### For High Volume
- Can request increased quotas
- Pay-as-you-go pricing
- Very affordable rates

## Troubleshooting

### "API key not valid"
- Make sure you copied the entire key
- Check for extra spaces
- Key should start with `AIza`

### "Quota exceeded"
- Free tier: 1,500 requests/day
- Wait 24 hours or upgrade
- Can process ~100 W2s per day on free tier

### "API not enabled"
- Go to Google Cloud Console
- Enable "Generative Language API"
- https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com

## Security

- ✅ Keep your API key in `.env` (git-ignored)
- ✅ Never commit API keys to version control
- ✅ Regenerate key if accidentally exposed
- ✅ Use separate keys for dev/production

## More Information

- API Documentation: https://ai.google.dev/docs
- Pricing: https://ai.google.dev/pricing
- Quotas: https://ai.google.dev/docs/quota
