// AUTO-GENERATED — ticket learn-002
// REVIEW REQUIRED before merge (Bước B)

const request = require('supertest');
const app = require('../../../src/app');

describe('GET /health (LEARN-002)', () => {
  it('returns ok status without auth', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
    expect(res.body.service).toBe('workflow-ai-poc');
  });
});
