export default {
  async fetch(request, env) {
    // Only allow POST requests
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    try {
      const requestData = await request.json();
      const apiKey = env.CLOUDFLARE_API_KEY || 'PwfJor56sIf_CrWSk09eOT3Np9fla4xU8WSrWYrz';
      const accountId = env.CLOUDFLARE_ACCOUNT_ID || '86e2b8822cebf8584cf942edb3103fae';
      const model = env.CLOUDFLARE_AI_MODEL || '@cf/meta/llama-2-7b-chat-int8';

      const aiResponse = await fetch(
        `https://api.cloudflare.com/client/v4/accounts/${accountId}/ai/run/${model}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
          },
          body: JSON.stringify(requestData)
        }
      );

      const data = await aiResponse.json();
      return new Response(JSON.stringify(data), {
        headers: { 'Content-Type': 'application/json' }
      });
    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  },
}; 