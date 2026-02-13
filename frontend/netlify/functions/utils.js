const jsonResponse = (status, body) => ({
  statusCode: status,
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
})

const parseBody = (event) => {
  try {
    return event.body ? JSON.parse(event.body) : {}
  } catch (e) {
    return {}
  }
}

module.exports = { jsonResponse, parseBody }
