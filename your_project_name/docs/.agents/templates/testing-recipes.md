# Testing Recipes

**Purpose**: Copy-pasteable setups and patterns for your project's testing infrastructure.

---

## 1. JavaScript / TypeScript (Vitest/Jest)

### `package.json` Scripts

```json
{
  "scripts": {
    "test": "vitest run --reporter=dot --bail",
    "test:verbose": "vitest run",
    "test:watch": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage"
  }
}
```

### `vitest.config.ts`

```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'happy-dom',
    setupFiles: ['./src/test/setup.ts'],
  },
});
```

### React Component Pattern

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import App from './App';

it('should display content when loaded', async () => {
  render(<App />);
  await waitFor(() => {
    expect(screen.getByText('Expected Title')).toBeInTheDocument();
  });
});
```

---

## 2. Python (Pytest)

### CLI Commands

```bash
pytest --tb=short -x         # Agent-optimized run
pytest --cov=src             # With coverage
```

### Flask / FastAPI Pattern

```python
import pytest
from my_app import create_app

@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
```

---

## 3. Playwright (E2E)

### Basic Test

```typescript
import { test, expect } from '@playwright/test';

test('user can complete main flow', async ({ page }) => {
  await page.goto('/');
  await page.click('[data-testid="start-button"]');
  await expect(page.locator('[data-testid="status"]')).toContainText('Complete');
});
```
