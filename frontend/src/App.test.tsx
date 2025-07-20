import { render, screen, waitFor } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import App from './App';

// Mock axios to avoid network calls in tests
const mockAxios = {
  get: jest.fn(),
  post: jest.fn(),
  delete: jest.fn()
};

jest.mock('axios', () => mockAxios);

describe('App Component', () => {
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
    
    // Mock successful API responses
    mockAxios.get.mockResolvedValue({ data: [] });
  });

  test('renders loading state initially', async () => {
    render(<App />);
    const loadingElement = screen.getByText(/Loading products/i);
    expect(loadingElement).toBeInTheDocument();
  });

  test('renders app title after loading', async () => {
    render(<App />);
    
    await waitFor(() => {
      const titleElement = screen.getByText(/DevOps Portfolio/i);
      expect(titleElement).toBeInTheDocument();
    });
  });

  test('renders products section after loading', async () => {
    render(<App />);
    
    await waitFor(() => {
      const productsElement = screen.getByText(/Products/i);
      expect(productsElement).toBeInTheDocument();
    });
  });

  test('renders shopping cart section after loading', async () => {
    render(<App />);
    
    await waitFor(() => {
      const cartElement = screen.getByText(/Shopping Cart/i);
      expect(cartElement).toBeInTheDocument();
    });
  });
}); 