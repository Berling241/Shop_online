import React, { useState } from 'react';
import { Heart, ShoppingCart, Star } from 'lucide-react';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Card, CardContent, CardFooter } from './ui/card';
import { cartAPI, formatPrice } from '../services/api';
import { useToast } from '../hooks/use-toast';

const ProductCard = ({ product }) => {
  const [isLiked, setIsLiked] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleAddToCart = async () => {
    setIsLoading(true);
    
    try {
      await cartAPI.addItem(product.id, 1);
      
      // Dispatch custom event pour mettre à jour le compteur
      window.dispatchEvent(new CustomEvent('cartUpdated'));
      
      toast({
        title: "Produit ajouté !",
        description: `${product.name} a été ajouté à votre panier`,
        duration: 2000,
      });
      
    } catch (error) {
      console.error('Error adding to cart:', error);
      toast({
        title: "Erreur",
        description: "Impossible d'ajouter le produit au panier",
        variant: "destructive",
        duration: 3000,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getCategoryColor = (category) => {
    return category === 'bijoux' 
      ? 'bg-gradient-to-r from-pink-100 to-purple-100 text-pink-700'
      : 'bg-gradient-to-r from-blue-100 to-purple-100 text-blue-700';
  };

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`h-3 w-3 ${
          i < Math.floor(rating) 
            ? 'fill-yellow-400 text-yellow-400' 
            : 'text-gray-300'
        }`}
      />
    ));
  };

  return (
    <Card className="group overflow-hidden transition-all duration-300 hover:shadow-xl hover:-translate-y-1 border-0 bg-white/80 backdrop-blur-sm">
      <div className="relative overflow-hidden">
        <img
          src={product.image}
          alt={product.name}
          className="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-110"
        />
        
        {/* Overlay au hover */}
        <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        
        {/* Badge de catégorie */}
        <Badge className={`absolute top-3 left-3 ${getCategoryColor(product.category)}`}>
          {product.category === 'bijoux' ? '💎' : '🎧'} {product.category.charAt(0).toUpperCase() + product.category.slice(1)}
        </Badge>
        
        {/* Bouton favoris */}
        <Button
          variant="ghost"
          size="icon"
          className={`absolute top-3 right-3 h-8 w-8 rounded-full backdrop-blur-sm ${
            isLiked 
              ? 'bg-pink-500 text-white' 
              : 'bg-white/80 text-gray-600 hover:bg-pink-500 hover:text-white'
          } transition-all duration-200`}
          onClick={() => setIsLiked(!isLiked)}
        >
          <Heart className={`h-4 w-4 ${isLiked ? 'fill-current' : ''}`} />
        </Button>
        
        {/* Badge stock */}
        {!product.inStock && (
          <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
            <Badge variant="destructive">Rupture de stock</Badge>
          </div>
        )}
      </div>

      <CardContent className="p-4">
        <div className="space-y-2">
          <h3 className="font-semibold text-gray-800 line-clamp-2 group-hover:text-pink-600 transition-colors">
            {product.name}
          </h3>
          
          <p className="text-sm text-gray-600 line-clamp-2">
            {product.description}
          </p>
          
          {/* Rating */}
          <div className="flex items-center space-x-2">
            <div className="flex items-center space-x-1">
              {renderStars(product.rating)}
            </div>
            <span className="text-xs text-gray-500">
              ({product.reviews} avis)
            </span>
          </div>
          
          {/* Prix */}
          <div className="flex items-center justify-between">
            <span className="text-lg font-bold text-gray-900">
              {formatPrice(product.price)}
            </span>
          </div>
        </div>
      </CardContent>

      <CardFooter className="p-4 pt-0">
        <Button
          className="w-full bg-gradient-to-r from-pink-500 to-purple-500 hover:from-pink-600 hover:to-purple-600 text-white transition-all duration-200 transform hover:scale-105"
          onClick={handleAddToCart}
          disabled={!product.inStock || isLoading}
        >
          <ShoppingCart className="h-4 w-4 mr-2" />
          {isLoading ? 'Ajout...' : 'Ajouter au panier'}
        </Button>
      </CardFooter>
    </Card>
  );
};

export default ProductCard;