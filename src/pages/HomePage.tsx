import React, { useState, useMemo } from 'react';
import { SearchBar } from '../components/SearchBar';
import { ProductCard } from '../components/ProductCard';
import { ProductRecommendations } from '../components/ProductRecommendations';
import { products, getTrendingProducts, getDiscountedProducts } from '../data/products';

export const HomePage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const filteredProducts = useMemo(() => {
    if (!searchQuery) return products;
    
    const query = searchQuery.toLowerCase();
    return products.filter(
      product =>
        product.name.toLowerCase().includes(query) ||
        product.description.toLowerCase().includes(query)
    );
  }, [searchQuery]);

  const trendingProducts = useMemo(() => getTrendingProducts(), []);
  const discountedProducts = useMemo(() => getDiscountedProducts(), []);

  return (
    <div className="container mx-auto px-4 py-8">
      <SearchBar onSearch={setSearchQuery} />

      {filteredProducts.length === 0 ? (
        <div className="text-center mt-8">
          <p className="text-gray-600 text-lg">No products found matching your search.</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
            {filteredProducts.map(product => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>

          {!searchQuery && (
            <>
              <ProductRecommendations
                title="Trending Products"
                products={trendingProducts}
              />
              <ProductRecommendations
                title="Special Offers"
                products={discountedProducts}
              />
            </>
          )}
        </>
      )}
    </div>
  );
};