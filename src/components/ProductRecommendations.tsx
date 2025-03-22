import React from 'react';
import { ProductCard } from './ProductCard';
import { Product } from '../types';

interface ProductRecommendationsProps {
  title: string;
  products: Product[];
}

export const ProductRecommendations: React.FC<ProductRecommendationsProps> = ({
  title,
  products,
}) => {
  if (products.length === 0) return null;

  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">{title}</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {products.map(product => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
};