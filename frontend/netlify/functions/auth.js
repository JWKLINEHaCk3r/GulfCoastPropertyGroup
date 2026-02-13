const jwt = require('jsonwebtoken')
const bcrypt = require('bcryptjs')
const { jsonResponse, parseBody } = require('./utils')

// NOTE: This is a lightweight example. For production, persist users in a DB.
const SECRET = process.env.JWT_SECRET
if (!SECRET) {
  // Fail fast to avoid insecure default secrets in production
  throw new Error('JWT_SECRET environment variable is required for auth function')
}

// Simple in-memory "users" for example purposes only
const users = {}

exports.handler = async function (event) {
  const body = parseBody(event)
  const { action } = event.queryStringParameters || {}

  if (action === 'signup') {
    const { email, password } = body
    if (!email || !password) return jsonResponse(400, { error: 'email and password required' })
    if (users[email]) return jsonResponse(409, { error: 'user exists' })
    const hash = await bcrypt.hash(password, 10)
    users[email] = { email, hash }
    const token = jwt.sign({ sub: email }, SECRET, { expiresIn: '24h' })
    return jsonResponse(201, { token, user: { email } })
  }

  if (action === 'login') {
    const { email, password } = body
    const user = users[email]
    if (!user) return jsonResponse(401, { error: 'invalid credentials' })
    const ok = await bcrypt.compare(password, user.hash)
    if (!ok) return jsonResponse(401, { error: 'invalid credentials' })
    const token = jwt.sign({ sub: email }, SECRET, { expiresIn: '24h' })
    return jsonResponse(200, { token, user: { email } })
  }

  return jsonResponse(400, { error: 'invalid action' })
}
