const Stripe = require('stripe')
const { jsonResponse } = require('./utils')

exports.handler = async function (event) {
  const stripeKey = process.env.STRIPE_SECRET_KEY
  const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET
  if (!stripeKey || !endpointSecret) {
    return jsonResponse(500, { error: 'STRIPE_SECRET_KEY or STRIPE_WEBHOOK_SECRET not configured' })
  }

  const stripe = new Stripe(stripeKey)
  const sig = event.headers['stripe-signature'] || event.headers['Stripe-Signature']
  let evt
  try {
    // Use raw body for signature verification
    const rawBody = event.body
    evt = stripe.webhooks.constructEvent(rawBody, sig, endpointSecret)
  } catch (err) {
    return jsonResponse(400, { error: 'Webhook signature verification failed', detail: err.message })
  }

  // Handle the event types you care about
  switch (evt.type) {
    case 'checkout.session.completed':
      // handle checkout session
      break
    case 'invoice.payment_succeeded':
      // handle invoice paid
      break
    default:
      break
  }

  return jsonResponse(200, { received: true })
}
