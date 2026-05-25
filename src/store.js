/** In-memory store for POC — not for production. */

const users = new Map([
  ['demo@bankco.local', { password: 'demo123', id: 'user-1', name: 'Demo User' }],
]);

const catalog = [
  { id: 'sku-1', name: 'Savings Account', price: 0 },
  { id: 'sku-2', name: 'Debit Card', price: 5 },
];

const sessions = new Map();
const carts = new Map();

function createSession(userId) {
  const token = `sess-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
  sessions.set(token, { userId, createdAt: Date.now() });
  return token;
}

function getSession(token) {
  return sessions.get(token) ?? null;
}

function getOrCreateCart(userId) {
  if (!carts.has(userId)) {
    carts.set(userId, { items: [], status: 'open' });
  }
  return carts.get(userId);
}

function resetForTests() {
  sessions.clear();
  carts.clear();
}

module.exports = {
  users,
  catalog,
  sessions,
  carts,
  createSession,
  getSession,
  getOrCreateCart,
  resetForTests,
};
