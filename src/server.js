const app = require('./app');

const PORT = Number(process.env.PORT) || 3000;

if (require.main === module) {
  app.listen(PORT, () => {
    // eslint-disable-next-line no-console
    console.log(`workflow-ai-poc listening on http://localhost:${PORT}`);
  });
}

module.exports = { app, PORT };
