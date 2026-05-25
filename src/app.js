const express = require('express');
const {
  users,
  catalog,
  createSession,
  getSession,
  getOrCreateCart,
} = require('./store');

const app = express();
app.use(express.json());

function requireAuth(req, res, next) {
  const header = req.headers.authorization;
  const token = header?.startsWith('Bearer ') ? header.slice(7) : null;
  const session = token ? getSession(token) : null;
  if (!session) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  req.userId = session.userId;
  req.token = token;
  return next();
}

app.get('/', (_req, res) => {
  res.json({ message: 'workflow-ai-poc', docs: '/health' });
});

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'workflow-ai-poc' });
});

app.post('/auth/login', (req, res) => {
  const { email, password } = req.body ?? {};
  if (!email || !password) {
    return res.status(400).json({ error: 'email and password required' });
  }
  const user = users.get(email);
  if (!user || user.password !== password) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  const token = createSession(user.id);
  return res.json({ token, userId: user.id, name: user.name });
});

app.get('/catalog', requireAuth, (_req, res) => {
  res.json({ items: catalog });
});

app.get('/cart', requireAuth, (req, res) => {
  const cart = getOrCreateCart(req.userId);
  res.json(cart);
});

app.post('/cart/items', requireAuth, (req, res) => {
  const { skuId, quantity = 1 } = req.body ?? {};
  const product = catalog.find((p) => p.id === skuId);
  if (!product) {
    return res.status(404).json({ error: 'Product not found' });
  }
  const cart = getOrCreateCart(req.userId);
  const existing = cart.items.find((i) => i.skuId === skuId);
  if (existing) {
    existing.quantity += quantity;
  } else {
    cart.items.push({ skuId, name: product.name, quantity, price: product.price });
  }
  res.status(201).json(cart);
});

app.post('/checkout', requireAuth, (req, res) => {
  const cart = getOrCreateCart(req.userId);
  if (cart.items.length === 0) {
    return res.status(400).json({ error: 'Cart is empty' });
  }
  const total = cart.items.reduce((sum, i) => sum + i.price * i.quantity, 0);
  const orderId = `ord-${Date.now()}`;
  cart.status = 'checked_out';
  cart.orderId = orderId;
  return res.json({
    orderId,
    status: 'confirmed',
    total,
    itemCount: cart.items.length,
  });
});

module.exports = app;
