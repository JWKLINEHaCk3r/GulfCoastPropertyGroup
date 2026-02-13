const fetch = require('node-fetch')
const { jsonResponse, parseBody } = require('./utils')

// Example function that orchestrates a simple multi-agent workflow by calling
// external AI endpoints (placeholder). Replace with real agent orchestration.
exports.handler = async function (event) {
  const body = parseBody(event)
  const { propertyAddress } = body
  if (!propertyAddress) return jsonResponse(400, { error: 'propertyAddress required' })

  try {
    // Example: call external AI service to qualify lead
    const qa = await fetch(process.env.AI_QUALIFY_URL || 'https://example.com/qualify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ address: propertyAddress }),
    })
    const qualify = await qa.json()

    // Example: call rehab estimator
    const re = await fetch(process.env.AI_REHAB_URL || 'https://example.com/rehab', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ address: propertyAddress }),
    })
    const rehab = await re.json()

    return jsonResponse(200, { qualify, rehab })
  } catch (err) {
    return jsonResponse(500, { error: err.message })
  }
}
