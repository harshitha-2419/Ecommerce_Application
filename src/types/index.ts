export interface Product {
  id: string;
  name: string;
  price: number;
  description: string;
  imageUrl: string;
  category: string;
  views: number;
  purchases: number;
  discount?: number;
}

export interface User {
  id: string;
  username: string;
  email: string;
  password: string;
}

export interface CartItem {
  productId: string;
  quantity: number;
}

export interface ChatMessage {
  id: string;
  userId: string;
  message: string;
  timestamp: Date;
  isUser: boolean;
}

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

export interface CartContextType {
  items: CartItem[];
  addToCart: (productId: string) => void;
  removeFromCart: (productId: string) => void;
  updateQuantity: (productId: string, quantity: number) => void;
  clearCart: () => void;
}

export interface ChatContextType {
  messages: ChatMessage[];
  sendMessage: (message: string) => void;
  clearChat: () => void;
}