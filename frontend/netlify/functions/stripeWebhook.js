const Stripe = require('stripe')
const { jsonResponse } = require('./utils')

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || '')
const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET || ''

exports.handler = async function (event) {
  const sig = event.headers['stripe-signature'] || event.headers['Stripe-Signature']
  let evt
  try {
    evt = stripe.webhooks.constructEvent(event.body, sig, endpointSecret)
  } catch (err) {
    return jsonResponse(400, { error: 'Webhook signature verification failed' })
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
