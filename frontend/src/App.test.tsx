import { render, screen } from '@testing-library/react';
import App from './App';

// Mock axios to avoid network calls in tests
jest.mock('axios', () => ({
  get: jest.fn(() => Promise.resolve({ data: [] })),
  post: jest.fn(() => Promise.resolve({ data: {} })),
  delete: jest.fn(() => Promise.resolve({ data: {} }))
}));

test('renders app title', () => {
  render(<App />);
  const titleElement = screen.getByText(/DevOps Portfolio/i);
  expect(titleElement).toBeInTheDocument();
});

test('renders products section', () => {
  render(<App />);
  const productsElement = screen.getByText(/Products/i);
  expect(productsElement).toBeInTheDocument();
});

test('renders shopping cart section', () => {
  render(<App />);
  const cartElement = screen.getByText(/Shopping Cart/i);
  expect(cartElement).toBeInTheDocument();
}); 