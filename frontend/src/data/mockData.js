// Mock data pour Darling boutique
export const mockProducts = [
  // Bijoux
  {
    id: 1,
    name: "Collier Élégant Doré",
    price: 25000,
    category: "bijoux",
    subcategory: "colliers",
    image: "https://images.unsplash.com/photo-1611652022419-a9419f74343d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHwyfHxqZXdlbHJ5fGVufDB8fHx8MTc1MzU2NTYyMHww&ixlib=rb-4.1.0&q=85",
    description: "Magnifique collier doré pour toutes occasions",
    inStock: true,
    rating: 4.8,
    reviews: 23
  },
  {
    id: 2,
    name: "Bagues Dorées Set de 3",
    price: 15000,
    category: "bijoux",
    subcategory: "bagues",
    image: "https://images.unsplash.com/photo-1543294001-f7cd5d7fb516?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHw0fHxqZXdlbHJ5fGVufDB8fHx8MTc1MzU2NTYyMHww&ixlib=rb-4.1.0&q=85",
    description: "Ensemble de 3 bagues dorées élégantes",
    inStock: true,
    rating: 4.5,
    reviews: 18
  },
  {
    id: 3,
    name: "Bracelet Argent Délicat",
    price: 18000,
    category: "bijoux",
    subcategory: "bracelets",
    image: "https://images.unsplash.com/photo-1611652022419-a9419f74343d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHwyfHxqZXdlbHJ5fGVufDB8fHx8MTc1MzU2NTYyMHww&ixlib=rb-4.1.0&q=85",
    description: "Bracelet en argent avec finition délicate",
    inStock: true,
    rating: 4.7,
    reviews: 31
  },
  
  // Tech
  {
    id: 4,
    name: "AirPods Pro Sans Fil",
    price: 85000,
    category: "tech",
    subcategory: "ecouteurs",
    image: "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2MzR8MHwxfHNlYXJjaHwzfHx3aXJlbGVzcyUyMGVhcmJ1ZHN8ZW58MHx8fHwxNzUzNTY1NjI2fDA&ixlib=rb-4.1.0&q=85",
    description: "Écouteurs sans fil de haute qualité avec réduction de bruit",
    inStock: true,
    rating: 4.9,
    reviews: 156
  },
  {
    id: 5,
    name: "Casque Bluetooth Premium",
    price: 75000,
    category: "tech",
    subcategory: "casques",
    image: "https://images.unsplash.com/photo-1628329567705-f8f7150c3cff?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwxfHxibHVldG9vdGglMjBoZWFkcGhvbmVzfGVufDB8fHx8MTc1MzU2NTYzMHww&ixlib=rb-4.1.0&q=85",
    description: "Casque audio bluetooth avec son haute fidélité",
    inStock: true,
    rating: 4.6,
    reviews: 89
  },
  {
    id: 6,
    name: "Écouteurs Colorés Set",
    price: 35000,
    category: "tech",
    subcategory: "ecouteurs",
    image: "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2MzR8MHwxfHNlYXJjaHw0fHx3aXJlbGVzcyUyMGVhcmJ1ZHN8ZW58MHx8fHwxNzUzNTY1NjI2fDA&ixlib=rb-4.1.0&q=85",
    description: "Collection d'écouteurs sans fil colorés",
    inStock: true,
    rating: 4.3,
    reviews: 67
  },
  {
    id: 7,
    name: "Ventilateur Miniature USB",
    price: 12000,
    category: "tech",
    subcategory: "ventilateurs",
    image: "https://images.unsplash.com/photo-1628329567705-f8f7150c3cff?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwxfHxibHVldG9vdGglMjBoZWFkcGhvbmVzfGVufDB8fHx8MTc1MzU2NTYzMHww&ixlib=rb-4.1.0&q=85",
    description: "Ventilateur portable miniature avec câble USB",
    inStock: true,
    rating: 4.1,
    reviews: 42
  }
];

export const categories = [
  {
    id: 'bijoux',
    name: 'Bijoux',
    subcategories: [
      { id: 'colliers', name: 'Colliers' },
      { id: 'bracelets', name: 'Bracelets' },
      { id: 'bagues', name: 'Bagues' }
    ]
  },
  {
    id: 'tech',
    name: 'Tech',
    subcategories: [
      { id: 'ecouteurs', name: 'Écouteurs Sans Fil' },
      { id: 'casques', name: 'Casques Bluetooth' },
      { id: 'ventilateurs', name: 'Ventilateurs Miniatures' }
    ]
  }
];

// Mock panier (localStorage simulation)
export const mockCart = [];

// Mock commandes
export const mockOrders = [];

// Méthodes de paiement mobile
export const paymentMethods = [
  {
    id: 'moov',
    name: 'Moov Money',
    icon: '📱',
    color: '#FF6B35'
  },
  {
    id: 'airtel',
    name: 'Airtel Money',
    icon: '💳',
    color: '#E74C3C'
  }
];

// Simulation localStorage pour le panier
export const cartStorage = {
  getCart: () => {
    const cart = localStorage.getItem('darling_cart');
    return cart ? JSON.parse(cart) : [];
  },
  
  setCart: (cart) => {
    localStorage.setItem('darling_cart', JSON.stringify(cart));
  },
  
  addToCart: (product, quantity = 1) => {
    const cart = cartStorage.getCart();
    const existingItem = cart.find(item => item.id === product.id);
    
    if (existingItem) {
      existingItem.quantity += quantity;
    } else {
      cart.push({ ...product, quantity });
    }
    
    cartStorage.setCart(cart);
    return cart;
  },
  
  removeFromCart: (productId) => {
    const cart = cartStorage.getCart();
    const updatedCart = cart.filter(item => item.id !== productId);
    cartStorage.setCart(updatedCart);
    return updatedCart;
  },
  
  updateQuantity: (productId, quantity) => {
    const cart = cartStorage.getCart();
    const item = cart.find(item => item.id === productId);
    if (item) {
      item.quantity = quantity;
      cartStorage.setCart(cart);
    }
    return cart;
  },
  
  clearCart: () => {
    localStorage.removeItem('darling_cart');
    return [];
  }
};