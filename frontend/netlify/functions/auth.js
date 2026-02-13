const jwt = require('jsonwebtoken')
const bcrypt = require('bcryptjs')
const { jsonResponse, parseBody } = require('./utils')
const { Pool } = require('pg')

// Require JWT_SECRET
const SECRET = process.env.JWT_SECRET
if (!SECRET) {
  throw new Error('JWT_SECRET environment variable is required for auth function')
}

// If DATABASE_URL is provided, use Postgres for persistent users
const DATABASE_URL = process.env.DATABASE_URL
let pool = null
if (DATABASE_URL) {
  pool = new Pool({ connectionString: DATABASE_URL, ssl: { rejectUnauthorized: false } })
}

async function ensureUsersTable() {
  if (!pool) return
  await pool.query(`
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
    );
  `)
}

exports.handler = async function (event) {
  const body = parseBody(event)
  const { action } = event.queryStringParameters || {}

  if (pool) {
    await ensureUsersTable()
  }

  if (action === 'signup') {
    const { email, password } = body
    if (!email || !password) return jsonResponse(400, { error: 'email and password required' })

    // If using DB
    if (pool) {
      const hash = await bcrypt.hash(password, 10)
      try {
        const res = await pool.query('INSERT INTO users (email, password_hash) VALUES ($1, $2) RETURNING id, email', [email, hash])
        const user = res.rows[0]
        const token = jwt.sign({ sub: user.email, id: user.id }, SECRET, { expiresIn: '24h' })
        return jsonResponse(201, { token, user: { id: user.id, email: user.email } })
      } catch (err) {
        if (err.code === '23505') return jsonResponse(409, { error: 'user exists' })
        return jsonResponse(500, { error: err.message })
      }
    }

    // Fallback in-memory (for dev)
    if (!global.users) global.users = {}
    if (global.users[email]) return jsonResponse(409, { error: 'user exists' })
    const hash = await bcrypt.hash(password, 10)
    global.users[email] = { email, hash }
    const token = jwt.sign({ sub: email }, SECRET, { expiresIn: '24h' })
    return jsonResponse(201, { token, user: { email } })
  }

  if (action === 'login') {
    const { email, password } = body
    if (!email || !password) return jsonResponse(400, { error: 'email and password required' })

    if (pool) {
      try {
        const res = await pool.query('SELECT id, email, password_hash FROM users WHERE email = $1', [email])
        const user = res.rows[0]
        if (!user) return jsonResponse(401, { error: 'invalid credentials' })
        const ok = await bcrypt.compare(password, user.password_hash)
        if (!ok) return jsonResponse(401, { error: 'invalid credentials' })
        const token = jwt.sign({ sub: user.email, id: user.id }, SECRET, { expiresIn: '24h' })
        return jsonResponse(200, { token, user: { id: user.id, email: user.email } })
      } catch (err) {
        return jsonResponse(500, { error: err.message })
      }
    }

    // Fallback in-memory
    if (!global.users || !global.users[email]) return jsonResponse(401, { error: 'invalid credentials' })
    const ok = await bcrypt.compare(password, global.users[email].hash)
    if (!ok) return jsonResponse(401, { error: 'invalid credentials' })
    const token = jwt.sign({ sub: email }, SECRET, { expiresIn: '24h' })
    return jsonResponse(200, { token, user: { email } })
  }

  return jsonResponse(400, { error: 'invalid action' })
}
