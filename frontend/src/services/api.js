import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Générer ou récupérer un session_id
const getSessionId = () => {
  let sessionId = localStorage.getItem('darling_session_id');
  if (!sessionId) {
    sessionId = 'session_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('darling_session_id', sessionId);
  }
  return sessionId;
};

// Instance axios configurée
const apiClient = axios.create({
  baseURL: API,
  timeout: 10000,
});

// Intercepteur pour ajouter le session_id aux headers
apiClient.interceptors.request.use((config) => {
  config.headers['X-Session-ID'] = getSessionId();
  return config;
});

// Products API
export const productsAPI = {
  // Récupérer tous les produits avec filtres optionnels
  getAll: async (filters = {}) => {
    const params = new URLSearchParams();
    
    if (filters.category) params.append('category', filters.category);
    if (filters.subcategory) params.append('subcategory', filters.subcategory);
    if (filters.search) params.append('search', filters.search);
    if (filters.sort_by) params.append('sort_by', filters.sort_by);
    
    const response = await apiClient.get(`/products?${params.toString()}`);
    return response.data;
  },

  // Récupérer un produit spécifique
  getById: async (productId) => {
    const response = await apiClient.get(`/products/${productId}`);
    return response.data;
  }
};

// Cart API
export const cartAPI = {
  // Récupérer le panier
  get: async () => {
    const sessionId = getSessionId();
    const response = await apiClient.get(`/cart/${sessionId}`);
    return response.data;
  },

  // Ajouter un produit au panier
  addItem: async (productId, quantity = 1) => {
    const sessionId = getSessionId();
    const response = await apiClient.post(`/cart/${sessionId}/add`, {
      product_id: productId,
      quantity: quantity
    });
    return response.data;
  },

  // Mettre à jour la quantité d'un produit
  updateItem: async (productId, quantity) => {
    const sessionId = getSessionId();
    const response = await apiClient.put(`/cart/${sessionId}/update/${productId}`, {
      quantity: quantity
    });
    return response.data;
  },

  // Supprimer un produit du panier
  removeItem: async (productId) => {
    const sessionId = getSessionId();
    const response = await apiClient.delete(`/cart/${sessionId}/remove/${productId}`);
    return response.data;
  },

  // Vider le panier
  clear: async () => {
    const sessionId = getSessionId();
    const response = await apiClient.delete(`/cart/${sessionId}/clear`);
    return response.data;
  }
};

// Orders API
export const ordersAPI = {
  // Créer une commande
  create: async (orderData) => {
    const sessionId = getSessionId();
    const response = await apiClient.post('/orders', {
      ...orderData,
      session_id: sessionId
    });
    return response.data;
  },

  // Récupérer une commande
  getById: async (orderId) => {
    const response = await apiClient.get(`/orders/${orderId}`);
    return response.data;
  },

  // Récupérer toutes les commandes de la session
  getAll: async () => {
    const sessionId = getSessionId();
    const response = await apiClient.get(`/orders?session_id=${sessionId}`);
    return response.data;
  }
};

// Categories API
export const categoriesAPI = {
  // Récupérer toutes les catégories
  getAll: async () => {
    const response = await apiClient.get('/categories');
    return response.data.categories;
  }
};

// Utilitaires
export const formatPrice = (price) => {
  return new Intl.NumberFormat('fr-FR').format(price) + ' FCFA';
};

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

export default {
  products: productsAPI,
  cart: cartAPI,
  orders: ordersAPI,
  categories: categoriesAPI,
  formatPrice,
  paymentMethods,
  getSessionId
};