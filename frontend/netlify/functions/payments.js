const Stripe = require('stripe')
const { jsonResponse, parseBody } = require('./utils')

exports.handler = async function (event) {
  const stripeKey = process.env.STRIPE_SECRET_KEY
  if (!stripeKey) {
    return jsonResponse(500, { error: 'STRIPE_SECRET_KEY not configured in environment' })
  }

  const stripe = new Stripe(stripeKey)
  const body = parseBody(event)
  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'subscription',
      line_items: body.items || [],
      success_url: body.success_url || `${process.env.FRONTEND_URL || ''}/success`,
      cancel_url: body.cancel_url || `${process.env.FRONTEND_URL || ''}/cancel`,
      client_reference_id: body.client_reference_id,
    })
    return jsonResponse(200, { sessionId: session.id, url: session.url })
  } catch (err) {
    return jsonResponse(500, { error: err.message })
  }
}
