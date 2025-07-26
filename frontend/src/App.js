import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import ProductCard from "./components/ProductCard";
import Cart from "./components/Cart";
import { productsAPI, categoriesAPI } from "./services/api";
import { Toaster } from "./components/ui/sonner";
import { Button } from "./components/ui/button";
import { Badge } from "./components/ui/badge";
import { Filter } from "lucide-react";

const Home = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [sortBy, setSortBy] = useState('name');
  const [showFilters, setShowFilters] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Charger les catégories
  useEffect(() => {
    const loadCategories = async () => {
      try {
        const categoriesData = await categoriesAPI.getAll();
        setCategories(categoriesData);
      } catch (error) {
        console.error('Error loading categories:', error);
      }
    };
    
    loadCategories();
  }, []);

  // Charger les produits avec filtres
  useEffect(() => {
    const loadProducts = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        const filters = {
          category: selectedCategory,
          search: searchQuery,
          sort_by: sortBy
        };
        
        const productsData = await productsAPI.getAll(filters);
        setProducts(productsData);
      } catch (error) {
        console.error('Error loading products:', error);
        setError('Impossible de charger les produits');
      } finally {
        setIsLoading(false);
      }
    };

    loadProducts();
  }, [selectedCategory, searchQuery, sortBy]);

  const handleCategorySelect = (category) => {
    setSelectedCategory(category);
  };

  const handleSearchChange = (query) => {
    setSearchQuery(query);
  };

  const getCategoryName = (categoryId) => {
    if (!categoryId) return 'Tous les produits';
    const category = categories.find(cat => cat.id === categoryId);
    return category ? category.name : categoryId;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-purple-50">
      <Header
        onCategorySelect={handleCategorySelect}
        onSearchChange={handleSearchChange}
        onCartClick={() => setIsCartOpen(true)}
      />

      {/* Hero Section */}
      <section className="bg-gradient-to-r from-pink-500 via-purple-500 to-pink-400 text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-4 animate-fadeIn">
            Darling Boutique
          </h1>
          <p className="text-xl md:text-2xl mb-8 opacity-90">
            Découvrez notre collection d'accessoires tendance
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Badge className="bg-white/20 text-white border-white/30 px-4 py-2">
              🆓 Livraison gratuite dès 50,000 FCFA
            </Badge>
            <Badge className="bg-white/20 text-white border-white/30 px-4 py-2">
              💳 Paiement Mobile Money
            </Badge>
          </div>
        </div>
      </section>

      {/* Filters and Sort */}
      <section className="container mx-auto px-4 py-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <div className="flex items-center space-x-4">
            <h2 className="text-2xl font-bold text-gray-800">
              {getCategoryName(selectedCategory)}
            </h2>
            <Badge variant="secondary">
              {products.length} produit{products.length > 1 ? 's' : ''}
            </Badge>
          </div>

          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowFilters(!showFilters)}
              className="sm:hidden"
            >
              <Filter className="h-4 w-4 mr-2" />
              Filtres
            </Button>

            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 border border-gray-200 rounded-lg focus:border-pink-300 focus:ring-2 focus:ring-pink-100 transition-colors"
            >
              <option value="name">Trier par nom</option>
              <option value="price-asc">Prix croissant</option>
              <option value="price-desc">Prix décroissant</option>
              <option value="rating">Mieux notés</option>
            </select>
          </div>
        </div>

        {/* Mobile Filters */}
        {showFilters && (
          <div className="sm:hidden mb-6 p-4 bg-white rounded-lg border">
            <h3 className="font-semibold mb-3">Catégories</h3>
            <div className="space-y-2">
              <Button
                variant={selectedCategory === null ? "default" : "ghost"}
                size="sm"
                className="w-full justify-start"
                onClick={() => handleCategorySelect(null)}
              >
                Tous les produits
              </Button>
              {categories.map((category) => (
                <Button
                  key={category.id}
                  variant={selectedCategory === category.id ? "default" : "ghost"}
                  size="sm"
                  className="w-full justify-start"
                  onClick={() => handleCategorySelect(category.id)}
                >
                  {category.id === 'bijoux' ? '💎' : '🎧'} {category.name}
                </Button>
              ))}
            </div>
          </div>
        )}
      </section>

      {/* Products Grid */}
      <section className="container mx-auto px-4 pb-12">
        {isLoading ? (
          // Loading state
          <div className="text-center py-12">
            <div className="w-12 h-12 border-4 border-pink-200 border-t-pink-500 rounded-full animate-spin mx-auto mb-4"></div>
            <h3 className="text-xl font-semibold text-gray-600 mb-2">
              Chargement des produits...
            </h3>
          </div>
        ) : error ? (
          // Error state
          <div className="text-center py-12">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 flex items-center justify-center">
              <span className="text-2xl">⚠️</span>
            </div>
            <h3 className="text-xl font-semibold text-gray-600 mb-2">
              Erreur de chargement
            </h3>
            <p className="text-gray-500 mb-4">{error}</p>
            <Button
              onClick={() => window.location.reload()}
              variant="outline"
            >
              Réessayer
            </Button>
          </div>
        ) : products.length === 0 ? (
          // No products found
          <div className="text-center py-12">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-100 flex items-center justify-center">
              <span className="text-2xl">🔍</span>
            </div>
            <h3 className="text-xl font-semibold text-gray-600 mb-2">
              Aucun produit trouvé
            </h3>
            <p className="text-gray-500 mb-4">
              Essayez de modifier vos filtres ou votre recherche
            </p>
            <Button
              onClick={() => {
                setSelectedCategory(null);
                setSearchQuery('');
              }}
              variant="outline"
            >
              Réinitialiser les filtres
            </Button>
          </div>
        ) : (
          // Products grid
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4 bg-gradient-to-r from-pink-400 to-purple-400 bg-clip-text text-transparent">
                Darling Boutique
              </h3>
              <p className="text-gray-400">
                Votre destination pour les accessoires tendance et la technologie moderne.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Paiement</h4>
              <div className="space-y-2 text-gray-400">
                <p>📱 Moov Money</p>
                <p>💳 Airtel Money</p>
                <p>🚚 Livraison gratuite dès 50,000 FCFA</p>
              </div>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Contact</h4>
              <div className="space-y-2 text-gray-400">
                <p>📞 +225 XX XX XX XX XX</p>
                <p>📧 contact@darlingboutique.ci</p>
                <p>📍 Abidjan, Côte d'Ivoire</p>
              </div>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 Darling Boutique. Tous droits réservés.</p>
          </div>
        </div>
      </footer>

      {/* Cart */}
      <Cart isOpen={isCartOpen} onClose={() => setIsCartOpen(false)} />
      
      {/* Toaster pour les notifications */}
      <Toaster />
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;