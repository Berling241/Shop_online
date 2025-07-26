import React, { useState, useEffect } from 'react';
import { X, Plus, Minus, Trash2, CreditCard } from 'lucide-react';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { cartAPI, ordersAPI, formatPrice, paymentMethods } from '../services/api';
import { useToast } from '../hooks/use-toast';

const Cart = ({ isOpen, onClose }) => {
  const [cart, setCart] = useState({ items: [], total: 0 });
  const [selectedPayment, setSelectedPayment] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const loadCart = async () => {
    if (!isOpen) return;
    
    setIsLoading(true);
    try {
      const cartData = await cartAPI.get();
      setCart(cartData);
    } catch (error) {
      console.error('Error loading cart:', error);
      toast({
        title: "Erreur",
        description: "Impossible de charger le panier",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadCart();
  }, [isOpen]);

  const updateQuantity = async (productId, newQuantity) => {
    if (newQuantity <= 0) {
      removeItem(productId);
      return;
    }
    
    try {
      const result = await cartAPI.updateItem(productId, newQuantity);
      setCart(result.cart);
      window.dispatchEvent(new CustomEvent('cartUpdated'));
    } catch (error) {
      console.error('Error updating quantity:', error);
      toast({
        title: "Erreur",
        description: "Impossible de mettre à jour la quantité",
        variant: "destructive",
      });
    }
  };

  const removeItem = async (productId) => {
    try {
      const result = await cartAPI.removeItem(productId);
      setCart(result.cart);
      window.dispatchEvent(new CustomEvent('cartUpdated'));
      
      toast({
        title: "Produit retiré",
        description: "Le produit a été retiré de votre panier",
        duration: 2000,
      });
    } catch (error) {
      console.error('Error removing item:', error);
      toast({
        title: "Erreur",
        description: "Impossible de retirer le produit",
        variant: "destructive",
      });
    }
  };

  const handleCheckout = async () => {
    if (!selectedPayment) {
      toast({
        title: "Erreur",
        description: "Veuillez sélectionner un mode de paiement",
        variant: "destructive",
      });
      return;
    }

    if (!phoneNumber || phoneNumber.length < 8) {
      toast({
        title: "Erreur", 
        description: "Veuillez saisir un numéro de téléphone valide",
        variant: "destructive",
      });
      return;
    }

    if (cart.items.length === 0) {
      toast({
        title: "Erreur",
        description: "Votre panier est vide",
        variant: "destructive",
      });
      return;
    }

    setIsProcessing(true);

    try {
      // Préparer les données de commande
      const orderItems = cart.items.map(item => ({
        product_id: item.product_id,
        product_name: item.product_name,
        product_price: item.product_price,
        product_image: item.product_image,
        quantity: item.quantity,
        subtotal: item.subtotal
      }));

      // Créer la commande
      const order = await ordersAPI.create({
        items: orderItems,
        payment_method: selectedPayment,
        phone_number: phoneNumber
      });

      toast({
        title: "Commande confirmée !",
        description: `Commande #${order.order_number} - Total: ${formatPrice(order.total)}`,
        duration: 5000,
      });
      
      // Recharger le panier (maintenant vide)
      await loadCart();
      window.dispatchEvent(new CustomEvent('cartUpdated'));
      
      setSelectedPayment('');
      setPhoneNumber('');
      onClose();
      
    } catch (error) {
      console.error('Error creating order:', error);
      const errorMessage = error.response?.data?.detail || "Une erreur est survenue lors de la commande";
      
      toast({
        title: "Échec de la commande",
        description: errorMessage,
        variant: "destructive",
        duration: 5000,
      });
    } finally {
      setIsProcessing(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm">
      <div className="fixed right-0 top-0 h-full w-full max-w-md bg-white shadow-xl overflow-y-auto">
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold bg-gradient-to-r from-pink-500 to-purple-500 bg-clip-text text-transparent">
              Mon Panier
            </h2>
            <Button variant="ghost" size="icon" onClick={onClose}>
              <X className="h-5 w-5" />
            </Button>
          </div>

          {isLoading ? (
            // Loading state
            <div className="text-center py-12">
              <div className="w-8 h-8 border-4 border-pink-200 border-t-pink-500 rounded-full animate-spin mx-auto mb-4"></div>
              <p className="text-gray-500">Chargement...</p>
            </div>
          ) : cart.items.length === 0 ? (
            // Panier vide
            <div className="text-center py-12">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-100 flex items-center justify-center">
                <CreditCard className="h-8 w-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-semibold text-gray-600 mb-2">Panier vide</h3>
              <p className="text-gray-500 mb-4">Ajoutez des produits pour commencer vos achats</p>
              <Button
                onClick={onClose}
                className="bg-gradient-to-r from-pink-500 to-purple-500 hover:from-pink-600 hover:to-purple-600 text-white"
              >
                Continuer les achats
              </Button>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Articles du panier */}
              <div className="space-y-4">
                {cart.items.map((item) => (
                  <Card key={item.product_id} className="overflow-hidden">
                    <CardContent className="p-4">
                      <div className="flex space-x-4">
                        <img
                          src={item.product_image}
                          alt={item.product_name}
                          className="w-16 h-16 object-cover rounded-lg"
                        />
                        
                        <div className="flex-1">
                          <h4 className="font-semibold text-sm mb-1">{item.product_name}</h4>
                          <p className="text-sm text-gray-600 mb-2">
                            {formatPrice(item.product_price)}
                          </p>
                          
                          <div className="flex items-center justify-between">
                            {/* Contrôles quantité */}
                            <div className="flex items-center space-x-2">
                              <Button
                                variant="outline"
                                size="icon"
                                className="h-8 w-8"
                                onClick={() => updateQuantity(item.product_id, item.quantity - 1)}
                              >
                                <Minus className="h-3 w-3" />
                              </Button>
                              
                              <span className="w-8 text-center font-semibold">
                                {item.quantity}
                              </span>
                              
                              <Button
                                variant="outline"
                                size="icon"
                                className="h-8 w-8"
                                onClick={() => updateQuantity(item.product_id, item.quantity + 1)}
                              >
                                <Plus className="h-3 w-3" />
                              </Button>
                            </div>
                            
                            {/* Bouton supprimer */}
                            <Button
                              variant="ghost"
                              size="icon"
                              className="h-8 w-8 text-red-500 hover:text-red-700"
                              onClick={() => removeItem(item.product_id)}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {/* Total */}
              <Card className="bg-gradient-to-r from-pink-50 to-purple-50">
                <CardContent className="p-4">
                  <div className="flex justify-between items-center text-lg font-bold">
                    <span>Total</span>
                    <span className="text-pink-600">
                      {formatPrice(cart.total)}
                    </span>
                  </div>
                </CardContent>
              </Card>

              {/* Méthodes de paiement */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Paiement Mobile</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Sélection du mode de paiement */}
                  <div className="grid grid-cols-2 gap-3">
                    {paymentMethods.map((method) => (
                      <Button
                        key={method.id}
                        variant={selectedPayment === method.id ? 'default' : 'outline'}
                        className={`h-12 ${
                          selectedPayment === method.id
                            ? 'bg-gradient-to-r from-pink-500 to-purple-500 text-white'
                            : 'hover:border-pink-300'
                        }`}
                        onClick={() => setSelectedPayment(method.id)}
                      >
                        <span className="mr-2">{method.icon}</span>
                        {method.name}
                      </Button>
                    ))}
                  </div>

                  {/* Numéro de téléphone */}
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Numéro de téléphone
                    </label>
                    <input
                      type="tel"
                      placeholder="Ex: 07 XX XX XX XX"
                      value={phoneNumber}
                      onChange={(e) => setPhoneNumber(e.target.value)}
                      className="w-full p-3 border border-gray-200 rounded-lg focus:border-pink-300 focus:ring-2 focus:ring-pink-100 transition-colors"
                    />
                  </div>

                  {/* Bouton de commande */}
                  <Button
                    className="w-full h-12 bg-gradient-to-r from-pink-500 to-purple-500 hover:from-pink-600 hover:to-purple-600 text-white transition-all duration-200"
                    onClick={handleCheckout}
                    disabled={isProcessing}
                  >
                    {isProcessing ? (
                      <div className="flex items-center space-x-2">
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        <span>Traitement...</span>
                      </div>
                    ) : (
                      <>
                        <CreditCard className="h-4 w-4 mr-2" />
                        Commander ({formatPrice(cart.total)})
                      </>
                    )}
                  </Button>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Cart;