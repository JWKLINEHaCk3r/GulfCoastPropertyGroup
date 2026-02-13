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

async function ensureRefreshTable() {
  if (!pool) return
  await pool.query(`
    CREATE TABLE IF NOT EXISTS refresh_tokens (
      id SERIAL PRIMARY KEY,
      user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
      token TEXT NOT NULL,
      expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
      created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
    );
  `)
}

async function storeRefreshToken(userId, token, expiresAt) {
  if (!pool) return
  return pool.query('INSERT INTO refresh_tokens (user_id, token, expires_at) VALUES ($1, $2, $3)', [userId, token, expiresAt])
}

async function verifyRefreshToken(token) {
  if (!pool) return null
  const res = await pool.query('SELECT user_id FROM refresh_tokens WHERE token = $1 AND expires_at > now()', [token])
  return res.rows[0] ? res.rows[0].user_id : null
}

async function revokeRefreshToken(token) {
  if (!pool) return
  await pool.query('DELETE FROM refresh_tokens WHERE token = $1', [token])
}

exports.handler = async function (event) {
  const body = parseBody(event)
  const { action } = event.queryStringParameters || {}

  if (pool) {
    await ensureUsersTable()
    await ensureRefreshTable()
    // ensure password_resets table
    await pool.query(`
      CREATE TABLE IF NOT EXISTS password_resets (
        id SERIAL PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        token TEXT NOT NULL,
        expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
      );
    `)
  }

  // Signup
  if (action === 'signup') {
    const { email, password } = body
    if (!email || !password) return jsonResponse(400, { error: 'email and password required' })

    if (pool) {
      const hash = await bcrypt.hash(password, 10)
      try {
        const res = await pool.query('INSERT INTO users (email, password_hash) VALUES ($1, $2) RETURNING id, email', [email, hash])
        const user = res.rows[0]
        const token = jwt.sign({ sub: user.email, id: user.id }, SECRET, { expiresIn: '24h' })
        const refreshToken = require('crypto').randomBytes(48).toString('hex')
        const expiresAt = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
        await storeRefreshToken(user.id, refreshToken, expiresAt)
        return jsonResponse(201, { token, refresh_token: refreshToken, user: { id: user.id, email: user.email } })
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

  // Login
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
        const refreshToken = require('crypto').randomBytes(48).toString('hex')
        const expiresAt = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
        await storeRefreshToken(user.id, refreshToken, expiresAt)
        return jsonResponse(200, { token, refresh_token: refreshToken, user: { id: user.id, email: user.email } })
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

  // Refresh access token
  if (action === 'refresh') {
    const { refresh_token } = body
    if (!refresh_token) return jsonResponse(400, { error: 'refresh_token required' })
    if (!pool) return jsonResponse(400, { error: 'DATABASE_URL required' })
    const userId = await verifyRefreshToken(refresh_token)
    if (!userId) return jsonResponse(401, { error: 'invalid refresh token' })
    const userRes = await pool.query('SELECT id, email FROM users WHERE id = $1', [userId])
    const user = userRes.rows[0]
    const token = jwt.sign({ sub: user.email, id: user.id }, SECRET, { expiresIn: '24h' })
    return jsonResponse(200, { token })
  }

  // Logout (revoke refresh token)
  if (action === 'logout') {
    const { refresh_token } = body
    if (refresh_token) await revokeRefreshToken(refresh_token)
    return jsonResponse(200, { message: 'logged out' })
  }

  // Request password reset
  if (action === 'request_reset') {
    const { email } = body
    if (!email) return jsonResponse(400, { error: 'email required' })
    if (!pool) return jsonResponse(400, { error: 'DATABASE_URL required for password reset' })
    const token = require('crypto').randomBytes(24).toString('hex')
    const expiresAt = new Date(Date.now() + 60 * 60 * 1000)
    await pool.query('INSERT INTO password_resets (email, token, expires_at) VALUES ($1, $2, $3) ON CONFLICT (email) DO UPDATE SET token = EXCLUDED.token, expires_at = EXCLUDED.expires_at', [email, token, expiresAt])
    const SENDGRID_KEY = process.env.SENDGRID_API_KEY
    if (SENDGRID_KEY) {
      const sgMail = require('@sendgrid/mail')
      sgMail.setApiKey(SENDGRID_KEY)
      const resetUrl = `${process.env.FRONTEND_URL || ''}/reset-password?token=${token}`
      const msg = {
        to: email,
        from: process.env.SENDGRID_FROM || 'noreply@example.com',
        subject: 'Password reset',
        text: `Reset your password: ${resetUrl}`,
        html: `<p>Reset your password: <a href="${resetUrl}">${resetUrl}</a></p>`
      }
      try { await sgMail.send(msg) } catch (err) { /* ignore send errors for now */ }
    }
    return jsonResponse(200, { message: 'password reset requested' })
  }

  // Confirm password reset
  if (action === 'confirm_reset') {
    const { token, new_password } = body
    if (!token || !new_password) return jsonResponse(400, { error: 'token and new_password required' })
    if (!pool) return jsonResponse(400, { error: 'DATABASE_URL required' })
    const res = await pool.query('SELECT email, expires_at FROM password_resets WHERE token = $1', [token])
    const row = res.rows[0]
    if (!row || new Date(row.expires_at) < new Date()) return jsonResponse(400, { error: 'invalid or expired token' })
    const hash = await bcrypt.hash(new_password, 10)
    await pool.query('UPDATE users SET password_hash = $1 WHERE email = $2', [hash, row.email])
    await pool.query('DELETE FROM password_resets WHERE email = $1', [row.email])
    return jsonResponse(200, { message: 'password reset successful' })
  }

  return jsonResponse(400, { error: 'invalid action' })
}
