import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';

export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m', target: 50 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
  },
};

export default function steelThread() {
  const loginRes = http.post(
    `${BASE_URL}/auth/login`,
    JSON.stringify({ email: 'demo@bankco.local', password: 'demo123' }),
    { headers: { 'Content-Type': 'application/json' } },
  );
  check(loginRes, { 'login 200': (r) => r.status === 200 });
  const token = loginRes.json('token');

  const headers = {
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json',
  };

  const catalogRes = http.get(`${BASE_URL}/catalog`, { headers });
  check(catalogRes, { 'catalog 200': (r) => r.status === 200 });

  const addRes = http.post(
    `${BASE_URL}/cart/items`,
    JSON.stringify({ skuId: 'sku-2', quantity: 1 }),
    { headers },
  );
  check(addRes, { 'add to cart 201': (r) => r.status === 201 });

  const checkoutRes = http.post(`${BASE_URL}/checkout`, null, { headers });
  check(checkoutRes, {
    'checkout confirmed': (r) => r.status === 200 && r.json('status') === 'confirmed',
  });

  sleep(1);
}
