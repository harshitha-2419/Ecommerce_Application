import React, { useMemo } from 'react';
import { Minus, Plus, Trash2 } from 'lucide-react';
import { useCart } from '../context/CartContext';
import { ProductRecommendations } from '../components/ProductRecommendations';
import { getProductById, getRelatedProducts } from '../data/products';

export const CartPage: React.FC = () => {
  const { items, updateQuantity, removeFromCart } = useCart();

  const cartDetails = useMemo(() => {
    return items.map(item => {
      const product = getProductById(item.productId);
      if (!product) return null;

      const totalPrice = product.price * item.quantity;
      return { ...item, product, totalPrice };
    }).filter(Boolean);
  }, [items]);

  const totalAmount = useMemo(() => {
    return cartDetails.reduce((sum, item) => sum + (item?.totalPrice || 0), 0);
  }, [cartDetails]);

  const relatedProducts = useMemo(() => {
    if (cartDetails.length === 0) return [];
    const firstProduct = cartDetails[0]?.product;
    if (!firstProduct) return [];
    return getRelatedProducts(firstProduct.category, firstProduct.id);
  }, [cartDetails]);

  if (cartDetails.length === 0) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Your Cart is Empty</h2>
          <p className="text-gray-600">Start shopping to add items to your cart!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-8">Shopping Cart</h2>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          {cartDetails.map(item => {
            if (!item?.product) return null;
            return (
              <div
                key={item.productId}
                className="flex items-center border-b border-gray-200 py-4"
              >
                <img
                  src={item.product.imageUrl}
                  alt={item.product.name}
                  className="w-24 h-24 object-cover rounded"
                />
                <div className="flex-1 ml-4">
                  <h3 className="text-lg font-semibold">{item.product.name}</h3>
                  <p className="text-gray-600">₹{item.product.price.toFixed(2)}</p>
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => updateQuantity(item.productId, item.quantity - 1)}
                    className="p-1 rounded-full hover:bg-gray-100"
                  >
                    <Minus className="w-4 h-4" />
                  </button>
                  <span className="w-8 text-center">{item.quantity}</span>
                  <button
                    onClick={() => updateQuantity(item.productId, item.quantity + 1)}
                    className="p-1 rounded-full hover:bg-gray-100"
                  >
                    <Plus className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => removeFromCart(item.productId)}
                    className="p-1 rounded-full hover:bg-gray-100 ml-4"
                  >
                    <Trash2 className="w-4 h-4 text-red-500" />
                  </button>
                </div>
                <div className="ml-8 text-right">
                  <p className="font-semibold">₹{item.totalPrice.toFixed(2)}</p>
                </div>
              </div>
            );
          })}
        </div>

        <div className="lg:col-span-1">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-4">Order Summary</h3>
            <div className="flex justify-between mb-4">
              <span>Subtotal</span>
              <span>₹{totalAmount.toFixed(2)}</span>
            </div>
            <div className="border-t border-gray-200 pt-4 mt-4">
              <div className="flex justify-between font-semibold text-lg">
                <span>Total</span>
                <span>₹{totalAmount.toFixed(2)}</span>
              </div>
            </div>
            <button className="w-full mt-6 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700">
              Proceed to Checkout
            </button>
          </div>
        </div>
      </div>

      <ProductRecommendations
        title="You Might Also Like"
        products={relatedProducts}
      />
    </div>
  );
};