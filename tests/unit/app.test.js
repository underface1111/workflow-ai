const request = require('supertest');
const app = require('../../src/app');
const { resetForTests } = require('../../src/store');

describe('workflow-ai-poc API', () => {
  beforeEach(() => {
    resetForTests();
  });

  describe('GET /health', () => {
    it('returns ok', async () => {
      const res = await request(app).get('/health');
      expect(res.status).toBe(200);
      expect(res.body.status).toBe('ok');
    });
  });

  describe('POST /auth/login', () => {
    it('rejects missing credentials', async () => {
      const res = await request(app).post('/auth/login').send({});
      expect(res.status).toBe(400);
    });

    it('rejects invalid credentials', async () => {
      const res = await request(app)
        .post('/auth/login')
        .send({ email: 'demo@bankco.local', password: 'wrong' });
      expect(res.status).toBe(401);
    });

    it('returns token for valid user', async () => {
      const res = await request(app)
        .post('/auth/login')
        .send({ email: 'demo@bankco.local', password: 'demo123' });
      expect(res.status).toBe(200);
      expect(res.body.token).toBeDefined();
      expect(res.body.userId).toBe('user-1');
    });
  });

  describe('steel thread: login → catalog → cart → checkout', () => {
    it('completes happy path', async () => {
      const login = await request(app)
        .post('/auth/login')
        .send({ email: 'demo@bankco.local', password: 'demo123' });
      const token = login.body.token;

      const catalogRes = await request(app)
        .get('/catalog')
        .set('Authorization', `Bearer ${token}`);
      expect(catalogRes.status).toBe(200);
      expect(catalogRes.body.items.length).toBeGreaterThan(0);

      const add = await request(app)
        .post('/cart/items')
        .set('Authorization', `Bearer ${token}`)
        .send({ skuId: 'sku-2', quantity: 1 });
      expect(add.status).toBe(201);

      const checkout = await request(app)
        .post('/checkout')
        .set('Authorization', `Bearer ${token}`);
      expect(checkout.status).toBe(200);
      expect(checkout.body.status).toBe('confirmed');
      expect(checkout.body.orderId).toMatch(/^ord-/);
    });

    it('requires auth for catalog', async () => {
      const res = await request(app).get('/catalog');
      expect(res.status).toBe(401);
    });

    it('rejects empty cart checkout', async () => {
      const login = await request(app)
        .post('/auth/login')
        .send({ email: 'demo@bankco.local', password: 'demo123' });
      const res = await request(app)
        .post('/checkout')
        .set('Authorization', `Bearer ${login.body.token}`);
      expect(res.status).toBe(400);
    });
  });
});
