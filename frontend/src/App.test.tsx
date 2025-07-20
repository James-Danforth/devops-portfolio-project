import { render, screen } from '@testing-library/react';
import App from './App';

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