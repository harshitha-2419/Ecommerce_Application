import React, { useState } from 'react';
import { ShoppingCart } from 'lucide-react';
import { Product } from '../types';
import { useCart } from '../context/CartContext';

interface ProductCardProps {
  product: Product;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const { addToCart } = useCart();
  const [notification, setNotification] = useState('');

  const handleAddToCart = () => {
    addToCart(product.id);
    setNotification('Product added to cart!');
    setTimeout(() => {
      setNotification('');
    }, 3000); // Hide notification after 3 seconds
  };

  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden transform hover:scale-105 transition-all duration-300">
      <img
        src={product.imageUrl}
        alt={product.name}
        className="w-full h-48 object-cover object-center"
      />
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-800 truncate">{product.name}</h3>
        <div className="flex items-center mt-2">
          <span className="text-xl font-bold text-gray-900">₹{product.price.toFixed(2)}</span>
          {product.discount && (
            <span className="ml-2 text-sm text-red-600 font-medium">-{product.discount}% OFF</span>
          )}
        </div>
        <p className="mt-2 text-gray-600 text-sm line-clamp-2">{product.description}</p>
        <button
          onClick={handleAddToCart}
          className="mt-4 w-full bg-blue-600 text-white py-2 px-4 rounded-full hover:bg-blue-700 flex items-center justify-center transition-colors"
        >
          <ShoppingCart className="w-5 h-5 mr-2" />
          Add to Cart
        </button>
        {notification && <p className="mt-2 text-green-600">{notification}</p>}
      </div>
    </div>
  );
};