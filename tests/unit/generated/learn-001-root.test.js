// AUTO-GENERATED — ticket learn-001
// REVIEW REQUIRED before merge (Bước B)

const request = require('supertest');
const app = require('../../../src/app');

describe('GET / (LEARN-001)', () => {
  it('returns service info without auth', async () => {
    const res = await request(app).get('/');
    expect(res.status).toBe(200);
    expect(res.body.message).toBe('workflow-ai-poc');
    expect(res.body.docs).toBe('/health');
  });
});
