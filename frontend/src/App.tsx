import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  stock: number;
  category: string;
}

interface CartItem {
  id: number;
  product_id: number;
  quantity: number;
  product: Product;
}

function App() {
  const [products, setProducts] = useState<Product[]>([]);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  useEffect(() => {
    fetchProducts();
    fetchCart();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/products`);
      setProducts(response.data);
    } catch (err) {
      setError('Failed to fetch products');
      console.error('Error fetching products:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchCart = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/cart/user123`);
      setCart(response.data);
    } catch (err) {
      console.error('Error fetching cart:', err);
    }
  };

  const addToCart = async (productId: number) => {
    try {
      await axios.post(`${API_BASE_URL}/cart`, {
        user_id: 'user123',
        product_id: productId,
        quantity: 1
      });
      setSuccess('Product added to cart!');
      fetchCart();
      fetchProducts(); // Refresh products to update stock levels
      setTimeout(() => setSuccess(null), 3000);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to add product to cart');
      console.error('Error adding to cart:', err);
    }
  };

  const removeFromCart = async (cartId: number) => {
    try {
      await axios.delete(`${API_BASE_URL}/cart/${cartId}`);
      setSuccess('Product removed from cart!');
      fetchCart();
      fetchProducts(); // Refresh products to update stock levels
      setTimeout(() => setSuccess(null), 3000);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to remove product from cart');
      console.error('Error removing from cart:', err);
    }
  };

  const processPurchase = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/purchase`, {
        user_id: 'user123'
      });
      setSuccess(response.data.message);
      setCart([]); // Clear cart immediately
      fetchProducts(); // Refresh products to update stock levels
      setTimeout(() => setSuccess(null), 5000);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to process purchase');
      console.error('Error processing purchase:', err);
    }
  };

  const resetMarket = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/reset-market`);
      setSuccess(response.data.message);
      fetchProducts(); // Refresh products
      setTimeout(() => setSuccess(null), 5000);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to reset market');
      console.error('Error resetting market:', err);
    }
  };

  const getTotalPrice = () => {
    return cart.reduce((total, item) => total + (item.product.price * item.quantity), 0);
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading products...</div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="header">
        <div className="container">
          <h1>DevOps Portfolio - E-commerce Store</h1>
          <p>Built with React, Flask, Docker, Kubernetes & CI/CD</p>
          <button 
            className="btn" 
            onClick={resetMarket}
            style={{ marginTop: '10px', backgroundColor: '#dc3545' }}
          >
            Reset Market
          </button>
        </div>
      </header>

      <div className="container">
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}

        <section>
          <h2>Products</h2>
          <div className="product-grid">
            {products.map((product) => (
              <div key={product.id} className="product-card">
                <h3>{product.name}</h3>
                <p>{product.description}</p>
                <div className="price">${product.price.toFixed(2)}</div>
                <p style={{ 
                  color: product.stock === 0 ? '#dc3545' : product.stock < 5 ? '#ffc107' : '#28a745',
                  fontWeight: 'bold'
                }}>
                  Stock: {product.stock}
                  {product.stock === 0 && ' (Out of Stock)'}
                  {product.stock > 0 && product.stock < 5 && ' (Low Stock)'}
                </p>
                <button 
                  className="btn" 
                  onClick={() => addToCart(product.id)}
                  disabled={product.stock === 0}
                  style={{
                    backgroundColor: product.stock === 0 ? '#6c757d' : '#007bff',
                    cursor: product.stock === 0 ? 'not-allowed' : 'pointer'
                  }}
                >
                  {product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
                </button>
              </div>
            ))}
          </div>
        </section>

        <section className="cart-section">
          <h2>Shopping Cart</h2>
          {cart.length === 0 ? (
            <p>Your cart is empty</p>
          ) : (
            <>
              {cart.map((item) => (
                <div key={item.id} className="cart-item">
                  <div>
                    <h4>{item.product.name}</h4>
                    <p>Quantity: {item.quantity}</p>
                    <p>Price: ${item.product.price.toFixed(2)}</p>
                  </div>
                  <button 
                    className="btn" 
                    onClick={() => removeFromCart(item.id)}
                  >
                    Remove
                  </button>
                </div>
              ))}
              <div style={{ marginTop: '1rem', textAlign: 'right' }}>
                <h3>Total: ${getTotalPrice().toFixed(2)}</h3>
                <button className="btn" onClick={processPurchase}>
                  Purchase
                </button>
              </div>
            </>
          )}
        </section>
      </div>
    </div>
  );
}

export default App; 